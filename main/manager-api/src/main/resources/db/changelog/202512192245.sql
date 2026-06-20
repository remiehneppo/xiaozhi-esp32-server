-- Thêm chỉ mục ID âm thanh vào lịch sử trò chuyện của tổng đài viên
ALTER TABLE ai_agent_chat_history ADD INDEX idx_ai_agent_chat_history_audio_id (audio_id);
