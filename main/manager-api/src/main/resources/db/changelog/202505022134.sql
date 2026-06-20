-- Khởi tạo lịch sử trò chuyện của tổng đài viên
DROP TABLE IF EXISTS ai_chat_history;
DROP TABLE IF EXISTS ai_chat_message;
DROP TABLE IF EXISTS ai_agent_chat_history;
CREATE TABLE ai_agent_chat_history
(
    id          BIGINT AUTO_INCREMENT COMMENT 'khóa chínhID' PRIMARY KEY,
    mac_address VARCHAR(50) COMMENT 'MACđịa chỉ',
    agent_id VARCHAR(32) COMMENT 'đại lýid',
    session_id  VARCHAR(50) COMMENT 'phiênID',
    chat_type   TINYINT(3) COMMENT 'Loại tin nhắn: 1-người dùng, 2-đại lý',
    content     VARCHAR(1024) COMMENT 'Nội dung trò chuyện',
    audio_id    VARCHAR(32) COMMENT 'Âm thanhID',
    created_at  DATETIME(3) DEFAULT CURRENT_TIMESTAMP(3) NOT NULL COMMENT 'thời gian sáng tạo',
    updated_at  DATETIME(3) DEFAULT CURRENT_TIMESTAMP(3) NOT NULL ON UPDATE CURRENT_TIMESTAMP(3) COMMENT 'Thời gian cập nhật',
    INDEX idx_ai_agent_chat_history_mac (mac_address),
    INDEX idx_ai_agent_chat_history_session_id (session_id),
    INDEX idx_ai_agent_chat_history_agent_id (agent_id),
    INDEX idx_ai_agent_chat_history_agent_session_created (agent_id, session_id, created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT 'Bảng ghi cuộc trò chuyện của đại lý';

DROP TABLE IF EXISTS ai_agent_chat_audio;
CREATE TABLE ai_agent_chat_audio
(
    id          VARCHAR(32) COMMENT 'khóa chínhID' PRIMARY KEY,
    audio       LONGBLOB COMMENT 'Âm thanhopusdữ liệu'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT 'Bảng dữ liệu âm thanh trò chuyện của đại lý'; 