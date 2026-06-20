update `ai_model_provider` set `fields` = 
'[{"key": "api_url","label": "APIđịa chỉ","type": "string"},{"key": "voice","label": "âm sắc","type": "string"},{"key": "output_dir","label": "Thư mục đầu ra","type": "string"},{"key": "authorization","label": "Ủy quyền","type": "string"},{"key": "appid","label": "ứng dụngID","type": "string"},{"key": "access_token","label": "mã thông báo truy cập","type": "string"},{"key": "cluster","label": "cụm","type": "string"},{"key": "speed_ratio","label": "tốc độ nói","type": "number"},{"key": "volume_ratio","label": "khối lượng","type": "number"},{"key": "pitch_ratio","label": "cao độ","type": "number"}]'
where `id` = 'SYSTEM_TTS_doubao';

-- Thêm nhà cung cấp ASR của Alibaba Cloud
delete from `ai_model_provider` where `id` = 'SYSTEM_ASR_AliyunASR';
INSERT INTO `ai_model_provider` (`id`, `model_type`, `provider_code`, `name`, `fields`, `sort`, `creator`, `create_date`, `updater`, `update_date`) VALUES
('SYSTEM_ASR_AliyunASR', 'ASR', 'aliyun', 'Nhận dạng giọng nói trên nền tảng đám mây của Alibaba', '[{"key":"appkey","label":"ứng dụngAppKey","type":"string"},{"key":"token","label":"tạm thờiToken","type":"string"},{"key":"access_key_id","label":"AccessKey ID","type":"string"},{"key":"access_key_secret","label":"AccessKey Secret","type":"string"},{"key":"output_dir","label":"Thư mục đầu ra","type":"string"}]', 5, 1, NOW(), 1, NOW());

-- Thêm cấu hình mô hình ASR của Alibaba Cloud
delete from `ai_model_config` where `id` = 'ASR_AliyunASR';
INSERT INTO `ai_model_config` VALUES ('ASR_AliyunASR', 'ASR', 'AliyunASR', 'Nhận dạng giọng nói trên nền tảng đám mây của Alibaba', 0, 1, '{\"type\": \"aliyun\", \"appkey\": \"\", \"token\": \"\", \"access_key_id\": \"\", \"access_key_secret\": \"\", \"output_dir\": \"tmp/\"}', NULL, NULL, 6, NULL, NULL, NULL, NULL);

-- Cập nhật tài liệu cấu hình mô hình Alibaba Cloud ASR
UPDATE `ai_model_config` SET 
`doc_link` = 'https://nls-portal.console.aliyun.com/',
`remark` = 'Đám mây của AlibabaASRHướng dẫn cấu hình：
1. chuyến thăm https://nls-portal.console.aliyun.com/ Kích hoạt dịch vụ
2. chuyến thăm https://nls-portal.console.aliyun.com/applist nhận đượcappkey
3. chuyến thăm https://nls-portal.console.aliyun.com/overview nhận đượctoken
4. nhận đượcaccess_key_idvàaccess_key_secret
5. Điền vào tập tin cấu hình' WHERE `id` = 'ASR_AliyunASR';

-- Chèn loại từ điển loại chương trình cơ sở
delete from `sys_dict_type` where `id` = 101;
INSERT INTO `sys_dict_type` (`id`, `dict_type`, `dict_name`, `remark`, `sort`, `creator`, `create_date`, `updater`, `update_date`) VALUES 
(101, 'FIRMWARE_TYPE', 'Loại phần mềm', 'Từ điển loại phần mềm', 0, 1, NOW(), 1, NOW());

-- Chèn dữ liệu từ điển loại chương trình cơ sở
delete from `sys_dict_data` where `dict_type_id` = 101;
INSERT INTO `sys_dict_data` (`id`, `dict_type_id`, `dict_label`, `dict_value`, `remark`, `sort`, `creator`, `create_date`, `updater`, `update_date`) VALUES 
(101001, 101, 'Phiên bản mới của hệ thống dây điện trên bảng mạch（WiFi）', 'bread-compact-wifi', 'Phiên bản mới của hệ thống dây điện trên bảng mạch（WiFi）', 1, 1, NOW(), 1, NOW()),
(101002, 101, 'Phiên bản mới của hệ thống dây điện trên bảng mạch（WiFi）+ LCD', 'bread-compact-wifi-lcd', 'Phiên bản mới của hệ thống dây điện trên bảng mạch（WiFi）+ LCD', 2, 1, NOW(), 1, NOW()),
(101003, 101, 'Phiên bản mới của hệ thống dây điện trên bảng mạch（ML307 AT）', 'bread-compact-ml307', 'Phiên bản mới của hệ thống dây điện trên bảng mạch（ML307 AT）', 3, 1, NOW(), 1, NOW()),
(101004, 101, 'bảng mạch（WiFi） ESP32 DevKit', 'bread-compact-esp32', 'bảng mạch（WiFi） ESP32 DevKit', 4, 1, NOW(), 1, NOW()),
(101005, 101, 'bảng mạch（WiFi+ LCD） ESP32 DevKit', 'bread-compact-esp32-lcd', 'bảng mạch（WiFi+ LCD） ESP32 DevKit', 5, 1, NOW(), 1, NOW()),
(101006, 101, 'DFRobot bảng trống k10', 'df-k10', 'DFRobot bảng trống k10', 6, 1, NOW(), 1, NOW()),
(101007, 101, 'ESP32 CGC', 'esp32-cgc', 'ESP32 CGC', 7, 1, NOW(), 1, NOW()),
(101008, 101, 'ESP BOX 3', 'esp-box-3', 'ESP BOX 3', 8, 1, NOW(), 1, NOW()),
(101009, 101, 'ESP BOX', 'esp-box', 'ESP BOX', 9, 1, NOW(), 1, NOW()),
(101010, 101, 'ESP BOX Lite', 'esp-box-lite', 'ESP BOX Lite', 10, 1, NOW(), 1, NOW()),
(101011, 101, 'Kevin Box 1', 'kevin-box-1', 'Kevin Box 1', 11, 1, NOW(), 1, NOW()),
(101012, 101, 'Kevin Box 2', 'kevin-box-2', 'Kevin Box 2', 12, 1, NOW(), 1, NOW()),
(101013, 101, 'Kevin C3', 'kevin-c3', 'Kevin C3', 13, 1, NOW(), 1, NOW()),
(101014, 101, 'Kevin SP V3Ban phát triển', 'kevin-sp-v3-dev', 'Kevin SP V3Ban phát triển', 14, 1, NOW(), 1, NOW()),
(101015, 101, 'Kevin SP V4Ban phát triển', 'kevin-sp-v4-dev', 'Kevin SP V4Ban phát triển', 15, 1, NOW(), 1, NOW()),
(101016, 101, 'Công nghệ chim ưng biển3.13LCDBan phát triển', 'kevin-yuying-313lcd', 'Công nghệ chim ưng biển3.13LCDBan phát triển', 16, 1, NOW(), 1, NOW()),
(101017, 101, 'Lichuang·Trường thực hànhESP32-S3Ban phát triển', 'lichuang-dev', 'Lichuang·Trường thực hànhESP32-S3Ban phát triển', 17, 1, NOW(), 1, NOW()),
(101018, 101, 'Lichuang·Trường thực hànhESP32-C3Ban phát triển', 'lichuang-c3-dev', 'Lichuang·Trường thực hànhESP32-C3Ban phát triển', 18, 1, NOW(), 1, NOW()),
(101019, 101, 'nút ma thuật Magiclick_2.4', 'magiclick-2p4', 'nút ma thuật Magiclick_2.4', 19, 1, NOW(), 1, NOW()),
(101020, 101, 'nút ma thuật Magiclick_2.5', 'magiclick-2p5', 'nút ma thuật Magiclick_2.5', 20, 1, NOW(), 1, NOW()),
(101021, 101, 'nút ma thuật Magiclick_C3', 'magiclick-c3', 'nút ma thuật Magiclick_C3', 21, 1, NOW(), 1, NOW()),
(101022, 101, 'nút ma thuật Magiclick_C3_v2', 'magiclick-c3-v2', 'nút ma thuật Magiclick_C3_v2', 22, 1, NOW(), 1, NOW()),
(101023, 101, 'M5Stack CoreS3', 'm5stack-core-s3', 'M5Stack CoreS3', 23, 1, NOW(), 1, NOW()),
(101024, 101, 'AtomS3 + Echo Base', 'atoms3-echo-base', 'AtomS3 + Echo Base', 24, 1, NOW(), 1, NOW()),
(101025, 101, 'AtomS3R + Echo Base', 'atoms3r-echo-base', 'AtomS3R + Echo Base', 25, 1, NOW(), 1, NOW()),
(101026, 101, 'AtomS3R CAM/M12 + Echo Base', 'atoms3r-cam-m12-echo-base', 'AtomS3R CAM/M12 + Echo Base', 26, 1, NOW(), 1, NOW()),
(101027, 101, 'AtomMatrix + Echo Base', 'atommatrix-echo-base', 'AtomMatrix + Echo Base', 27, 1, NOW(), 1, NOW()),
(101028, 101, 'Anh Tôm Mini C3', 'xmini-c3', 'Anh Tôm Mini C3', 28, 1, NOW(), 1, NOW()),
(101029, 101, 'ESP32S3_KORVO2_V3Ban phát triển', 'esp32s3-korvo2-v3', 'ESP32S3_KORVO2_V3Ban phát triển', 29, 1, NOW(), 1, NOW()),
(101030, 101, 'ESP-SparkBotBan phát triển', 'esp-sparkbot', 'ESP-SparkBotBan phát triển', 30, 1, NOW(), 1, NOW()),
(101031, 101, 'ESP-Spot-S3', 'esp-spot-s3', 'ESP-Spot-S3', 31, 1, NOW(), 1, NOW()),
(101032, 101, 'Waveshare ESP32-S3-Touch-AMOLED-1.8', 'esp32-s3-touch-amoled-1.8', 'Waveshare ESP32-S3-Touch-AMOLED-1.8', 32, 1, NOW(), 1, NOW()),
(101033, 101, 'Waveshare ESP32-S3-Touch-LCD-1.85C', 'esp32-s3-touch-lcd-1.85c', 'Waveshare ESP32-S3-Touch-LCD-1.85C', 33, 1, NOW(), 1, NOW()),
(101034, 101, 'Waveshare ESP32-S3-Touch-LCD-1.85', 'esp32-s3-touch-lcd-1.85', 'Waveshare ESP32-S3-Touch-LCD-1.85', 34, 1, NOW(), 1, NOW()),
(101035, 101, 'Waveshare ESP32-S3-Touch-LCD-1.46', 'esp32-s3-touch-lcd-1.46', 'Waveshare ESP32-S3-Touch-LCD-1.46', 35, 1, NOW(), 1, NOW()),
(101036, 101, 'Waveshare ESP32-S3-Touch-LCD-3.5', 'esp32-s3-touch-lcd-3.5', 'Waveshare ESP32-S3-Touch-LCD-3.5', 36, 1, NOW(), 1, NOW()),
(101037, 101, 'Hạt khoai tây', 'tudouzi', 'Hạt khoai tây', 37, 1, NOW(), 1, NOW()),
(101038, 101, 'LILYGO T-Circle-S3', 'lilygo-t-circle-s3', 'LILYGO T-Circle-S3', 38, 1, NOW(), 1, NOW()),
(101039, 101, 'LILYGO T-CameraPlus-S3', 'lilygo-t-cameraplus-s3', 'LILYGO T-CameraPlus-S3', 39, 1, NOW(), 1, NOW()),
(101040, 101, 'Movecall Moji Tiểu ChỉAICông cụ phái sinh', 'movecall-moji-esp32s3', 'Movecall Moji Tiểu ChỉAICông cụ phái sinh', 40, 1, NOW(), 1, NOW()),
(101041, 101, 'Movecall CuiCan rực rỡ·AImặt dây chuyền', 'movecall-cuican-esp32s3', 'Movecall CuiCan rực rỡ·AImặt dây chuyền', 41, 1, NOW(), 1, NOW()),
(101042, 101, 'nguyên tử đúng giờDNESP32S3Ban phát triển', 'atk-dnesp32s3', 'nguyên tử đúng giờDNESP32S3Ban phát triển', 42, 1, NOW(), 1, NOW()),
(101043, 101, 'nguyên tử đúng giờDNESP32S3-BOX', 'atk-dnesp32s3-box', 'nguyên tử đúng giờDNESP32S3-BOX', 43, 1, NOW(), 1, NOW()),
(101044, 101, 'Ban phát triển DuduCHATX(wifi)', 'du-chatx', 'Ban phát triển DuduCHATX(wifi)', 44, 1, NOW(), 1, NOW()),
(101045, 101, 'trường Thái Cực Quyềnesp32s3', 'taiji-pi-s3', 'trường Thái Cực Quyềnesp32s3', 45, 1, NOW(), 1, NOW()),
(101046, 101, 'Trí tuệ ngôi sao công nghệ không tên0.85(WIFI)', 'xingzhi-cube-0.85tft-wifi', 'Trí tuệ ngôi sao công nghệ không tên0.85(WIFI)', 46, 1, NOW(), 1, NOW()),
(101047, 101, 'Trí tuệ ngôi sao công nghệ không tên0.85(ML307)', 'xingzhi-cube-0.85tft-ml307', 'Trí tuệ ngôi sao công nghệ không tên0.85(ML307)', 47, 1, NOW(), 1, NOW()),
(101048, 101, 'Trí tuệ ngôi sao công nghệ không tên0.96(WIFI)', 'xingzhi-cube-0.96oled-wifi', 'Trí tuệ ngôi sao công nghệ không tên0.96(WIFI)', 48, 1, NOW(), 1, NOW()),
(101049, 101, 'Trí tuệ ngôi sao công nghệ không tên0.96(ML307)', 'xingzhi-cube-0.96oled-ml307', 'Trí tuệ ngôi sao công nghệ không tên0.96(ML307)', 49, 1, NOW(), 1, NOW()),
(101050, 101, 'Trí tuệ ngôi sao công nghệ không tên1.54(WIFI)', 'xingzhi-cube-1.54tft-wifi', 'Trí tuệ ngôi sao công nghệ không tên1.54(WIFI)', 50, 1, NOW(), 1, NOW()),
(101051, 101, 'Trí tuệ ngôi sao công nghệ không tên1.54(ML307)', 'xingzhi-cube-1.54tft-ml307', 'Trí tuệ ngôi sao công nghệ không tên1.54(ML307)', 51, 1, NOW(), 1, NOW()),
(101052, 101, 'SenseCAP Watcher', 'sensecap-watcher', 'SenseCAP Watcher', 52, 1, NOW(), 1, NOW()),
(101053, 101, 'Sibo ZhilianAIhộp đồng hành', 'doit-s3-aibox', 'Sibo ZhilianAIhộp đồng hành', 53, 1, NOW(), 1, NOW()),
(101054, 101, 'Nguyên Không·tuổi trẻ', 'mixgo-nova', 'Nguyên Không·tuổi trẻ', 54, 1, NOW(), 1, NOW());
