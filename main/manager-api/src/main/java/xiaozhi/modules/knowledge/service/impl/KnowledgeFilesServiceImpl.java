package xiaozhi.modules.knowledge.service.impl;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;

import org.apache.commons.lang3.StringUtils;
import org.springframework.beans.BeanUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Lazy;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.multipart.MultipartFile;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.core.conditions.update.UpdateWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;

import lombok.extern.slf4j.Slf4j;
import xiaozhi.common.exception.ErrorCode;
import org.springframework.util.CollectionUtils;
import xiaozhi.common.exception.RenException;
import xiaozhi.modules.knowledge.dto.KnowledgeFilesDTO;
import xiaozhi.modules.knowledge.dto.document.ChunkDTO;
import xiaozhi.modules.knowledge.dto.document.RetrievalDTO;
import xiaozhi.modules.knowledge.dto.document.DocumentDTO;
import xiaozhi.common.page.PageData;
import xiaozhi.common.redis.RedisKeys;
import xiaozhi.common.redis.RedisUtils;
import xiaozhi.common.service.impl.BaseServiceImpl;
import xiaozhi.modules.knowledge.dao.DocumentDao;
import xiaozhi.modules.knowledge.entity.DocumentEntity;
import xiaozhi.modules.knowledge.rag.KnowledgeBaseAdapter;
import xiaozhi.modules.knowledge.rag.KnowledgeBaseAdapterFactory;
import xiaozhi.modules.knowledge.service.KnowledgeBaseService;
import xiaozhi.modules.knowledge.service.KnowledgeFilesService;

@Service
@Slf4j
public class KnowledgeFilesServiceImpl extends BaseServiceImpl<DocumentDao, DocumentEntity>
        implements KnowledgeFilesService {

    private final KnowledgeBaseService knowledgeBaseService;
    private final DocumentDao documentDao;
    private final ObjectMapper objectMapper;
    private final RedisUtils redisUtils;

    public KnowledgeFilesServiceImpl(KnowledgeBaseService knowledgeBaseService,
            DocumentDao documentDao,
            ObjectMapper objectMapper,
            RedisUtils redisUtils) {
        this.knowledgeBaseService = knowledgeBaseService;
        this.documentDao = documentDao;
        this.objectMapper = objectMapper;
        this.redisUtils = redisUtils;
    }

    @Lazy
    @Autowired
    private KnowledgeFilesService self;

    @Override
    public Map<String, Object> getRAGConfig(String ragModelId) {
        return knowledgeBaseService.getRAGConfig(ragModelId);
    }

    @Override
    public PageData<KnowledgeFilesDTO> getPageList(KnowledgeFilesDTO knowledgeFilesDTO, Integer page, Integer limit) {
        log.info("=== Bắt đầu nhận danh sách các tài liệu cơ sở kiến thức (Local-First Phiên bản tối ưu hóa) ===");
        String datasetId = knowledgeFilesDTO.getDatasetId();
        if (StringUtils.isBlank(datasetId)) {
            throw new RenException(ErrorCode.RAG_DATASET_ID_AND_MODEL_ID_NOT_NULL);
        }

        // Đồng bộ hóa đối chiếu hoàn toàn: lấy tài liệu từ xa từ RAGFlow, đồng bộ hóa thời gian thực đảm bảo nhận biết ngay lập tức các thay đổi từ xa
        try {
            self.syncDocumentsFromRAG(datasetId);
        } catch (Exception e) {
            log.warn("từRAGFlowKhông thể đồng bộ hóa tất cả tài liệu(Không ảnh hưởng đến các truy vấn cục bộ): datasetId={}, error={}", datasetId, e.getMessage());
        }

        // 1. Nhận dữ liệu bảng bóng cục bộ (phân trang MyBatis-Plus)
        Page<DocumentEntity> pageParams = new Page<>(page, limit);
        QueryWrapper<DocumentEntity> queryWrapper = new QueryWrapper<>();
        queryWrapper.eq("dataset_id", datasetId);
        if (StringUtils.isNotBlank(knowledgeFilesDTO.getName())) {
            queryWrapper.like("name", knowledgeFilesDTO.getName());
        }
        if (StringUtils.isNotBlank(knowledgeFilesDTO.getRun())) {
            queryWrapper.eq("run", knowledgeFilesDTO.getRun());
        }
        if (StringUtils.isNotBlank(knowledgeFilesDTO.getStatus())) {
            queryWrapper.eq("status", knowledgeFilesDTO.getStatus());
        }
        queryWrapper.orderByDesc("created_at");

        // 2. Thực hiện truy vấn cục bộ
        Page<DocumentEntity> iPage = documentDao.selectPage(pageParams, queryWrapper);

        // 3. Chuyển đổi DTO thủ công
        List<KnowledgeFilesDTO> dtoList = new ArrayList<>();
        for (DocumentEntity entity : iPage.getRecords()) {
            dtoList.add(convertEntityToDTO(entity));
        }
        PageData<KnowledgeFilesDTO> pageData = new PageData<>(dtoList, iPage.getTotal());

        // 4. Đồng bộ hóa trạng thái động (có giới hạn và bảo vệ hiện tại)
        // [Sửa lỗi] P1: Mở rộng danh sách trắng đồng bộ hóa, CANCEL/FAIL cũng cho phép đồng bộ hóa tần số thấp để hỗ trợ khả năng tự phục hồi
        if (pageData.getList() != null && !pageData.getList().isEmpty()) {
            KnowledgeBaseAdapter adapter = null;
            for (KnowledgeFilesDTO dto : pageData.getList()) {
                String runStatus = dto.getRun();
                // Đồng bộ hóa mức độ ưu tiên cao: CHẠY/KHỞI ĐỘNG (thời gian hồi chiêu 5 giây)
                boolean isActiveSync = "RUNNING".equals(runStatus) || "UNSTART".equals(runStatus);
                // Đồng bộ hóa tự phục hồi tần số thấp: CANCEL/FAIL (làm mát trong 60 giây) để ngăn chặn việc khóa vĩnh viễn các trạng thái lỗi
                boolean isRecoverySync = "CANCEL".equals(runStatus) || "FAIL".equals(runStatus);
                boolean needSync = isActiveSync || isRecoverySync;

                if (needSync) {
                    // Bảo vệ giới hạn dòng điện: Thời gian hồi chiêu 5 giây ở trạng thái hoạt động, thời gian hồi chiêu 60 giây ở trạng thái tự phục hồi
                    long cooldownMs = isActiveSync ? 5000 : 60000;
                    DocumentEntity localEntity = documentDao.selectOne(new QueryWrapper<DocumentEntity>()
                            .eq("document_id", dto.getDocumentId()));
                    if (localEntity != null && localEntity.getLastSyncAt() != null) {
                        long diff = System.currentTimeMillis() - localEntity.getLastSyncAt().getTime();
                        if (diff < cooldownMs) {
                            continue;
                        }
                    }

                    // Bộ điều hợp khởi tạo lười biếng, chỉ được tạo khi thực sự cần đồng bộ hóa
                    if (adapter == null) {
                        try {
                            Map<String, Object> ragConfig = knowledgeBaseService.getRAGConfigByDatasetId(datasetId);
                            adapter = KnowledgeBaseAdapterFactory.getAdapter(extractAdapterType(ragConfig), ragConfig);
                        } catch (Exception e) {
                            log.warn("Đồng bộ hóa bị gián đoạn：Không thể khởi tạo bộ chuyển đổi, {}", e.getMessage());
                            break;
                        }
                    }
                    // [Sửa phím] Ghi lại số lượng Token trước khi đồng bộ hóa và sử dụng nó để tính toán mức tăng
                    Long oldTokenCount = dto.getTokenCount() != null ? dto.getTokenCount() : 0L;

                    syncDocumentStatusWithRAG(dto, adapter);

                    // Tính toán mức tăng và cập nhật số liệu thống kê cơ sở kiến thức (phù hợp với các nhiệm vụ đã lên lịch)
                    Long newTokenCount = dto.getTokenCount() != null ? dto.getTokenCount() : 0L;
                    Long tokenDelta = newTokenCount - oldTokenCount;
                    if (tokenDelta != 0) {
                        knowledgeBaseService.updateStatistics(datasetId, 0, 0L, tokenDelta);
                        log.info("Đồng bộ hóa tải chậm: Thống kê cơ sở kiến thức chính xác, docId={}, tokenDelta={}", dto.getDocumentId(), tokenDelta);
                    }
                }
            }
        }

        log.info("Lấy danh sách tài liệu thành công，tổng cộng: {}", pageData.getTotal());
        return pageData;
    }

    /**
     * Chuyển đổi các thực thể bản ghi cục bộ thành DTO, căn chỉnh thủ công các trường không nhất quán (kích thước -> kích thước tệp, loại -> loại tệp)
     */
    private KnowledgeFilesDTO convertEntityToDTO(DocumentEntity entity) {
        if (entity == null) {
            return null;
        }
        KnowledgeFilesDTO dto = new KnowledgeFilesDTO();
        // 1. Sao chép các trường cơ bản
        BeanUtils.copyProperties(entity, dto);

        // Vấn đề 2: Sửa lỗi ngữ nghĩa ID. Giao diện người dùng đã quen với việc sử dụng id làm khóa chính cho các hoạt động.
        // Trong mô-đun này, documentId từ xa phải luôn được ánh xạ tới id của DTO để đảm bảo rằng ID giao diện người dùng nhất quán trong các thao tác như chi tiết/xóa.
        dto.setId(entity.getDocumentId());

        // 2. Chuyển đổi các thực thể bản ghi cục bộ thành DTO và căn chỉnh các trường không nhất quán theo cách thủ công (kích thước -> kích thước tệp, loại -> loại tệp)
        dto.setFileSize(entity.getSize());
        dto.setFileType(entity.getType());
        dto.setRun(entity.getRun());
        dto.setChunkCount(entity.getChunkCount());
        dto.setTokenCount(entity.getTokenCount());
        dto.setError(entity.getError());

        // 3. Quá trình giải tuần tự hóa JSON siêu dữ liệu tùy chỉnh (Vấn đề 3)
        if (StringUtils.isNotBlank(entity.getMetaFields())) {
            try {
                dto.setMetaFields(objectMapper.readValue(entity.getMetaFields(),
                        new TypeReference<Map<String, Object>>() {
                        }));
            } catch (Exception e) {
                log.warn("Khử lưu huỳnh MetaFields thất bại, entityId: {}, error: {}", entity.getId(), e.getMessage());
            }
        }

        // 4. Phân tích cú pháp và định cấu hình quá trình giải tuần tự hóa JSON
        if (StringUtils.isNotBlank(entity.getParserConfig())) {
            try {
                dto.setParserConfig(objectMapper.readValue(entity.getParserConfig(),
                        new com.fasterxml.jackson.core.type.TypeReference<Map<String, Object>>() {
                        }));
            } catch (Exception e) {
                log.warn("Khử lưu huỳnh ParserConfig thất bại, entityId: {}, error: {}", entity.getId(), e.getMessage());
            }
        }
        return dto;

    }

    /**
     * Đồng bộ hóa trạng thái tài liệu với trạng thái RAG thực tế
     * Tối ưu hóa logic đồng bộ hóa trạng thái để đảm bảo trạng thái trong quá trình phân tích có thể được hiển thị bình thường
     * Chỉ cập nhật trạng thái hoàn tất nếu tài liệu có các phần và thời gian phân tích cú pháp vượt quá 30 giây
     */
    /**
     * Đồng bộ hóa trạng thái tài liệu với trạng thái RAG thực tế (nâng cao: hỗ trợ bộ điều hợp đầu vào bên ngoài)
     */
    private void syncDocumentStatusWithRAG(KnowledgeFilesDTO dto, KnowledgeBaseAdapter adapter) {
        if (dto == null || StringUtils.isBlank(dto.getDocumentId()) || adapter == null) {
            return;
        }

        String documentId = dto.getDocumentId();
        String datasetId = dto.getDatasetId();

        try {
            // Sử dụng ListReq được gõ mạnh với tính năng lọc ID để lấy trạng thái
            DocumentDTO.ListReq listReq = DocumentDTO.ListReq.builder()
                    .id(documentId)
                    .page(1)
                    .pageSize(1)
                    .build();

            PageData<KnowledgeFilesDTO> remoteList = adapter.getDocumentList(datasetId, listReq);

            if (remoteList != null && remoteList.getList() != null && !remoteList.getList().isEmpty()) {
                KnowledgeFilesDTO remoteDto = remoteList.getList().get(0);
                String remoteStatus = remoteDto.getStatus();

                // Logic phán đoán liên kết trạng thái cốt lõi
                boolean statusChanged = remoteStatus != null && !remoteStatus.equals(dto.getStatus());
                boolean runChanged = remoteDto.getRun() != null && !remoteDto.getRun().equals(dto.getRun());
                boolean isProcessing = "RUNNING".equals(remoteDto.getRun()) || "UNSTART".equals(remoteDto.getRun());

                // Miễn là trạng thái thay đổi hoặc trạng thái đang chạy thay đổi hoặc tệp vẫn đang được phân tích cú pháp (làm mới tiến trình theo thời gian thực), quá trình đồng bộ hóa sẽ được thực hiện.
                if (statusChanged || runChanged || isProcessing) {
                    log.info("đồng bộ bóng：thay đổi trạng thái={}，Phân tích cú pháp={}，Tài liệu={}，trạng thái mới nhất={}，Tiến độ={}",
                            statusChanged, isProcessing, documentId, remoteStatus, remoteDto.getProgress());

                    // 1. Đồng bộ bộ nhớ DTO
                    dto.setStatus(remoteStatus);
                    dto.setRun(remoteDto.getRun());
                    dto.setProgress(remoteDto.getProgress());
                    dto.setChunkCount(remoteDto.getChunkCount());
                    dto.setTokenCount(remoteDto.getTokenCount());
                    dto.setError(remoteDto.getError());
                    dto.setProcessDuration(remoteDto.getProcessDuration());
                    dto.setThumbnail(remoteDto.getThumbnail());

                    // 2. Đồng bộ bảng bóng cục bộ
                    UpdateWrapper<DocumentEntity> updateWrapper = new UpdateWrapper<DocumentEntity>()
                            .set("status", remoteStatus)
                            .set("run", remoteDto.getRun())
                            .set("progress", remoteDto.getProgress())
                            .set("chunk_count", remoteDto.getChunkCount())
                            .set("token_count", remoteDto.getTokenCount())
                            .set("error", remoteDto.getError())
                            .set("process_duration", remoteDto.getProcessDuration())
                            .set("thumbnail", remoteDto.getThumbnail())
                            .eq("document_id", documentId)
                            .eq("dataset_id", datasetId);

                    // Đồng bộ hóa siêu dữ liệu nối tiếp
                    if (remoteDto.getMetaFields() != null) {
                        try {
                            updateWrapper.set("meta_fields",
                                    objectMapper.writeValueAsString(remoteDto.getMetaFields()));
                        } catch (Exception e) {
                            log.warn("Đồng bộ hóa siêu dữ liệu tuần tự không thành công: {}", e.getMessage());
                        }
                    }

                    // Ưu tiên đồng bộ hóa thời gian cập nhật bên RAG để tránh hành vi đồng bộ hóa cục bộ ghi đè thời gian sửa đổi doanh nghiệp
                    Date lastUpdate = remoteDto.getUpdatedAt() != null ? remoteDto.getUpdatedAt() : new Date();
                    updateWrapper.set("updated_at", lastUpdate);
                    updateWrapper.set("last_sync_at", new Date()); // Ghi lại thời gian đồng bộ hóa thư viện bóng

                    documentDao.update(null, updateWrapper);
                }
            } else {
                // Vấn đề 6: Danh sách từ xa trống. Tài liệu có thể đã bị xóa hoặc có thể xảy ra sự cố với lệnh gọi bộ chuyển đổi.
                // [Sửa lỗi] P2: Chỉ đánh dấu CANCEL nếu điều khiển từ xa trả về danh sách trống hợp pháp
                // Đồng thời, Last_sync_at được cập nhật để hợp tác với cơ chế làm mát P1 nhằm ngăn chặn việc đánh giá sai tần số cao.
                log.warn("Nhận thức đồng bộ hóa từ xa：RAGFlow Trả về một danh sách tài liệu trống, docId={}, Hiện trạng địa phương={}",
                        documentId, dto.getRun());
                dto.setRun("CANCEL");
                dto.setError("Tài liệu đã bị xóa trong dịch vụ từ xa");

                documentDao.update(null, new UpdateWrapper<DocumentEntity>()
                        .set("run", "CANCEL")
                        .set("error", "Tài liệu đã bị xóa trong dịch vụ từ xa")
                        .set("updated_at", new Date())
                        .set("last_sync_at", new Date())
                        .eq("document_id", documentId));
            }
        } catch (Exception e) {
            // [Sửa lỗi] P2: CANCEL không được đánh dấu khi bộ điều hợp gọi một ngoại lệ để tránh đánh giá sai do sự cố mạng/khử tuần tự hóa.
            // Chỉ ghi lại nhật ký và đợi chu kỳ đồng bộ hóa tiếp theo để thử lại.
            log.warn("Cuộc gọi bộ điều hợp không thành công khi đồng bộ hóa trạng thái tài liệu(Không được đánh dấuCANCEL), documentId: {}, error: {}",
                    documentId, e.getMessage());
        }
    }

    @Override
    public DocumentDTO.InfoVO getByDocumentId(String documentId, String datasetId) {
        if (StringUtils.isBlank(documentId) || StringUtils.isBlank(datasetId)) {
            throw new RenException(ErrorCode.RAG_DATASET_ID_AND_MODEL_ID_NOT_NULL);
        }

        log.info("=== Bắt đầu dựa trêndocumentIdNhận tài liệu ===");
        log.info("documentId: {}, datasetId: {}", documentId, datasetId);

        try {
            // Nhận cấu hình RAG
            Map<String, Object> ragConfig = knowledgeBaseService.getRAGConfigByDatasetId(datasetId);

            // Trích xuất loại bộ điều hợp
            String adapterType = extractAdapterType(ragConfig);

            // Sử dụng nhà máy sản xuất bộ chuyển đổi để lấy phiên bản bộ chuyển đổi
            KnowledgeBaseAdapter adapter = KnowledgeBaseAdapterFactory.getAdapter(adapterType, ragConfig);

            // Nhận chi tiết tài liệu bằng bộ chuyển đổi
            DocumentDTO.InfoVO info = adapter.getDocumentById(datasetId, documentId);

            if (info != null) {
                log.info("Lấy thông tin chi tiết tài liệu thành công，documentId: {}", documentId);
                return info;
            } else {
                throw new RenException(ErrorCode.Knowledge_Base_RECORD_NOT_EXISTS);
            }

        } catch (Exception e) {
            log.error("TheodocumentIdKhông lấy được tài liệu: {}", e.getMessage(), e);
            String errorMessage = e.getMessage() != null ? e.getMessage() : "null";
            if (e instanceof RenException) {
                throw (RenException) e;
            }
            throw new RenException(ErrorCode.RAG_API_ERROR, errorMessage);
        } finally {
            log.info("=== TheodocumentIdHoạt động thu thập tài liệu kết thúc ===");
        }
    }

    @Override
    public KnowledgeFilesDTO uploadDocument(String datasetId, MultipartFile file, String name,
            Map<String, Object> metaFields, String chunkMethod,
            Map<String, Object> parserConfig) {
        if (StringUtils.isBlank(datasetId) || file == null || file.isEmpty()) {
            throw new RenException(ErrorCode.PARAMS_GET_ERROR);
        }

        log.info("=== Bắt đầu thao tác tải tài liệu lên (Tối ưu hóa tính nhất quán mạnh mẽ) ===");

        // 1. Chuẩn bị (không giao dịch)
        String fileName = StringUtils.isNotBlank(name) ? name : file.getOriginalFilename();
        if (StringUtils.isBlank(fileName)) {
            throw new RenException(ErrorCode.RAG_FILE_NAME_NOT_NULL);
        }

        log.info("1. Bắt đầu tải lên từ xa: datasetId={}, fileName={}", datasetId, fileName);

        // Nhận bộ chuyển đổi (không giao dịch)
        Map<String, Object> ragConfig = knowledgeBaseService.getRAGConfigByDatasetId(datasetId);
        KnowledgeBaseAdapter adapter = KnowledgeBaseAdapterFactory.getAdapter(extractAdapterType(ragConfig), ragConfig);

        // Xây dựng một yêu cầu được gõ mạnh DTO
        DocumentDTO.UploadReq uploadReq = DocumentDTO.UploadReq.builder()
                .datasetId(datasetId)
                .file(file)
                .name(fileName)
                .metaFields(metaFields)
                .build();

        // Chuyển đổi phương thức chunked (Chuỗi -> Enum)
        if (StringUtils.isNotBlank(chunkMethod)) {
            try {
                uploadReq.setChunkMethod(DocumentDTO.InfoVO.ChunkMethod.valueOf(chunkMethod.toUpperCase()));
            } catch (Exception e) {
                log.warn("Phương pháp phân đoạn không hợp lệ: {}, Cấu hình mặc định nền sẽ được sử dụng", chunkMethod);
            }
        }

        // Chuyển đổi cấu hình phân tích cú pháp (Bản đồ -> DTO)
        if (parserConfig != null && !parserConfig.isEmpty()) {
            uploadReq.setParserConfig(objectMapper.convertValue(parserConfig, DocumentDTO.InfoVO.ParserConfig.class));
        }

        // Thực hiện upload từ xa (tốn thời gian IO, giao dịch bên ngoài)
        KnowledgeFilesDTO result = adapter.uploadDocument(uploadReq);

        if (result == null || StringUtils.isBlank(result.getDocumentId())) {
            throw new RenException(ErrorCode.RAG_API_ERROR, "Tải lên từ xa đã thành công nhưng không trả về kết quả hợp lệ. DocumentID");
        }

        // 2. Sự kiên trì cục bộ (được gọi thông qua bản thân để kích hoạt tác nhân @Transactional)
        log.info("2. Lưu đồng bộ các bản ghi bóng cục bộ: documentId={}", result.getDocumentId());
        self.saveDocumentShadow(datasetId, result, fileName, chunkMethod, parserConfig);

        log.info("=== Đã lưu thành công bản ghi bóng và tải lên tài liệu ===");
        return result;
    }

    /**
     * Lưu bản ghi bóng nguyên tử (Ngữ nghĩa Upsert)
     * Nếu document_id đã tồn tại, hãy cập nhật nó; nếu nó không tồn tại, hãy chèn nó để tránh xung đột ràng buộc ĐỘC ĐÁO.
     *
     * @return true=chèn mới, false=cập nhật bản ghi hiện có
     */
    @Transactional(rollbackFor = Exception.class)
    public boolean saveDocumentShadow(String datasetId, KnowledgeFilesDTO result, String originalName, String chunkMethod,
            Map<String, Object> parserConfig) {
        DocumentEntity entity = new DocumentEntity();
        entity.setDatasetId(datasetId);
        entity.setDocumentId(result.getDocumentId());
        entity.setName(StringUtils.isNotBlank(result.getName()) ? result.getName() : originalName);
        entity.setSize(result.getFileSize());
        entity.setType(getFileType(entity.getName()));
        entity.setChunkMethod(chunkMethod);

        if (parserConfig != null) {
            try {
                entity.setParserConfig(objectMapper.writeValueAsString(parserConfig));
            } catch (Exception e) {
                log.warn("Cấu hình phân tích cú pháp tuần tự hóa không thành công: {}", e.getMessage());
            }
        }

        entity.setStatus(result.getStatus() != null ? result.getStatus() : "1");
        entity.setRun(result.getRun());
        entity.setProgress(result.getProgress());
        entity.setThumbnail(result.getThumbnail());
        entity.setProcessDuration(result.getProcessDuration());
        entity.setSourceType(result.getSourceType());
        entity.setError(result.getError());
        entity.setChunkCount(result.getChunkCount());
        entity.setTokenCount(result.getTokenCount());
        entity.setEnabled(1);

        // Siêu dữ liệu liên tục
        if (result.getMetaFields() != null) {
            try {
                entity.setMetaFields(objectMapper.writeValueAsString(result.getMetaFields()));
            } catch (Exception e) {
                log.warn("Không thể duy trì siêu dữ liệu bóng: {}", e.getMessage());
            }
        }

        // Đồng bộ hóa dấu thời gian bên RAG trước, nếu không thì sử dụng giờ địa phương
        entity.setCreatedAt(result.getCreatedAt() != null ? result.getCreatedAt() : new Date());
        entity.setUpdatedAt(result.getUpdatedAt() != null ? result.getUpdatedAt() : new Date());

        // Upsert: Kiểm tra xem document_id đã tồn tại chưa, cập nhật nếu nó tồn tại, chèn nếu nó không tồn tại
        DocumentEntity existing = documentDao.selectOne(
                new QueryWrapper<DocumentEntity>().eq("document_id", entity.getDocumentId()));

        if (existing != null) {
            entity.setId(existing.getId());
            entity.setCreatedAt(existing.getCreatedAt()); // Giữ nguyên thời gian tạo ban đầu
            documentDao.updateById(entity);
            log.info("Bản ghi bóng được cập nhật: documentId={}", entity.getDocumentId());
            return false;
        } else {
            documentDao.insert(entity);
            // Tăng tổng số tài liệu trong tập dữ liệu khi thêm bản ghi mới
            knowledgeBaseService.updateStatistics(datasetId, 1, 0L, 0L);
            log.info("Đã chèn bản ghi bóng: documentId={}, datasetId={}", entity.getDocumentId(), datasetId);
            return true;
        }
    }

    @Override
    @Transactional(propagation = Propagation.NOT_SUPPORTED)
    public void deleteDocuments(String datasetId, DocumentDTO.BatchIdReq req) {
        if (StringUtils.isBlank(datasetId) || req == null || req.getIds() == null || req.getIds().isEmpty()) {
            throw new RenException(ErrorCode.RAG_DATASET_ID_AND_MODEL_ID_NOT_NULL);
        }

        List<String> documentIds = req.getIds();
        log.info("=== Bắt đầu xóa tài liệu theo đợt: datasetId={}, count={} ===", datasetId, documentIds.size());

        // 1. Xem trước trạng thái và quyền hàng loạt
        List<DocumentEntity> entities = documentDao.selectList(
                new QueryWrapper<DocumentEntity>()
                        .eq("dataset_id", datasetId)
                        .in("document_id", documentIds));

        if (entities.size() != documentIds.size()) {
            log.warn("Một số tài liệu không tồn tại hoặc có quyền sở hữu bất thường: dự kiến={}, thực tế={}", documentIds.size(), entities.size());
            throw new RenException(ErrorCode.NO_PERMISSION);
        }

        long totalChunkDelta = 0;
        long totalTokenDelta = 0;

        for (DocumentEntity entity : entities) {
            // Chặn các yêu cầu xóa tài liệu đang được phân tích cú pháp
            // [Sửa lỗi] Trường chạy (CHẠY) nên được sử dụng trong phân tích cú pháp thay vì trường trạng thái
            // status="1" có nghĩa là "đã bật/bình thường", không phải "phân tích cú pháp"
            if ("RUNNING".equals(entity.getRun())) {
                log.warn("Chặn các yêu cầu xóa các tệp đang được phân tích cú pháp: docId={}", entity.getDocumentId());
                throw new RenException(ErrorCode.RAG_DOCUMENT_PARSING_DELETE_ERROR);
            }
            totalChunkDelta += entity.getChunkCount() != null ? entity.getChunkCount() : 0L;
            totalTokenDelta += entity.getTokenCount() != null ? entity.getTokenCount() : 0L;
        }

        // 2. Nhận bộ chuyển đổi (không giao dịch)
        Map<String, Object> ragConfig = knowledgeBaseService.getRAGConfigByDatasetId(datasetId);
        KnowledgeBaseAdapter adapter = KnowledgeBaseAdapterFactory.getAdapter(extractAdapterType(ragConfig), ragConfig);

        // 3. Thực hiện xóa từ xa
        try {
            adapter.deleteDocument(datasetId, req);
            log.info("Yêu cầu xóa hàng loạt từ xa thành công");
        } catch (Exception e) {
            log.warn("Yêu cầu xóa từ xa không thành công một phần hoặc hoàn toàn: {}", e.getMessage());
        }

        // 4. Dọn dẹp nguyên tử các bản ghi bóng cục bộ và đồng bộ hóa dữ liệu thống kê
        self.deleteDocumentShadows(documentIds, datasetId, totalChunkDelta, totalTokenDelta);

        // 5. Xóa bộ nhớ đệm
        try {
            String cacheKey = RedisKeys.getKnowledgeBaseCacheKey(datasetId);
            redisUtils.delete(cacheKey);
            log.info("Đã xóa bộ nhớ đệm tập dữ liệu: {}", cacheKey);
        } catch (Exception e) {
            log.warn("trục xuất Redis Bộ nhớ đệm không thành công: {}", e.getMessage());
        }

        log.info("=== Đã hoàn thành việc dọn dẹp tài liệu hàng loạt ===");
    }

    /**
     * Xóa hàng loạt bản ghi bóng và đồng bộ hóa số liệu thống kê của bảng cha
     */
    @Transactional(rollbackFor = Exception.class)
    public void deleteDocumentShadows(List<String> documentIds, String datasetId, Long chunkDelta, Long tokenDelta) {
        // 1. Xóa hồ sơ về mặt vật lý
        int deleted = documentDao.delete(
                new QueryWrapper<DocumentEntity>()
                        .eq("dataset_id", datasetId)
                        .in("document_id", documentIds));

        if (deleted > 0) {
            // 2. Cập nhật đồng bộ số liệu thống kê tập dữ liệu
            knowledgeBaseService.updateStatistics(datasetId, -documentIds.size(), -chunkDelta, -tokenDelta);
            log.info("Thống kê tập dữ liệu khấu trừ được đồng bộ hóa: datasetId={}, chunks={}, tokens={}", datasetId, chunkDelta, tokenDelta);
        }
    }

    /**
     * Nhận loại tệp - hỗ trợ bốn loại định dạng tài liệu RAG
     */
    private String getFileType(String fileName) {
        if (StringUtils.isBlank(fileName)) {
            log.warn("Tên tệp trống，Trở lạiunknownloại");
            return "unknown";
        }

        try {
            int lastDotIndex = fileName.lastIndexOf('.');
            if (lastDotIndex > 0 && lastDotIndex < fileName.length() - 1) {
                String extension = fileName.substring(lastDotIndex + 1).toLowerCase();

                // Loại định dạng tài liệu
                String[] documentTypes = { "pdf", "doc", "docx", "txt", "md", "mdx" };
                String[] spreadsheetTypes = { "csv", "xls", "xlsx" };
                String[] presentationTypes = { "ppt", "pptx" };

                // Kiểm tra loại tài liệu
                for (String type : documentTypes) {
                    if (type.equals(extension)) {
                        return "document";
                    }
                }

                // Kiểm tra loại bảng
                for (String type : spreadsheetTypes) {
                    if (type.equals(extension)) {
                        return "spreadsheet";
                    }
                }
                // Kiểm tra loại slide
                for (String type : presentationTypes) {
                    if (type.equals(extension)) {
                        return "presentation";
                    }
                }
                // Trả về phần mở rộng ban đầu dưới dạng loại tệp
                return extension;
            }
            return "unknown";
        } catch (Exception e) {
            log.error("Không thể lấy được loại tệp: ", e);
            return "unknown";
        }
    }

    /**
     * Trích xuất loại bộ điều hợp từ cấu hình RAG
     */
    private String extractAdapterType(Map<String, Object> config) {
        if (config == null) {
            throw new RenException(ErrorCode.RAG_CONFIG_NOT_FOUND);
        }

        // Trích xuất trường loại từ cấu hình
        String adapterType = (String) config.get("type");
        if (StringUtils.isBlank(adapterType)) {
            throw new RenException(ErrorCode.RAG_ADAPTER_TYPE_NOT_FOUND);
        }

        // Xác minh rằng loại bộ điều hợp đã được đăng ký
        if (!KnowledgeBaseAdapterFactory.isAdapterTypeRegistered(adapterType)) {
            throw new RenException(ErrorCode.RAG_ADAPTER_TYPE_NOT_SUPPORTED, "Loại bộ chuyển đổi chưa được đăng ký: " + adapterType);
        }

        return adapterType;
    }

    @Override
    public boolean parseDocuments(String datasetId, List<String> documentIds) {
        if (StringUtils.isBlank(datasetId) || documentIds == null || documentIds.isEmpty()) {
            throw new RenException(ErrorCode.RAG_DATASET_ID_AND_MODEL_ID_NOT_NULL);
        }

        log.info("=== Bắt đầu phân tích tài liệu（Cắt thành từng miếng） ===");
        log.info("datasetId: {}, documentIds: {}", datasetId, documentIds);

        try {
            // Nhận cấu hình RAG
            Map<String, Object> ragConfig = knowledgeBaseService.getRAGConfigByDatasetId(datasetId);

            // Trích xuất loại bộ điều hợp
            String adapterType = extractAdapterType(ragConfig);

            // Nhận bộ điều hợp cơ sở kiến thức
            KnowledgeBaseAdapter adapter = KnowledgeBaseAdapterFactory.getAdapter(adapterType, ragConfig);

            log.debug("Phân tích các tham số tài liệu: documentIds: {}", documentIds);

            // Gọi bộ điều hợp để phân tích tài liệu
            boolean result = adapter.parseDocuments(datasetId, documentIds);

            if (result) {
                log.info("Lệnh phân tích tài liệu đã được gửi thành công，Chuẩn bị đồng bộ hóa trạng thái thư viện bóng cục bộ，datasetId: {}, documentIds: {}", datasetId, documentIds);
                // Sau khi lệnh thành công, trạng thái bóng cục bộ ngay lập tức được cập nhật thành CHẠY và Phân tích cú pháp (1) để đảm bảo danh sách Local-First có thể được phản hồi ngay lập tức
                documentDao.update(null, new UpdateWrapper<DocumentEntity>()
                        .set("run", "RUNNING")
                        .set("status", "1")
                        .set("updated_at", new Date())
                        .eq("dataset_id", datasetId)
                        .in("document_id", documentIds));

                log.info("Trạng thái cục bộ của tài liệu đã được cập nhật thành RUNNING");
            } else {
                log.error("Phân tích tài liệu không thành công，datasetId: {}, documentIds: {}", datasetId, documentIds);
                throw new RenException(ErrorCode.RAG_API_ERROR, "Phân tích tài liệu không thành công");
            }

            return result;

        } catch (Exception e) {
            log.error("Không thể phân tích tài liệu: {}", e.getMessage(), e);
            String errorMessage = e.getMessage() != null ? e.getMessage() : "null";
            if (e instanceof RenException) {
                throw (RenException) e;
            }
            throw new RenException(ErrorCode.RAG_API_ERROR, errorMessage);
        } finally {
            log.info("=== Hoạt động phân tích tài liệu kết thúc ===");
        }
    }

    @Override
    public ChunkDTO.ListVO listChunks(String datasetId, String documentId, ChunkDTO.ListReq req) {
        if (StringUtils.isBlank(datasetId) || StringUtils.isBlank(documentId)) {
            throw new RenException(ErrorCode.RAG_DATASET_ID_AND_MODEL_ID_NOT_NULL);
        }

        log.info("=== Bắt đầu liệt kê các lát: datasetId={}, documentId={}, req={} ===", datasetId, documentId, req);

        try {
            Map<String, Object> ragConfig = knowledgeBaseService.getRAGConfigByDatasetId(datasetId);
            KnowledgeBaseAdapter adapter = KnowledgeBaseAdapterFactory.getAdapter(extractAdapterType(ragConfig),
                    ragConfig);

            ChunkDTO.ListVO result = adapter.listChunks(datasetId, documentId, req);
            log.info("Danh sách lát thu được thành công: datasetId={}, total={}", datasetId, result.getTotal());
            return result;
        } catch (Exception e) {
            log.error("Không thể liệt kê các lát: {}", e.getMessage(), e);
            String errorMessage = e.getMessage() != null ? e.getMessage() : "null";
            if (e instanceof RenException) {
                throw (RenException) e;
            }
            throw new RenException(ErrorCode.RAG_API_ERROR, errorMessage);
        } finally {
            log.info("=== Kết thúc thao tác cắt lát danh sách ===");
        }
    }

    @Override
    public RetrievalDTO.ResultVO retrievalTest(RetrievalDTO.TestReq req) {
        if (CollectionUtils.isEmpty(req.getDatasetIds())) {
            throw new RenException("Cơ sở kiến thức để kiểm tra thu hồi không được chỉ định");
        }

        log.info("=== Bắt đầu thử nghiệm thu hồi: req={} ===", req);

        try {
            Map<String, Object> ragConfig = knowledgeBaseService.getRAGConfigByDatasetId(req.getDatasetIds().get(0));
            KnowledgeBaseAdapter adapter = KnowledgeBaseAdapterFactory.getAdapter(extractAdapterType(ragConfig),
                    ragConfig);

            RetrievalDTO.ResultVO result = adapter.retrievalTest(req);
            log.info("Thu hồi thử nghiệm thành công: total={}", result != null ? result.getTotal() : 0);
            return result;
        } catch (Exception e) {
            log.error("Kiểm tra thu hồi không thành công: {}", e.getMessage(), e);
            String errorMessage = e.getMessage() != null ? e.getMessage() : "null";
            if (e instanceof RenException) {
                throw (RenException) e;
            }
            throw new RenException(ErrorCode.RAG_API_ERROR, errorMessage);
        } finally {
            log.info("=== Hoạt động thử nghiệm thu hồi đã kết thúc ===");
        }
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void deleteDocumentsByDatasetId(String datasetId) {
        log.info("Tài liệu về tập dữ liệu sạch Cascade: datasetId={}", datasetId);
        List<DocumentEntity> list = documentDao
                .selectList(new QueryWrapper<DocumentEntity>().eq("dataset_id", datasetId));
        if (list == null || list.isEmpty())
            return;

        List<String> docIds = list.stream().map(DocumentEntity::getDocumentId).toList();

        // Gói gọi logic xóa hiện có (bao gồm cả xóa vật lý RAG)
        DocumentDTO.BatchIdReq req = DocumentDTO.BatchIdReq.builder().ids(docIds).build();
        this.deleteDocuments(datasetId, req);
    }

    @Override
    public int syncDocumentsFromRAG(String datasetId) {
        log.info("=== bắt đầu từRAGFlowĐồng bộ hóa tất cả tài liệu vào bảng bóng cục bộ: datasetId={} ===", datasetId);

        // 1. Lấy bộ chuyển đổi
        Map<String, Object> ragConfig = knowledgeBaseService.getRAGConfigByDatasetId(datasetId);
        KnowledgeBaseAdapter adapter = KnowledgeBaseAdapterFactory.getAdapter(extractAdapterType(ragConfig), ragConfig);

        // 2. Kéo tất cả tài liệu từ xa trong các trang
        List<KnowledgeFilesDTO> allRemoteDocs = new ArrayList<>();
        int pageNum = 1;
        int pageSize = 100;
        long totalRemote = Long.MAX_VALUE;

        while ((long) (pageNum - 1) * pageSize < totalRemote) {
            DocumentDTO.ListReq req = DocumentDTO.ListReq.builder()
                    .page(pageNum)
                    .pageSize(pageSize)
                    .build();
            PageData<KnowledgeFilesDTO> remotePage = adapter.getDocumentList(datasetId, req);
            if (remotePage == null || remotePage.getList() == null || remotePage.getList().isEmpty()) {
                break;
            }
            allRemoteDocs.addAll(remotePage.getList());
            totalRemote = remotePage.getTotal();
            pageNum++;
        }

        // 3. Nhận tài liệu hiện có tại địa phương
        List<DocumentEntity> localDocs = documentDao.selectList(
                new QueryWrapper<DocumentEntity>().eq("dataset_id", datasetId));
        Set<String> localDocIds = localDocs.stream()
                .map(DocumentEntity::getDocumentId)
                .collect(Collectors.toSet());

        // 4. Thu thập ID tài liệu từ xa
        Set<String> remoteDocIds = allRemoteDocs.stream()
                .map(KnowledgeFilesDTO::getDocumentId)
                .filter(id -> id != null)
                .collect(Collectors.toSet());

        // 5. Bổ sung: Chèn tài liệu tồn tại từ xa nhưng bị thiếu cục bộ
        List<KnowledgeFilesDTO> newDocs = allRemoteDocs.stream()
                .filter(doc -> doc.getDocumentId() != null && !localDocIds.contains(doc.getDocumentId()))
                .collect(Collectors.toList());

        int syncCount = 0;
        if (!newDocs.isEmpty()) {
            for (KnowledgeFilesDTO doc : newDocs) {
                try {
                    self.saveDocumentShadow(datasetId, doc, doc.getName(), doc.getChunkMethod(), doc.getParserConfig());
                    // Đồng bộ hóa số liệu thống kê mã thông báo/khối hiện có ở đầu từ xa
                    Long tokenCount = doc.getTokenCount() != null ? doc.getTokenCount() : 0L;
                    long chunkCount = doc.getChunkCount() != null ? doc.getChunkCount().longValue() : 0L;
                    if (tokenCount > 0 || chunkCount > 0) {
                        knowledgeBaseService.updateStatistics(datasetId, 0, chunkCount, tokenCount);
                    }
                    syncCount++;
                } catch (Exception e) {
                    log.warn("Đồng bộ hóa các bản ghi bóng tài liệu đơn không thành công: docId={}, error={}", doc.getDocumentId(), e.getMessage());
                }
            }
            log.info("từRAGFlowThêm đồng bộ hóa {} bản ghi bóng tài liệu, datasetId={}", syncCount, datasetId);
        }

        // 6. Dọn dẹp: Xóa các bản ghi bóng không còn tồn tại ở đầu từ xa nhưng vẫn được giữ lại cục bộ.
        List<DocumentEntity> deletedDocs = localDocs.stream()
                .filter(entity -> !remoteDocIds.contains(entity.getDocumentId()))
                .collect(Collectors.toList());

        if (!deletedDocs.isEmpty()) {
            List<String> deletedDocIds = new ArrayList<>();
            long totalChunkDelta = 0;
            long totalTokenDelta = 0;

            for (DocumentEntity entity : deletedDocs) {
                deletedDocIds.add(entity.getDocumentId());
                totalChunkDelta += entity.getChunkCount() != null ? entity.getChunkCount() : 0L;
                totalTokenDelta += entity.getTokenCount() != null ? entity.getTokenCount() : 0L;
            }
            try {
                self.deleteDocumentShadows(deletedDocIds, datasetId, totalChunkDelta, totalTokenDelta);
                log.info("Dọn dẹp các bản ghi bóng đã xóa từ xa: {} một, datasetId={}", deletedDocs.size(), datasetId);
            } catch (Exception e) {
                log.warn("Không thể dọn sạch các bản ghi bóng đã xóa từ xa: datasetId={}, error={}", datasetId, e.getMessage());
            }
        }

        // 7. Cập nhật đầy đủ: Đối với các tài liệu tồn tại cả từ xa và cục bộ, tất cả các trường sẽ được đồng bộ hóa dựa trên đầu từ xa.
        // Xử lý việc truyền lại documentId tái sử dụng RAGFlow, thay đổi siêu dữ liệu sau khi chỉnh sửa từ xa, v.v.
        Map<String, KnowledgeFilesDTO> remoteDocMap = allRemoteDocs.stream()
                .filter(doc -> doc.getDocumentId() != null)
                .collect(Collectors.toMap(KnowledgeFilesDTO::getDocumentId, doc -> doc, (a, b) -> b));

        Map<String, DocumentEntity> localDocMap = localDocs.stream()
                .collect(Collectors.toMap(DocumentEntity::getDocumentId, e -> e, (a, b) -> b));

        int updateCount = 0;
        for (Map.Entry<String, KnowledgeFilesDTO> entry : remoteDocMap.entrySet()) {
            String docId = entry.getKey();
            DocumentEntity local = localDocMap.get(docId);
            if (local == null) {
                continue; // không phải địa phương，từng bước5Quy trình
            }
            KnowledgeFilesDTO remote = entry.getValue();

            // Cập nhật toàn bộ trường (tùy thuộc vào đầu từ xa) để đảm bảo rằng cục bộ và RAGFlow hoàn toàn nhất quán
            UpdateWrapper<DocumentEntity> updateWrapper = new UpdateWrapper<DocumentEntity>()
                    .set("run", remote.getRun())
                    .set("status", remote.getStatus() != null ? remote.getStatus() : local.getStatus())
                    .set("progress", remote.getProgress())
                    .set("chunk_count", remote.getChunkCount())
                    .set("token_count", remote.getTokenCount())
                    .set("size", remote.getFileSize())
                    .set("error", remote.getError())
                    .set("process_duration", remote.getProcessDuration())
                    .set("updated_at", new Date())
                    .set("last_sync_at", new Date())
                    .eq("document_id", docId)
                    .eq("dataset_id", datasetId);

            if (remote.getName() != null) {
                updateWrapper.set("name", remote.getName());
            }
            if (remote.getThumbnail() != null) {
                updateWrapper.set("thumbnail", remote.getThumbnail());
            }
            if (remote.getMetaFields() != null) {
                try {
                    updateWrapper.set("meta_fields", objectMapper.writeValueAsString(remote.getMetaFields()));
                } catch (Exception e) {
                    log.warn("Tuần tự hóa siêu dữ liệu cập nhật đồng bộ không thành công: docId={}, error={}", docId, e.getMessage());
                }
            }

            documentDao.update(null, updateWrapper);

            // Đồng bộ hóa các khác biệt thống kê (sửa bảng cha khi số lượng khối/mã thông báo thay đổi)
            Long remoteTokenCount = remote.getTokenCount() != null ? remote.getTokenCount() : 0L;
            Long localTokenCount = local.getTokenCount() != null ? local.getTokenCount() : 0L;
            long remoteChunkCount = remote.getChunkCount() != null ? remote.getChunkCount().longValue() : 0L;
            long localChunkCount = local.getChunkCount() != null ? local.getChunkCount().longValue() : 0L;
            long tokenDelta = remoteTokenCount - localTokenCount;
            long chunkDelta = remoteChunkCount - localChunkCount;
            if (tokenDelta != 0 || chunkDelta != 0) {
                knowledgeBaseService.updateStatistics(datasetId, 0, chunkDelta, tokenDelta);
                log.info("cập nhật bóng: Thống kê cơ sở kiến thức chính xác, docId={}, chunkDelta={}, tokenDelta={}", docId, chunkDelta, tokenDelta);
            }

            updateCount++;
        }

        if (syncCount == 0 && deletedDocs.isEmpty() && updateCount == 0) {
            log.info("Bảng bóng cục bộ đã được liên kết vớiRAGFlowĐồng bộ hóa hoàn toàn, datasetId={}", datasetId);
        } else {
            log.info("Đồng bộ hóa đã hoàn tất: Mới={}, dọn dẹp={}, cập nhật={}, datasetId={}", syncCount, deletedDocs.size(), updateCount, datasetId);
        }

        return syncCount;
    }

    @Override
    public void syncRunningDocuments() {
        // 1. Truy vấn tất cả tài liệu ở trạng thái ĐANG CHẠY
        List<DocumentEntity> runningDocs = documentDao.selectList(
                new QueryWrapper<DocumentEntity>()
                        .eq("run", "RUNNING")
                        .eq("status", "1") // Chỉ đồng bộ hóa các tài liệu đã bật
        );

        if (runningDocs == null || runningDocs.isEmpty()) {
            return;
        }

        log.info("nhiệm vụ theo lịch trình: khám phá {} tài liệu đang được phân tích，Bắt đầu đồng bộ hóa...", runningDocs.size());

        // 2. Nhóm theo DatasetID và tái sử dụng Adaptor
        Map<String, List<DocumentEntity>> groupedDocs = runningDocs.stream()
                .collect(Collectors.groupingBy(DocumentEntity::getDatasetId));

        groupedDocs.forEach((datasetId, docs) -> {
            KnowledgeBaseAdapter adapter = null;
            try {
                // Khởi tạo Adapter (chỉ khởi tạo một lần cho mỗi tập dữ liệu)
                Map<String, Object> ragConfig = knowledgeBaseService.getRAGConfigByDatasetId(datasetId);
                adapter = KnowledgeBaseAdapterFactory.getAdapter(extractAdapterType(ragConfig), ragConfig);
            } catch (Exception e) {
                log.warn("Không thể tạo tập dữ liệu {} Khởi tạo bộ chuyển đổi，Bỏ qua đồng bộ hóa: {}", datasetId, e.getMessage());
                return;
            }

            for (DocumentEntity doc : docs) {
                try {
                    // Xây dựng một DTO tạm thời và chuyển nó sang phương thức đồng bộ hóa
                    KnowledgeFilesDTO dto = convertEntityToDTO(doc);
                    // Ghi lại số lượng Token trước khi đồng bộ
                    Long oldTokenCount = dto.getTokenCount() != null ? dto.getTokenCount() : 0L;

                    syncDocumentStatusWithRAG(dto, adapter);

                    // 3. [Sửa phím] Tính delta và cập nhật số liệu thống kê cơ sở kiến thức
                    Long newTokenCount = dto.getTokenCount() != null ? dto.getTokenCount() : 0L;
                    Long tokenDelta = newTokenCount - oldTokenCount;

                    // Chỉ cập nhật số liệu thống kê khi trạng thái thay đổi thành THÀNH CÔNG và số lượng Token thay đổi
                    if (tokenDelta != 0) {
                        knowledgeBaseService.updateStatistics(datasetId, 0, 0L, tokenDelta);
                        log.info("nhiệm vụ theo lịch trình: Thống kê cơ sở kiến thức chính xác đồng bộ, docId={}, tokenDelta={}", dto.getDocumentId(), tokenDelta);
                    }
                } catch (Exception e) {
                    log.error("Đồng bộ hóa tài liệu {} thất bại: {}", doc.getDocumentId(), e.getMessage());
                }
            }
        });
    }
}