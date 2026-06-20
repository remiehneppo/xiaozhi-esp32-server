-- Thêm trường mới vào giọng nói của nhân viên
ALTER TABLE ai_agent_voice_print
    ADD COLUMN audio_id VARCHAR(32) NOT NULL COMMENT 'Âm thanhID';