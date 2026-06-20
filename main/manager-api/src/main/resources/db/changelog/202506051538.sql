-- Đã thêm cấu hình mô hình và nhà cung cấp LinkeraiTTS
delete from `ai_model_provider` where id = 'SYSTEM_TTS_LinkeraiTTS';
INSERT INTO `ai_model_provider` (`id`, `model_type`, `provider_code`, `name`, `fields`, `sort`, `creator`, `create_date`, `updater`, `update_date`) VALUES
('SYSTEM_TTS_LinkeraiTTS', 'TTS', 'linkerai', 'Linkeraitổng hợp giọng nói', '[{"key":"api_url","label":"APIđịa chỉ","type":"string"},{"key":"audio_format","label":"định dạng âm thanh","type":"string"},{"key":"access_token","label":"mã thông báo truy cập","type":"string"},{"key":"voice","label":"Âm thanh mặc định","type":"string"}]', 14, 1, NOW(), 1, NOW());

delete from `ai_model_config` where id = 'TTS_LinkeraiTTS';
INSERT INTO `ai_model_config` VALUES ('TTS_LinkeraiTTS', 'TTS', 'LinkeraiTTS', 'Linkeraitổng hợp giọng nói', 0, 1, '{\"type\": \"linkerai\", \"api_url\": \"https://tts.linkerai.cn/tts\", \"audio_format\": \"pcm\", \"access_token\": \"U4YdYXVfpwWnk2t5Gp822zWPCuORyeJL\", \"voice\": \"OUeAo1mhq6IBExi\"}', NULL, NULL, 17, NULL, NULL, NULL, NULL);

-- Tài liệu cấu hình mô hình LinkeraiTTS
UPDATE `ai_model_config` SET 
`doc_link` = 'https://tts.linkerai.cn/docs',
`remark` = 'LinkeraiHướng dẫn cấu hình dịch vụ tổng hợp giọng nói：
1. chuyến thăm https://linkerai.cn Đăng ký và nhận mã thông báo truy cập
2. mặc địnhaccess_tokenđể thử nghiệm，Không sử dụng cho mục đích thương mại
3. Hỗ trợ chức năng nhân bản âm thanh，Bạn có thể tự mình tải lên âm thanh，điền vàovoicethông số
4. nếuvoiceTham số trống，Âm thanh mặc định sẽ được sử dụng' WHERE `id` = 'TTS_LinkeraiTTS';


delete from `ai_tts_voice` where tts_model_id = 'TTS_LinkeraiTTS';
INSERT INTO `ai_tts_voice` VALUES ('TTS_LinkeraiTTS_0001', 'TTS_LinkeraiTTS', 'Chỉ Nhược', 'OUeAo1mhq6IBExi', 'Tiếng Trung', NULL, NULL, 1, NULL, NULL, NULL, NULL);
