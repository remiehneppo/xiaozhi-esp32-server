-- Nhà cung cấp mô hình OpenAI ASR
delete from `ai_model_provider` where id = 'SYSTEM_ASR_OpenaiASR';
INSERT INTO `ai_model_provider` (`id`, `model_type`, `provider_code`, `name`, `fields`, `sort`, `creator`, `create_date`, `updater`, `update_date`) VALUES
('SYSTEM_ASR_OpenaiASR', 'ASR', 'openai', 'OpenAInhận dạng giọng nói', '[{"key": "base_url", "type": "string", "label": "Khái niệm cơ bảnURL"}, {"key": "model_name", "type": "string", "label": "Tên mẫu"}, {"key": "api_key", "type": "string", "label": "APIchìa khóa"}, {"key": "output_dir", "type": "string", "label": "Thư mục đầu ra"}]', 9, 1, NOW(), 1, NOW());


-- Cấu hình mô hình OpenAI ASR
delete from `ai_model_config` where id = 'ASR_OpenaiASR';
INSERT INTO `ai_model_config` VALUES ('ASR_OpenaiASR', 'ASR', 'OpenaiASR', 'OpenAInhận dạng giọng nói', 0, 1, '{\"type\": \"openai\", \"api_key\": \"\", \"base_url\": \"https://api.openai.com/v1/audio/transcriptions\", \"model_name\": \"gpt-4o-mini-transcribe\", \"output_dir\": \"tmp/\"}', NULL, NULL, 9, NULL, NULL, NULL, NULL);

-- cấu hình mô hình ASR Groq
delete from `ai_model_config` where id = 'ASR_GroqASR';
INSERT INTO `ai_model_config` VALUES ('ASR_GroqASR', 'ASR', 'GroqASR', 'Groqnhận dạng giọng nói', 0, 1, '{\"type\": \"openai\", \"api_key\": \"\", \"base_url\": \"https://api.groq.com/openai/v1/audio/transcriptions\", \"model_name\": \"whisper-large-v3-turbo\", \"output_dir\": \"tmp/\"}', NULL, NULL, 10, NULL, NULL, NULL, NULL);


-- Đã cập nhật hướng dẫn cấu hình OpenAI ASR
UPDATE `ai_model_config` SET 
`doc_link` = 'https://platform.openai.com/docs/api-reference/audio/createTranscription',
`remark` = 'OpenAI ASRHướng dẫn cấu hình：
1. cần phải ở trongOpenAINền tảng mở để tạo ra các tổ chức và có đượcapi_key
2. Hỗ trợ、Tiếng Anh、ngày、Nhận dạng giọng nói tiếng Hàn và các ngôn ngữ khác，Tài liệu tham khảo cụ thểhttps://platform.openai.com/docs/guides/speech-to-text
3. Cần có kết nối Internet
4. Tệp đầu ra được lưu trongtmp/Thư mục
Các bước ứng dụng：
* *Các bước ứng dụng OpenAi ASR:**
1.Đăng nhậpOpenAI Platform。https://auth.openai.com/log-in
2.tạo raapi-key  https://platform.openai.com/settings/organization/api-keys
3.Có thể lựa chọn mô hìnhgpt-4o-transcribehoặcGPT-4o mini Transcribe
' WHERE `id` = 'ASR_OpenaiASR';

-- Đã cập nhật hướng dẫn cấu hình Groq ASR
UPDATE `ai_model_config` SET 
`doc_link` = 'https://console.groq.com/docs/speech-to-text',
`remark` = 'Groq ASRHướng dẫn cấu hình：
1.Đăng nhậpgroq Console。https://console.groq.com/home
2.tạo raapi-key  https://console.groq.com/keys
3.Có thể lựa chọn mô hìnhwhisper-large-v3-turbohoặcwhisper-large-v3（distil-whisper-large-v3-enChỉ hỗ trợ phiên âm tiếng Anh）
' WHERE `id` = 'ASR_GroqASR';