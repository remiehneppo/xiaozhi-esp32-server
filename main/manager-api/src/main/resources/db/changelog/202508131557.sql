-- Thêm nhà cung cấp TTS phát trực tuyến mái chèo_speech
DELETE FROM `ai_model_provider` WHERE id = 'SYSTEM_TTS_PaddleSpeechTTS';
INSERT INTO `ai_model_provider` (`id`, `model_type`, `provider_code`, `name`, `fields`, `sort`, `creator`, `create_date`, `updater`, `update_date`) 
VALUES ('SYSTEM_TTS_PaddleSpeechTTS', 'TTS', 'paddle_speech', 'PaddleSpeechTTS', 
'[{"key":"protocol","label":"loại giao thức","type":"string","options":["websocket","http"]},{"key":"url","label":"Địa chỉ dịch vụ","type":"string"},{"key":"spk_id","label":"âm sắc","type":"int"},{"key":"sample_rate","label":"Tốc độ lấy mẫu","type":"float"},{"key":"speed","label":"tốc độ nói","type":"float"},{"key":"volume","label":"khối lượng","type":"float"},{"key":"save_path","label":"lưu đường dẫn","type":"string"}]', 
17, 1, NOW(), 1, NOW());

-- Thêm cấu hình mô hình TTS truyền trực tuyến mái chèo_speech
DELETE FROM `ai_model_config` WHERE id = 'TTS_PaddleSpeechTTS';
INSERT INTO `ai_model_config` VALUES ('TTS_PaddleSpeechTTS', 'TTS', 'PaddleSpeechTTS', 'PaddleSpeechTTS', 0, 1, 
'{"type": "paddle_speech", "protocol": "websocket", "url": "ws://127.0.0.1:8092/paddlespeech/tts/streaming", "spk_id": "0", "sample_rate": 24000, "speed": 1.0, "volume": 1.0, "save_path": "./streaming_tts.wav"}', 
NULL, NULL, 20, NULL, NULL, NULL, NULL);

-- Đã cập nhật hướng dẫn cấu hình PaddleSpeechTTS
UPDATE `ai_model_config` SET 
`doc_link` = 'https://github.com/PaddlePaddle/PaddleSpeech',
`remark` = 'PaddleSpeechTTS Hướng dẫn cấu hình：
1. PaddleSpeech Đây là công cụ tổng hợp giọng nói nguồn mở của Baidu Feipiao.，Hỗ trợ triển khai ngoại tuyến cục bộ và đào tạo mô hình。paddlepaddleĐịa chỉ khung plasma bay của Baidu：https://www.paddlepaddle.org.cn/
2. hỗ trợ WebSocket và HTTP thỏa thuận，Được sử dụng theo mặc định WebSocket phát trực tiếp（Tài liệu triển khai tham khảo：https://github.com/xinnan-tech/xiaozhi-esp32-server/blob/main/docs/paddlespeech-deploy.md）。
3. Triển khai cục bộ trước khi sử dụng paddlespeech dịch vụ，Dịch vụ chạy theo mặc định trong ws://127.0.0.1:8092/paddlespeech/tts/streaming
4. Hỗ trợ phát âm tùy chỉnh、tốc độ nói、Khối lượng và tốc độ mẫu。
' WHERE `id` = 'TTS_PaddleSpeechTTS';

-- Xóa âm thanh cũ và thêm âm thanh mặc định
DELETE FROM `ai_tts_voice` WHERE tts_model_id = 'TTS_PaddleSpeechTTS';
INSERT INTO `ai_tts_voice` VALUES ('TTS_PaddleSpeechTTS_0000', 'TTS_PaddleSpeechTTS', 'Mặc định', '0', 'Tiếng Trung', NULL, NULL, NULL, NULL, 1, NULL, NULL, NULL, NULL);