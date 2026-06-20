-- Thêm trường cấu hình bản ghi trò chuyện
ALTER TABLE `ai_agent` 
ADD COLUMN `chat_history_conf` tinyint NOT NULL DEFAULT 0 COMMENT 'Cấu hình lịch sử trò chuyện（0Không ghi lại 1Chỉ ghi lại văn bản 2Ghi lại văn bản và lời nói）' AFTER `system_prompt`;

ALTER TABLE `ai_agent_template` 
ADD COLUMN `chat_history_conf` tinyint NOT NULL DEFAULT 0 COMMENT 'Cấu hình lịch sử trò chuyện（0Không ghi lại 1Chỉ ghi lại văn bản 2Ghi lại văn bản và lời nói）' AFTER `system_prompt`;