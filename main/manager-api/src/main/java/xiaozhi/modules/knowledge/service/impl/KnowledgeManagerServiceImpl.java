package xiaozhi.modules.knowledge.service.impl;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import xiaozhi.modules.knowledge.service.KnowledgeBaseService;
import xiaozhi.modules.knowledge.service.KnowledgeFilesService;
import xiaozhi.modules.knowledge.service.KnowledgeManagerService;

import java.util.List;

@Service
@Slf4j
@RequiredArgsConstructor
public class KnowledgeManagerServiceImpl implements KnowledgeManagerService {

    private final KnowledgeBaseService knowledgeBaseService;
    private final KnowledgeFilesService knowledgeFilesService;

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void deleteDatasetWithFiles(String datasetId) {
        log.info("=== Quá trình xóa xếp tầng bắt đầu: datasetId={} ===", datasetId);

        // 1. Trước tiên, hãy gọi dịch vụ tệp để dọn sạch tất cả các bản ghi tài liệu trong tập dữ liệu (bao gồm cả phía RAGFlow)
        log.info("Step 1: Dọn dẹp các tài liệu liên quan...");
        knowledgeFilesService.deleteDocumentsByDatasetId(datasetId);

        // 2. Gọi lại dịch vụ cơ sở tri thức để đăng xuất hoàn toàn bộ dữ liệu (bao gồm cả bên RAGFlow)
        log.info("Step 2: Xóa chủ đề tập dữ liệu...");
        knowledgeBaseService.deleteByDatasetId(datasetId);

        log.info("=== Xóa tầng thành công: datasetId={} ===", datasetId);
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void batchDeleteDatasetsWithFiles(List<String> datasetIds) {
        if (datasetIds == null || datasetIds.isEmpty())
            return;
        log.info("=== Việc xóa tầng hàng loạt bắt đầu: count={} ===", datasetIds.size());
        for (String id : datasetIds) {
            deleteDatasetWithFiles(id);
        }
    }
}
