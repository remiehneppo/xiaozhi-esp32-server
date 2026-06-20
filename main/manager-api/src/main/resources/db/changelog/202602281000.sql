-- bảng thẻ
CREATE TABLE IF NOT EXISTS ai_agent_tag (
    id VARCHAR(32) NOT NULL COMMENT 'khóa chính',
    tag_name VARCHAR(64) NOT NULL COMMENT 'Tên thẻ',
    sort INT UNSIGNED DEFAULT 0 COMMENT 'sắp xếp',
    creator BIGINT COMMENT 'Người sáng tạo',
    created_at DATETIME COMMENT 'thời gian sáng tạo',
    updater BIGINT COMMENT 'Trình cập nhật',
    updated_at DATETIME COMMENT 'Thời gian cập nhật',
    deleted TINYINT DEFAULT 0 COMMENT 'xóa dấu',
    PRIMARY KEY (id),
    UNIQUE KEY uk_tag_name (tag_name),
    INDEX idx_sort (sort)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Bảng thẻ đại lý';

-- Bảng liên kết thẻ tác nhân
CREATE TABLE IF NOT EXISTS ai_agent_tag_relation (
    id VARCHAR(32) NOT NULL COMMENT 'khóa chính',
    agent_id VARCHAR(32) NOT NULL COMMENT 'đại lýID',
    tag_id VARCHAR(32) NOT NULL COMMENT 'nhãnID',
    creator BIGINT COMMENT 'Người sáng tạo',
    created_at DATETIME COMMENT 'thời gian sáng tạo',
    updater BIGINT COMMENT 'Trình cập nhật',
    updated_at DATETIME COMMENT 'Thời gian cập nhật',
    PRIMARY KEY (id),
    UNIQUE KEY uk_agent_tag (agent_id, tag_id),
    INDEX idx_agent_id (agent_id),
    INDEX idx_tag_id (tag_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Bảng liên kết thẻ tác nhân';
