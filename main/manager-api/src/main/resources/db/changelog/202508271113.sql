-- Nhà cung cấp mô hình VOSK ASR
delete from `ai_model_provider` where id = 'SYSTEM_ASR_VoskASR';
INSERT INTO `ai_model_provider` (`id`, `model_type`, `provider_code`, `name`, `fields`, `sort`, `creator`, `create_date`, `updater`, `update_date`) VALUES
('SYSTEM_ASR_VoskASR', 'ASR', 'vosk', 'VOSKNhận dạng giọng nói ngoại tuyến', '[{"key": "model_path", "type": "string", "label": "đường dẫn mô hình"}, {"key": "output_dir", "type": "string", "label": "Thư mục đầu ra"}]', 11, 1, NOW(), 1, NOW());

-- Cấu hình mô hình VOSK ASR
delete from `ai_model_config` where id = 'ASR_VoskASR';
INSERT INTO `ai_model_config` VALUES ('ASR_VoskASR', 'ASR', 'VoskASR', 'VOSKNhận dạng giọng nói ngoại tuyến', 0, 1, '{\"type\": \"vosk\", \"model_path\": \"\", \"output_dir\": \"tmp/\"}', NULL, NULL, 11, NULL, NULL, NULL, NULL);

-- Hướng dẫn cấu hình VOSK ASR được cập nhật
UPDATE `ai_model_config` SET 
`doc_link` = 'https://alphacephei.com/vosk/',
`remark` = 'VOSK ASRHướng dẫn cấu hình：
1. VOSKLà thư viện nhận dạng giọng nói ngoại tuyến，Hỗ trợ nhiều ngôn ngữ
2. Bạn cần tải xuống tệp mô hình trước：https://alphacephei.com/vosk/models
3. Mô hình Trung Quốc được khuyến khíchvosk-model-small-cn-0.22hoặcvosk-model-cn-0.22
4. Chạy hoàn toàn ngoại tuyến，Không cần kết nối internet
5. Tệp đầu ra được lưu trongtmp/Thư mục
Các bước sử dụng：
1. chuyến thăm https://alphacephei.com/vosk/models Tải xuống mô hình Trung Quốc
2. Giải nén tệp mô hình vào thư mục dự ánmodels/vosk/thư mục
3. Chỉ định đường dẫn mô hình chính xác trong cấu hình
4. Lưu ý：VOSKĐầu ra mô hình tiếng Trung không có dấu chấm câu，Sẽ có khoảng cách giữa các từ
' WHERE `id` = 'ASR_VoskASR';