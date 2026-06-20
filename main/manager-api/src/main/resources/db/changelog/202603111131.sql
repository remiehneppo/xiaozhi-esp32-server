-- Thêm các tham số được trả về bởi ragflow (được trả về khi tạo/truy vấn cơ sở kiến thức)
SET @col_exists = (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'ai_rag_dataset' AND COLUMN_NAME = 'tenant_id');
SET @sql = IF(@col_exists = 0, 'ALTER TABLE `ai_rag_dataset` ADD COLUMN `tenant_id` varchar(32) DEFAULT NULL COMMENT ''người thuê nhàID''', 'SELECT ''Column tenant_id already exists'' AS msg');
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_exists = (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'ai_rag_dataset' AND COLUMN_NAME = 'avatar');
SET @sql = IF(@col_exists = 0, 'ALTER TABLE `ai_rag_dataset` ADD COLUMN `avatar` text DEFAULT NULL COMMENT ''Hình đại diện cơ sở kiến thức (Base64)''', 'SELECT ''Column avatar already exists'' AS msg');
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_exists = (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'ai_rag_dataset' AND COLUMN_NAME = 'embedding_model');
SET @sql = IF(@col_exists = 0, 'ALTER TABLE `ai_rag_dataset` ADD COLUMN `embedding_model` varchar(50) DEFAULT NULL COMMENT ''Nhúng tên mẫu''', 'SELECT ''Column embedding_model already exists'' AS msg');
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_exists = (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'ai_rag_dataset' AND COLUMN_NAME = 'permission');
SET @sql = IF(@col_exists = 0, 'ALTER TABLE `ai_rag_dataset` ADD COLUMN `permission` varchar(20) DEFAULT ''me'' COMMENT ''Cài đặt quyền：me/team''', 'SELECT ''Column permission already exists'' AS msg');
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_exists = (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'ai_rag_dataset' AND COLUMN_NAME = 'chunk_method');
SET @sql = IF(@col_exists = 0, 'ALTER TABLE `ai_rag_dataset` ADD COLUMN `chunk_method` varchar(50) DEFAULT NULL COMMENT ''Phương pháp chia nhỏ''', 'SELECT ''Column chunk_method already exists'' AS msg');
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_exists = (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'ai_rag_dataset' AND COLUMN_NAME = 'parser_config');
SET @sql = IF(@col_exists = 0, 'ALTER TABLE `ai_rag_dataset` ADD COLUMN `parser_config` text DEFAULT NULL COMMENT ''Cấu hình trình phân tích cú pháp (JSON)''', 'SELECT ''Column parser_config already exists'' AS msg');
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_exists = (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'ai_rag_dataset' AND COLUMN_NAME = 'chunk_count');
SET @sql = IF(@col_exists = 0, 'ALTER TABLE `ai_rag_dataset` ADD COLUMN `chunk_count` bigint(20) DEFAULT 0 COMMENT ''Tổng số khối''', 'SELECT ''Column chunk_count already exists'' AS msg');
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_exists = (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'ai_rag_dataset' AND COLUMN_NAME = 'document_count');
SET @sql = IF(@col_exists = 0, 'ALTER TABLE `ai_rag_dataset` ADD COLUMN `document_count` bigint(20) DEFAULT 0 COMMENT ''Tổng số tài liệu''', 'SELECT ''Column document_count already exists'' AS msg');
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_exists = (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'ai_rag_dataset' AND COLUMN_NAME = 'token_num');
SET @sql = IF(@col_exists = 0, 'ALTER TABLE `ai_rag_dataset` ADD COLUMN `token_num` bigint(20) DEFAULT 0 COMMENT ''tổng cộng Token con số''', 'SELECT ''Column token_num already exists'' AS msg');
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

-- Bảng tài liệu (Shadow DB cho RAGFlow)
-- Giữ ID tài liệu và liên kết ID tài liệu từ xa ragflow với ID cục bộ (chỉ cần sao lưu liên kết thông tin meta, trên thực tế, nội dung tệp vẫn được lưu trữ trong ragflow)
DROP TABLE IF EXISTS `ai_rag_knowledge_document`;
CREATE TABLE `ai_rag_knowledge_document` (
     `id` varchar(36) NOT NULL COMMENT 'Chỉ địa phươngID',
     `dataset_id` varchar(36) NOT NULL COMMENT 'cơ sở tri thứcID (hiệp hội ai_rag_dataset)',
     `document_id` varchar(64) NOT NULL COMMENT 'RAGFlowTài liệuID (từ xaID)',
     `name` varchar(255) DEFAULT NULL COMMENT 'Tên tài liệu',
     `size` bigint(20) DEFAULT NULL COMMENT 'kích thước tập tin(Bytes)',
     `type` varchar(20) DEFAULT NULL COMMENT 'Loại tệp',
     `chunk_method` varchar(50) DEFAULT NULL COMMENT 'Phương pháp chia nhỏ',
     `parser_config` text COMMENT 'Cấu hình phân tích(JSON)',
     `status` varchar(10) DEFAULT '1' COMMENT 'Trạng thái sẵn có (1:kích hoạt 0:Vô hiệu hóa)',
     `run` varchar(32) DEFAULT 'UNSTART' COMMENT 'Trạng thái chạy (UNSTART/RUNNING/CANCEL/DONE/FAIL)',
     `progress` double DEFAULT '0' COMMENT 'Tiến trình phân tích cú pháp (0.0 ~ 1.0)',
     `thumbnail` mediumtext COMMENT 'hình thu nhỏ (Base64 hoặc URL)',
     `process_duration` double DEFAULT '0' COMMENT 'Phân tích cần có thời gian (đơn vị: giây)',
     `meta_fields` text COMMENT 'Siêu dữ liệu tùy chỉnh (JSON)',
     `source_type` varchar(32) DEFAULT 'local' COMMENT 'Loại nguồn (local, s3, url Đợi đã)',
     `error` text COMMENT 'thông báo lỗi',
     `chunk_count` int(11) DEFAULT '0' COMMENT 'Số lượng khối',
     `token_count` bigint(20) DEFAULT '0' COMMENT 'Tokensố lượng',
     `enabled` tinyint(1) DEFAULT '1' COMMENT 'Trạng thái đã bật',
     `creator` bigint(20) DEFAULT NULL COMMENT 'Người sáng tạo',
     `created_at` datetime DEFAULT NULL COMMENT 'thời gian sáng tạo',
     `updated_at` datetime DEFAULT NULL COMMENT 'Thời gian cập nhật',
     `last_sync_at` datetime DEFAULT NULL COMMENT 'Lần đồng bộ hóa cuối cùng',
     PRIMARY KEY (`id`),
     UNIQUE KEY `uk_doc_id` (`document_id`),
     KEY `idx_dataset_id` (`dataset_id`),
     KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Bảng tài liệu cơ sở kiến thức';