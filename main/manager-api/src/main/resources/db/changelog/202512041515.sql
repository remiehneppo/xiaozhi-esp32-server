-- liquibase formatted sql

-- changeset xiaozhi:202512041515
CREATE TABLE ai_agent_context_provider (
    id VARCHAR(32) NOT NULL COMMENT 'khóa chính',
    agent_id VARCHAR(32) NOT NULL COMMENT 'đại lýID',
    context_providers JSON COMMENT 'Cấu hình nguồn ngữ cảnh',
    creator BIGINT COMMENT 'Người sáng tạo',
    created_at DATETIME COMMENT 'thời gian sáng tạo',
    updater BIGINT COMMENT 'Trình cập nhật',
    updated_at DATETIME COMMENT 'Thời gian cập nhật',
    PRIMARY KEY (id),
    INDEX idx_agent_id (agent_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Bảng cấu hình nguồn ngữ cảnh của tác nhân';
