package xiaozhi.modules.knowledge.controller;

import java.util.List;
import java.util.Map;

import org.apache.shiro.authz.annotation.RequiresPermissions;
import org.springdoc.core.annotations.ParameterObject;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.AllArgsConstructor;
import xiaozhi.common.exception.ErrorCode;
import xiaozhi.common.exception.RenException;
import xiaozhi.common.page.PageData;
import xiaozhi.common.utils.Result;
import xiaozhi.modules.knowledge.dto.KnowledgeBaseDTO;
import xiaozhi.modules.knowledge.dto.KnowledgeFilesDTO;
import xiaozhi.modules.knowledge.dto.document.ChunkDTO;
import xiaozhi.modules.knowledge.dto.document.DocumentDTO;
import xiaozhi.modules.knowledge.dto.document.RetrievalDTO;
import xiaozhi.modules.knowledge.service.KnowledgeBaseService;
import xiaozhi.modules.knowledge.service.KnowledgeFilesService;
import xiaozhi.modules.security.user.SecurityUser;

@AllArgsConstructor
@RestController
@RequestMapping("/datasets/{dataset_id}")
@Tag(name = "Quản lý tài liệu cơ sở tri thức")
public class KnowledgeFilesController {

    private final KnowledgeFilesService knowledgeFilesService;
    private final KnowledgeBaseService knowledgeBaseService;

    /**
     * Xác minh xem người dùng hiện tại có được phép vận hành cơ sở kiến thức đã chỉ định hay không
     *
     * @paramdatadataID cơ sở kiến thức ID
     */
    private void validateKnowledgeBasePermission(String datasetId) {
        // Lấy ID người dùng đã đăng nhập hiện tại
        Long currentUserId = SecurityUser.getUserId();

        // Nhận thông tin cơ sở kiến thức
        KnowledgeBaseDTO knowledgeBase = knowledgeBaseService.getByDatasetId(datasetId);

        // Kiểm tra quyền: Người dùng chỉ có thể vận hành cơ sở tri thức do chính họ tạo ra
        if (knowledgeBase.getCreator() == null || !knowledgeBase.getCreator().equals(currentUserId)) {
            throw new RenException(ErrorCode.NO_PERMISSION);
        }
    }

    @GetMapping("/documents")
    @Operation(summary = "Truy vấn danh sách tài liệu theo trang")
    @RequiresPermissions("sys:role:normal")
    public Result<PageData<KnowledgeFilesDTO>> getPageList(
            @PathVariable("dataset_id") String datasetId,
            @RequestParam(required = false) String name,
            @RequestParam(required = false) String status,
            @RequestParam(required = false, defaultValue = "1") Integer page,
            @RequestParam(required = false, defaultValue = "10") Integer page_size) {
        // Xác minh quyền cơ sở kiến thức
        validateKnowledgeBasePermission(datasetId);

        // Thông số lắp ráp
        KnowledgeFilesDTO knowledgeFilesDTO = new KnowledgeFilesDTO();
        knowledgeFilesDTO.setDatasetId(datasetId);
        knowledgeFilesDTO.setName(name);
        knowledgeFilesDTO.setStatus(status);
        PageData<KnowledgeFilesDTO> pageData = knowledgeFilesService.getPageList(knowledgeFilesDTO, page, page_size);
        return new Result<PageData<KnowledgeFilesDTO>>().ok(pageData);
    }

    @GetMapping("/documents/status/{status}")
    @Operation(summary = "Truy vấn danh sách tài liệu theo trạng thái trang")
    @RequiresPermissions("sys:role:normal")
    public Result<PageData<KnowledgeFilesDTO>> getPageListByStatus(
            @PathVariable("dataset_id") String datasetId,
            @PathVariable("status") String status,
            @RequestParam(required = false, defaultValue = "1") Integer page,
            @RequestParam(required = false, defaultValue = "10") Integer page_size) {
        // Xác minh quyền cơ sở kiến thức
        validateKnowledgeBasePermission(datasetId);
        // Thông số lắp ráp
        KnowledgeFilesDTO knowledgeFilesDTO = new KnowledgeFilesDTO();
        knowledgeFilesDTO.setDatasetId(datasetId);
        knowledgeFilesDTO.setStatus(status);
        PageData<KnowledgeFilesDTO> pageData = knowledgeFilesService.getPageList(knowledgeFilesDTO, page, page_size);
        return new Result<PageData<KnowledgeFilesDTO>>().ok(pageData);
    }

    @PostMapping("/documents")
    @Operation(summary = "Tải tài liệu lên cơ sở tri thức")
    @RequiresPermissions("sys:role:normal")
    public Result<KnowledgeFilesDTO> uploadDocument(
            @PathVariable("dataset_id") String datasetId,
            @RequestParam("file") MultipartFile file,
            @RequestParam(required = false) String name,
            @RequestParam(required = false) String chunkMethod,
            @RequestParam(required = false) String metaFields,
            @RequestParam(required = false) String parserConfig) {

        // Xác minh quyền cơ sở kiến thức
        validateKnowledgeBasePermission(datasetId);

        KnowledgeFilesDTO resp = knowledgeFilesService.uploadDocument(datasetId, file, name,
                metaFields != null ? parseJsonMap(metaFields) : null,
                chunkMethod,
                parserConfig != null ? parseJsonMap(parserConfig) : null);
        return new Result<KnowledgeFilesDTO>().ok(resp);
    }

    @DeleteMapping("/documents")
    @Operation(summary = "Xóa tài liệu theo đợt")
    @RequiresPermissions("sys:role:normal")
    public Result<Void> delete(@PathVariable("dataset_id") String datasetId,
            @RequestBody DocumentDTO.BatchIdReq req) {
        // Xác minh quyền cơ sở kiến thức
        validateKnowledgeBasePermission(datasetId);

        knowledgeFilesService.deleteDocuments(datasetId, req);
        return new Result<>();
    }

    @DeleteMapping("/documents/{document_id}")
    @Operation(summary = "Xóa một tài liệu")
    @RequiresPermissions("sys:role:normal")
    public Result<Void> deleteSingle(@PathVariable("dataset_id") String datasetId,
            @PathVariable("document_id") String documentId) {
        // Xác minh quyền cơ sở kiến thức
        validateKnowledgeBasePermission(datasetId);

        DocumentDTO.BatchIdReq req = new DocumentDTO.BatchIdReq();
        req.setIds(java.util.Collections.singletonList(documentId));
        knowledgeFilesService.deleteDocuments(datasetId, req);
        return new Result<>();
    }

    @PostMapping("/chunks")
    @Operation(summary = "Phân tích tài liệu（Cắt thành từng miếng）")
    @RequiresPermissions("sys:role:normal")
    public Result<Void> parseDocuments(@PathVariable("dataset_id") String datasetId,
            @RequestBody Map<String, List<String>> requestBody) {
        // Xác minh quyền cơ sở kiến thức
        validateKnowledgeBasePermission(datasetId);

        List<String> documentIds = requestBody.get("document_ids");
        if (documentIds == null || documentIds.isEmpty()) {
            return new Result<Void>().error("document_idsTham số không được để trống");
        }

        boolean success = knowledgeFilesService.parseDocuments(datasetId, documentIds);
        if (success) {
            return new Result<Void>();
        } else {
            return new Result<Void>().error("Phân tích tài liệu không thành công，Tài liệu có thể đang được xử lý");
        }
    }

    @GetMapping("/documents/{document_id}/chunks")
    @Operation(summary = "Liệt kê các lát của tài liệu được chỉ định")
    @RequiresPermissions("sys:role:normal")
    public Result<ChunkDTO.ListVO> listChunks(
            @PathVariable("dataset_id") String datasetId,
            @PathVariable("document_id") String documentId,
            @RequestParam(name = "page", required = false, defaultValue = "1") Integer page,
            @RequestParam(name = "page_size", required = false, defaultValue = "10") Integer pageSize,
            @RequestParam(required = false) String keywords,
            @RequestParam(required = false) String id) {

        // Xác minh quyền (xác minh sự tồn tại của cơ sở kiến thức và xác minh quyền sở hữu được bao gồm trong nội bộ)
        validateKnowledgeBasePermission(datasetId);

        // Xây dựng đối tượng yêu cầu
        ChunkDTO.ListReq req = ChunkDTO.ListReq.builder()
                .page(page)
                .pageSize(pageSize)
                .keywords(keywords)
                .id(id)
                .build();

        // Gọi lớp dịch vụ để lấy danh sách lát cắt được định kiểu mạnh
        ChunkDTO.ListVO result = knowledgeFilesService.listChunks(datasetId, documentId, req);
        return new Result<ChunkDTO.ListVO>().ok(result);
    }

    @PostMapping("/retrieval-test")
    @Operation(summary = "kiểm tra thu hồi")
    @RequiresPermissions("sys:role:normal")
    public Result<RetrievalDTO.ResultVO> retrievalTest(
            @PathVariable("dataset_id") String datasetId,
            @RequestBody RetrievalDTO.TestReq req) {

        // Xác minh quyền cơ sở kiến thức
        validateKnowledgeBasePermission(datasetId);

        // Logic chìm nghiệp vụ: Nếu ID cơ sở kiến thức không được chỉ định, nó sẽ được đặt thành Id tập dữ liệu trong đường dẫn hiện tại.
        if (req.getDatasetIds() == null || req.getDatasetIds().isEmpty()) {
            req.setDatasetIds(java.util.Arrays.asList(datasetId));
        }

        // [Củng cố] Kiểm soát mạnh mẽ các thông số phân trang để ngăn ngừa lỗi Negative Slicing ở phía RAGFlow
        if (req.getPage() == null || req.getPage() < 1) {
            req.setPage(1);
        }
        if (req.getPageSize() == null || req.getPageSize() < 1) {
            req.setPageSize(100);
        }

        // Gọi dịch vụ truy xuất và trả về một đối tượng tổng hợp được định kiểu mạnh
        RetrievalDTO.ResultVO result = knowledgeFilesService.retrievalTest(req);
        return new Result<RetrievalDTO.ResultVO>().ok(result);
    }

    /**
     * Phân tích chuỗi JSON thành đối tượng Map
     */
    private Map<String, Object> parseJsonMap(String jsonString) {
        try {
            ObjectMapper objectMapper = new ObjectMapper();
            return objectMapper.readValue(jsonString, new TypeReference<Map<String, Object>>() {
            });
        } catch (Exception e) {
            throw new RuntimeException("phân tích cú phápJSONchuỗi thất bại: " + jsonString, e);
        }
    }
}