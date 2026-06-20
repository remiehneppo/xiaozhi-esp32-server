-- Đã thêm nhà cung cấp TTS phát trực tuyến Index-TTS-vLLM
delete from `ai_model_provider` where id = 'SYSTEM_TTS_IndexStreamTTS';
INSERT INTO `ai_model_provider` (`id`, `model_type`, `provider_code`, `name`, `fields`, `sort`, `creator`, `create_date`, `updater`, `update_date`) VALUES
('SYSTEM_TTS_IndexStreamTTS', 'TTS', 'index_stream', 'Index-TTS-vLLMtổng hợp giọng nói trực tuyến', '[{"key":"api_url","label":"APIĐịa chỉ dịch vụ","type":"string"},{"key":"voice","label":"Âm thanh mặc định","type":"string"},{"key":"audio_format","label":"định dạng âm thanh","type":"string"},{"key":"output_dir","label":"Thư mục đầu ra","type":"string"}]', 16, 1, NOW(), 1, NOW());

-- Thêm cấu hình mô hình TTS phát trực tuyến Index-TTS-vLLM
delete from `ai_model_config` where id = 'TTS_IndexStreamTTS';
INSERT INTO `ai_model_config` VALUES ('TTS_IndexStreamTTS', 'TTS', 'IndexStreamTTS', 'Index-TTS-vLLMtổng hợp giọng nói trực tuyến', 0, 1, '{\"type\": \"index_stream\", \"api_url\": \"http://127.0.0.1:11996/tts\", \"voice\": \"jay_klee\", \"audio_format\": \"pcm\", \"output_dir\": \"tmp/\"}', NULL, NULL, 19, NULL, NULL, NULL, NULL);

-- Đã cập nhật hướng dẫn cấu hình TTS phát trực tuyến Index-TTS-vLLM
UPDATE `ai_model_config` SET 
`doc_link` = 'https://github.com/Ksuriuri/index-tts-vllm',
`remark` = 'Index-TTS-vLLMphát trực tuyếnTTSHướng dẫn cấu hình：
1. Index-TTS-vLLMdựa trênIndex-TTSdự ánvLLMDịch vụ lý luận，Cung cấp khả năng tổng hợp giọng nói trực tuyến
2. Hỗ trợ nhiều âm sắc，Chất lượng âm thanh tự nhiên，Thích hợp cho các tình huống tương tác bằng giọng nói khác nhau
3. Cần triển khai trướcIndex-TTS-vLLMdịch vụ，Sau đó cấu hìnhAPIđịa chỉ
4. Hỗ trợ tổng hợp phát trực tuyến theo thời gian thực，Có độ trễ thấp hơn
5. Hỗ trợ âm thanh tùy chỉnh，Có sẵn tại các dự ánassetsĐăng ký âm thanh mới trong thư mục
Các bước triển khai：
1. Dự án nhân bản：git clone https://github.com/Ksuriuri/index-tts-vllm.git
2. Cài đặt phụ thuộc：pip install -r requirements.txt
3. Bắt đầu dịch vụ：python app.py
4. Dịch vụ chạy theo mặc định trong http://127.0.0.1:11996
5. Nếu bạn cần những âm thanh khác，Các mặt hàng có sẵnassetsĐăng ký theo thư mục
6. Hỗ trợ nhiều định dạng âm thanh：pcm、wav、mp3Đợi đã
Để biết thêm cấu hình，Vui lòng tham khảo：https://github.com/Ksuriuri/index-tts-vllm/blob/master/README.md
' WHERE `id` = 'TTS_IndexStreamTTS';

-- Đã thêm âm thanh TTS phát trực tuyến Index-TTS-vLLM
delete from `ai_tts_voice` where tts_model_id = 'TTS_IndexStreamTTS';
-- Âm thanh mặc định
INSERT INTO `ai_tts_voice` VALUES ('TTS_IndexStreamTTS_0001', 'TTS_IndexStreamTTS', 'Jay Klee', 'jay_klee', 'Tiếng Trung và tiếng Trung và tiếng Anh hỗn hợp', NULL, NULL, NULL, NULL, 1, NULL, NULL, NULL, NULL);
