-- Nhà cung cấp mô hình VLLM
delete from `ai_model_provider` where id = 'SYSTEM_ASR_DoubaoStreamASR';
INSERT INTO `ai_model_provider` (`id`, `model_type`, `provider_code`, `name`, `fields`, `sort`, `creator`, `create_date`, `updater`, `update_date`) VALUES
('SYSTEM_ASR_DoubaoStreamASR', 'ASR', 'doubao_stream', 'Nhận dạng giọng nói động cơ núi lửa(phát trực tuyến)', '[{"key":"appid","label":"ứng dụngID","type":"string"},{"key":"access_token","label":"mã thông báo truy cập","type":"string"},{"key":"cluster","label":"cụm","type":"string"},{"key":"boosting_table_name","label":"Tên file từ nóng","type":"string"},{"key":"correct_table_name","label":"Thay thế tên file word","type":"string"},{"key":"output_dir","label":"Thư mục đầu ra","type":"string"}]', 3, 1, NOW(), 1, NOW());


-- Cấu hình mô hình VLLM
delete from `ai_model_config` where id = 'ASR_DoubaoStreamASR';
INSERT INTO `ai_model_config` VALUES ('ASR_DoubaoStreamASR', 'ASR', 'DoubaoStreamASR', 'Nhận dạng giọng nói Beanbao(phát trực tuyến)', 0, 1, '{\"type\": \"doubao_stream\", \"appid\": \"\", \"access_token\": \"\", \"cluster\": \"volcengine_input_common\", \"output_dir\": \"tmp/\"}', NULL, NULL, 3, NULL, NULL, NULL, NULL);


-- Đã cập nhật hướng dẫn cấu hình Doubao ASR
UPDATE `ai_model_config` SET 
`doc_link` = 'https://console.volcengine.com/speech/app',
`remark` = 'túi đậuASRHướng dẫn cấu hình：
1. túi đậuASRvà bánh đậu(phát trực tuyến)ASRSự khác biệt là：túi đậuASRĐó là trả tiền cho mỗi lần xem，túi đậu(phát trực tuyến)ASRNó được tính phí đúng giờ
2. Trả tiền cho mỗi lần xem thường rẻ hơn，Nhưng túi đậu(phát trực tuyến)ASRCông nghệ mô hình lớn được sử dụng，hiệu ứng tốt hơn
3. Bạn cần tạo một ứng dụng trong bảng điều khiển Volcano Engine và lấyappidvàaccess_token
4. Hỗ trợ nhận dạng giọng nói tiếng Trung
5. Cần có kết nối Internet
6. Tệp đầu ra được lưu trongtmp/Thư mục
Các bước ứng dụng：
1. chuyến thăm https://console.volcengine.com/speech/app
2. Tạo ứng dụng mới
3. nhận đượcappidvàaccess_token
4. Điền vào tập tin cấu hình
Nếu bạn cần đặt những từ nóng，Vui lòng tham khảo：https://www.volcengine.com/docs/6561/155738
' WHERE `id` = 'ASR_DoubaoASR';

UPDATE `ai_model_config` SET 
`doc_link` = 'https://console.volcengine.com/speech/app',
`remark` = 'túi đậuASRHướng dẫn cấu hình：
1. túi đậuASRvà bánh đậu(phát trực tuyến)ASRSự khác biệt là：túi đậuASRĐó là trả tiền cho mỗi lần xem，túi đậu(phát trực tuyến)ASRNó được tính phí đúng giờ
2. Trả tiền cho mỗi lần xem thường rẻ hơn，Nhưng túi đậu(phát trực tuyến)ASRCông nghệ mô hình lớn được sử dụng，hiệu ứng tốt hơn
3. Bạn cần tạo một ứng dụng trong bảng điều khiển Volcano Engine và lấyappidvàaccess_token
4. Hỗ trợ nhận dạng giọng nói tiếng Trung
5. Cần có kết nối Internet
6. Tệp đầu ra được lưu trongtmp/Thư mục
Các bước ứng dụng：
1. chuyến thăm https://console.volcengine.com/speech/app
2. Tạo ứng dụng mới
3. nhận đượcappidvàaccess_token
4. Điền vào tập tin cấu hình
Nếu bạn cần đặt những từ nóng，Vui lòng tham khảo：https://www.volcengine.com/docs/6561/155738
' WHERE `id` = 'ASR_DoubaoStreamASR';
