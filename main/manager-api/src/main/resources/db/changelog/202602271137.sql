-- Cập nhật cấu hình nhà cung cấp Tencent TTS và thêm các thông số về tốc độ, âm lượng và định dạng
UPDATE `ai_model_provider`
SET fields = '[{"key":"appid","label":"ứng dụngID","type":"string"},{"key":"secret_id","label":"Secret ID","type":"string"},{"key":"secret_key","label":"Secret Key","type":"string"},{"key":"format","label":"định dạng âm thanh","type":"string"},{"key":"speed","label":"tốc độ nói","type":"number"},{"key":"volume","label":"khối lượng","type":"number"},{"key":"output_dir","label":"Thư mục đầu ra","type":"string"},{"key":"voice","label":"âm sắcID","type":"string"},{"key":"region","label":"khu vực","type":"string"}]'
WHERE id = 'SYSTEM_TTS_TencentTTS';

-- Cập nhật cấu hình mô hình Tencent TTS, thêm thông số tốc độ và âm lượng, đồng thời bổ sung mô tả thông số
UPDATE `ai_model_config` SET 
    `config_json` = JSON_SET(`config_json`, '$.speed', 0, '$.volume', 0),
    `remark` = 'TencentTTSHướng dẫn cấu hình：
1. Cần kích hoạt dịch vụ tương tác giọng nói thông minh trên nền tảng Tencent Cloud
2. Hỗ trợ nhiều âm sắc，Cấu hình hiện tại sử dụng101001
3. Cần có kết nối Internet
4. Tệp đầu ra được lưu trongtmp/Thư mục
Các bước ứng dụng：
1. chuyến thăm https://console.cloud.tencent.com/cam/capi Nhận chìa khóa
2. chuyến thăm https://console.cloud.tencent.com/tts/resourcebundle Nhận tài nguyên miễn phí
3. Tạo ứng dụng mới
4. nhận đượcappid、secret_idvàsecret_key
5. Điền vào tập tin cấu hình
Thông số âm thanh：
- format: định dạng âm thanh，hỗ trợpcm、wav、mp3
- speed: tốc độ nói，phạm vi-2~6，Mặc định0
- volume: khối lượng，phạm vi-10~10，Mặc định0'
WHERE `id` = 'TTS_TencentTTS';

-- Cập nhật cấu hình nhà cung cấp CozeCnTTS để thêm thông số tốc độ và độ ồn_rate
UPDATE `ai_model_provider`
SET fields = '[{"key":"voice","label":"âm sắc","type":"string"},{"key":"access_token","label":"mã thông báo truy cập","type":"string"},{"key":"speed","label":"tốc độ nói","type":"number"},{"key":"loudness_rate","label":"Tăng âm lượng","type":"number"},{"key":"output_dir","label":"Thư mục đầu ra","type":"string"},{"key":"response_format","label":"định dạng phản hồi","type":"string"}]'
WHERE id = 'SYSTEM_TTS_cozecn';

-- Cập nhật cấu hình mô hình CozeCnTTS, thêm thông số tốc độ và độ ồn_rate, đồng thời bổ sung mô tả thông số
UPDATE `ai_model_config` SET 
    `config_json` = JSON_SET(`config_json`, '$.speed', 1, '$.loudness_rate', 0),
    `remark` = 'CozeHướng dẫn cấu hình tổng hợp giọng nói tiếng Trung：
1. chuyến thăm https://www.coze.cn/ Đăng ký và đăng nhập
2. Tạo một ứng dụng và nhậnaccess_token
3. Chọn đúng giai điệuID
Thông số âm thanh：
- response_format: định dạng âm thanh，hỗ trợpcm、wav、mp3
- speed: tốc độ nói，phạm vi0.5~2，Mặc định1
- loudness_rate: Tăng âm lượng，phạm vi-50~100，Mặc định0'
WHERE `id` = 'TTS_CozeCnTTS';
