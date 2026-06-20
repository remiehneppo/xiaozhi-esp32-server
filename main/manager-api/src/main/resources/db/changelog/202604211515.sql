-- Danh sách file word thay thế đại lý
CREATE TABLE IF NOT EXISTS `ai_agent_correct_word_file` (
    `id`          VARCHAR(32)  NOT NULL,
    `file_name`   VARCHAR(256) NOT NULL COMMENT 'tên tập tin gốc',
    `word_count`  INT          NOT NULL DEFAULT 0 COMMENT 'Số từ thay thế',
    `content`     TEXT         COMMENT 'Nội dung gốc của tập tin',
    `creator`     BIGINT       DEFAULT NULL,
    `created_at`  DATETIME     DEFAULT CURRENT_TIMESTAMP,
    `updater`     BIGINT       DEFAULT NULL,
    `updated_at`  DATETIME     DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    INDEX `idx_creator` (`creator`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='tập tin từ thay thế';

-- Danh sách nhập từ thay thế
CREATE TABLE IF NOT EXISTS `ai_agent_correct_word_item` (
    `id`          VARCHAR(32)  NOT NULL,
    `file_id`     VARCHAR(32)  NOT NULL COMMENT 'Tập tin thuộc vềID',
    `source_word` VARCHAR(128) NOT NULL COMMENT 'từ gốc',
    `target_word` VARCHAR(128) NOT NULL COMMENT 'từ thay thế',
    PRIMARY KEY (`id`),
    INDEX `idx_file_id` (`file_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Mục nhập từ thay thế';

-- Bảng liên kết tệp từ thay thế tác nhân
CREATE TABLE IF NOT EXISTS `ai_agent_correct_word_mapping` (
    `id`          VARCHAR(32)  NOT NULL,
    `agent_id`    VARCHAR(32)  NOT NULL,
    `file_id`     VARCHAR(32)  NOT NULL,
    `creator`     BIGINT       DEFAULT NULL,
    `created_at`  DATETIME     DEFAULT CURRENT_TIMESTAMP,
    `updater`     BIGINT       DEFAULT NULL,
    `updated_at`  DATETIME     DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE INDEX `uk_agent_file` (`agent_id`, `file_id`),
    INDEX `idx_agent_id` (`agent_id`),
    INDEX `idx_file_id` (`file_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Liên kết tập tin từ thay thế đại lý';
