-- Thêm cấu hình mô hình Baidu ASR
delete from `ai_model_config` where `id` = 'ASR_BaiduASR';
INSERT INTO `ai_model_config` VALUES ('ASR_BaiduASR', 'ASR', 'BaiduASR', 'Nhận dạng giọng nói của Baidu', 0, 1, '{\"type\": \"baidu\", \"app_id\": \"\", \"api_key\": \"\", \"secret_key\": \"\", \"dev_pid\": 1537, \"output_dir\": \"tmp/\"}', NULL, NULL, 7, NULL, NULL, NULL, NULL);


-- Thêm nhà cung cấp ASR của Baidu
delete from `ai_model_provider` where `id` = 'SYSTEM_ASR_BaiduASR';
INSERT INTO `ai_model_provider` (`id`, `model_type`, `provider_code`, `name`, `fields`, `sort`, `creator`, `create_date`, `updater`, `update_date`) VALUES
('SYSTEM_ASR_BaiduASR', 'ASR', 'baidu', 'Nhận dạng giọng nói của Baidu', '[{"key":"app_id","label":"ứng dụngAppID","type":"string"},{"key":"api_key","label":"API Key","type":"string"},{"key":"secret_key","label":"Secret Key","type":"string"},{"key":"dev_pid","label":"Thông số ngôn ngữ","type":"number"},{"key":"output_dir","label":"Thư mục đầu ra","type":"string"}]', 7, 1, NOW(), 1, NOW());


-- Cập nhật hướng dẫn cấu hình Baidu ASR
UPDATE `ai_model_config` SET 
`doc_link` = 'https://console.bce.baidu.com/ai-engine/old/#/ai/speech/app/list',
`remark` = 'BaiduASRHướng dẫn cấu hình：
1. chuyến thăm https://console.bce.baidu.com/ai-engine/old/#/ai/speech/app/list
2. Tạo ứng dụng mới
3. nhận đượcAppID、API KeyvàSecret Key
4. Điền vào tập tin cấu hình
Xem hạn ngạch tài nguyên：https://console.bce.baidu.com/ai-engine/old/#/ai/speech/overview/resource/list
Mô tả tham số ngôn ngữ：https://ai.baidu.com/ai-doc/SPEECH/0lbxfnc9b
' WHERE `id` = 'ASR_BaiduASR';

-- Cập nhật các trường của nhà cung cấp Beanbag
update `ai_model_provider` set `fields` = 
'[{"key":"appid","label":"ứng dụngID","type":"string"},{"key":"access_token","label":"mã thông báo truy cập","type":"string"},{"key":"cluster","label":"cụm","type":"string"},{"key":"boosting_table_name","label":"Tên file từ nóng","type":"string"},{"key":"correct_table_name","label":"Thay thế tên file word","type":"string"},{"key":"output_dir","label":"Thư mục đầu ra","type":"string"}]'
where `id` = 'SYSTEM_ASR_DoubaoASR';

-- Đã cập nhật hướng dẫn cấu hình Doubao ASR
UPDATE `ai_model_config` SET 
`doc_link` = 'https://console.volcengine.com/speech/app',
`remark` = 'túi đậuASRHướng dẫn cấu hình：
1. Bạn cần tạo một ứng dụng trong bảng điều khiển Volcano Engine và lấyappidvàaccess_token
2. Hỗ trợ nhận dạng giọng nói tiếng Trung
3. Cần có kết nối Internet
4. Tệp đầu ra được lưu trongtmp/Thư mục
Các bước ứng dụng：
1. chuyến thăm https://console.volcengine.com/speech/app
2. Tạo ứng dụng mới
3. nhận đượcappidvàaccess_token
4. Điền vào tập tin cấu hình
Nếu bạn cần đặt những từ nóng，Vui lòng tham khảo：https://www.volcengine.com/docs/6561/155738
' WHERE `id` = 'ASR_DoubaoASR';