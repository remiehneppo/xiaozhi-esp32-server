-- Sửa đổi loại trường nội dung trò chuyện
ALTER TABLE ai_agent_chat_history MODIFY COLUMN content TEXT COMMENT 'Nội dung trò chuyện';
