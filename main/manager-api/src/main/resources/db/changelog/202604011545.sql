-- Thêm trường ID mẫu nhỏ vào bảng thân thông minh
SET @col_exists = (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'ai_agent' AND COLUMN_NAME = 'slm_model_id');
SET @sql = IF(@col_exists = 0, 'ALTER TABLE `ai_agent` ADD COLUMN `slm_model_id` VARCHAR(255) NULL COMMENT ''mô hình nhỏID'' AFTER `llm_model_id`', 'SELECT ''Column slm_model_id already exists'' AS msg');
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

-- Tạo bảng tiêu đề trò chuyện
DROP TABLE IF EXISTS `ai_agent_chat_title`;
CREATE TABLE `ai_agent_chat_title` (
    `id` VARCHAR(32) NOT NULL COMMENT 'khóa chínhID',
    `session_id` VARCHAR(255) NOT NULL COMMENT 'phiênID',
    `title` VARCHAR(255) DEFAULT NULL COMMENT 'Tiêu đề trò chuyện',
    `created_at` DATETIME DEFAULT NULL COMMENT 'thời gian sáng tạo',
    `updated_at` DATETIME DEFAULT NULL COMMENT 'Thời gian cập nhật',
    PRIMARY KEY (`id`),
    KEY `idx_session_id` (`session_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Bảng tiêu đề trò chuyện của đại lý';
