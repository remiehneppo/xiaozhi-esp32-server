-- bảng cơ sở kiến thức
DROP TABLE IF EXISTS `ai_rag_dataset`;
CREATE TABLE `ai_rag_dataset` (
    `id` VARCHAR(32) NOT NULL COMMENT 'mã định danh duy nhất',
    `dataset_id` VARCHAR(64) NOT NULL COMMENT 'cơ sở tri thứcID',
    `rag_model_id` VARCHAR(64) COMMENT 'RAGCấu hình mô hìnhID',
    `name` VARCHAR(100) NOT NULL COMMENT 'Tên cơ sở kiến thức',
    `description` TEXT COMMENT 'Mô tả cơ sở kiến thức',
    `status` TINYINT(1) DEFAULT 1 COMMENT 'Trạng thái：0vô hiệu hóa 1kích hoạt',
    `creator` BIGINT COMMENT 'Người sáng tạo',
    `created_at` DATETIME COMMENT 'thời gian sáng tạo',
    `updater` BIGINT COMMENT 'Trình cập nhật',
    `updated_at` DATETIME COMMENT 'Thời gian cập nhật',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_dataset_id` (`dataset_id`),
    INDEX `idx_ai_rag_dataset_status` (`status`),
    INDEX `idx_ai_rag_dataset_creator` (`creator`),
    INDEX `idx_ai_rag_dataset_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='bảng cơ sở kiến thức';