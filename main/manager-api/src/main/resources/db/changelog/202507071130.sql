-- Thêm nhà cung cấp ASR phát trực tuyến trên nền tảng đám mây của Alibaba
delete from `ai_model_provider` where id = 'SYSTEM_ASR_AliyunStreamASR';
INSERT INTO `ai_model_provider` (`id`, `model_type`, `provider_code`, `name`, `fields`, `sort`, `creator`, `create_date`, `updater`, `update_date`) VALUES
('SYSTEM_ASR_AliyunStreamASR', 'ASR', 'aliyun_stream', 'Nhận dạng giọng nói trên nền tảng đám mây của Alibaba(phát trực tuyến)', '[{"key":"appkey","label":"ứng dụngAppKey","type":"string"},{"key":"token","label":"tạm thờiToken","type":"string"},{"key":"access_key_id","label":"AccessKey ID","type":"string"},{"key":"access_key_secret","label":"AccessKey Secret","type":"string"},{"key":"host","label":"Địa chỉ dịch vụ","type":"string"},{"key":"max_sentence_silence","label":"Thời gian phát hiện phân đoạn câu","type":"number"},{"key":"output_dir","label":"Thư mục đầu ra","type":"string"}]', 6, 1, NOW(), 1, NOW());

-- Thêm cấu hình mô hình ASR phát trực tuyến trên nền tảng đám mây của Alibaba
delete from `ai_model_config` where id = 'ASR_AliyunStreamASR';
INSERT INTO `ai_model_config` VALUES ('ASR_AliyunStreamASR', 'ASR', 'AliyunStreamASR', 'Nhận dạng giọng nói trên nền tảng đám mây của Alibaba(phát trực tuyến)', 0, 1, '{\"type\": \"aliyun_stream\", \"appkey\": \"\", \"token\": \"\", \"access_key_id\": \"\", \"access_key_secret\": \"\", \"host\": \"nls-gateway-cn-shanghai.aliyuncs.com\", \"max_sentence_silence\": 800, \"output_dir\": \"tmp/\"}', NULL, NULL, 8, NULL, NULL, NULL, NULL);

-- Đã cập nhật hướng dẫn cấu hình ASR phát trực tuyến trên nền tảng đám mây của Alibaba
UPDATE `ai_model_config` SET 
`doc_link` = 'https://nls-portal.console.aliyun.com/',
`remark` = 'Truyền phát trực tuyến trên nền tảng đám mây của AlibabaASRHướng dẫn cấu hình：
1. Đám mây của AlibabaASRvà Đám mây của Alibaba(phát trực tuyến)ASRSự khác biệt là：Đám mây của AlibabaASRĐó là sự nhận dạng một lần，Đám mây của Alibaba(phát trực tuyến)ASRlà nhận dạng phát trực tuyến theo thời gian thực
2. phát trực tuyếnASRCó độ trễ thấp hơn và hiệu suất thời gian thực tốt hơn，Thích hợp cho các tình huống tương tác bằng giọng nói
3. Bạn cần tạo một ứng dụng trong Bảng điều khiển tương tác giọng nói thông minh trên nền tảng đám mây của Alibaba và lấy thông tin xác thực.
4. Hỗ trợ nhận dạng giọng nói theo thời gian thực của Trung Quốc，Hỗ trợ dự đoán dấu câu và chuẩn hóa văn bản nghịch đảo
5. Cần có kết nối Internet，Tệp đầu ra được lưu trongtmp/Thư mục
Các bước ứng dụng：
1. chuyến thăm https://nls-portal.console.aliyun.com/ Kích hoạt dịch vụ tương tác giọng nói thông minh
2. chuyến thăm https://nls-portal.console.aliyun.com/applist Tạo dự án và nhậnappkey
3. chuyến thăm https://nls-portal.console.aliyun.com/overview Nhận tạm thờitoken（hoặc cấu hìnhaccess_key_idvàaccess_key_secretNhận tự động）
4. Nếu bạn cần cập nhậttokenquản lý，Cấu hình đề xuấtaccess_key_idvàaccess_key_secret
5. max_sentence_silenceTham số kiểm soát thời gian phát hiện phân đoạn câu（mili giây），Mặc định800ms
Để biết thêm cấu hình tham số，Vui lòng tham khảo：https://help.aliyun.com/zh/isi/developer-reference/real-time-speech-recognition
' WHERE `id` = 'ASR_AliyunStreamASR';
