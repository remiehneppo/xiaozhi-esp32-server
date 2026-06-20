-- Thêm nhà cung cấp TTS phát trực tuyến iFlytek
delete from `ai_model_provider` where id = 'SYSTEM_TTS_XunFeiStreamTTS';
INSERT INTO `ai_model_provider` (`id`, `model_type`, `provider_code`, `name`, `fields`, `sort`, `creator`, `create_date`, `updater`, `update_date`) VALUES
('SYSTEM_TTS_XunFeiStreamTTS', 'TTS', 'xunfei_stream', 'Tổng hợp giọng nói trực tuyến iFlytek', '[{"key":"app_id","label":"APP_ID","type":"string"},{"key":"api_secret","label":"API_Secret","type":"string"},{"key":"api_key","label":"APIchìa khóa","type":"string"},{"key":"output_dir","label":"Thư mục đầu ra","type":"string"},{"key":"voice","label":"âm sắc","type":"string"},{"key":"format","label":"định dạng âm thanh","type":"string"},{"key":"sample_rate","label":"Tốc độ lấy mẫu","type":"number"},{"key": "volume", "type": "number", "label": "khối lượng"},{"key": "speed", "type": "number", "label": "tốc độ nói"},{"key": "pitch", "type": "number", "label": "cao độ"},{"key": "oral_level", "type": "number", "label": "mức độ thông tục"},{"key": "spark_assist", "type": "number", "label": "Nó có phải là thông tục không?"},{"key": "stop_split", "type": "number", "label": "Tách câu phía máy chủ"},{"key": "remain", "type": "number", "label": "giữ lại ngôn ngữ viết"}]', 20, 1, NOW(), 1, NOW());

-- Thêm cấu hình mô hình TTS phát trực tuyến iFlytek
delete from `ai_model_config` where id = 'TTS_XunFeiStreamTTS';
INSERT INTO `ai_model_config` VALUES ('TTS_XunFeiStreamTTS', 'TTS', 'XunFeiStreamTTS', 'Tổng hợp giọng nói trực tuyến iFlytek', 0, 1, '{\"type\": \"xunfei_stream\", \"app_id\": \"\", \"api_secret\": \"\", \"api_key\": \"\", \"output_dir\": \"tmp/\", \"voice\": \"x5_lingxiaoxuan_flow\", \"format\": \"raw\", \"sample_rate\": 24000, \"volume\": 50, \"speed\": 50, \"pitch\": 50, \"oral_level\": \"mid\", \"spark_assist\": 1, \"stop_split\": 0, \"remain\": 0}', NULL, NULL, 23, NULL, NULL, NULL, NULL);

-- Đã cập nhật hướng dẫn cấu hình TTS phát trực tuyến iFlytek
UPDATE `ai_model_config` SET 
`doc_link` = 'https://console.xfyun.cn/app/myapp',
`remark` = 'phát trực tuyến iFlytekTTSMô tả：
1. Đăng nhập vào Nền tảng công nghệ giọng nói iFlytek https://console.xfyun.cn/app/myapp Tạo ứng dụng liên quan
2. Chọn các dịch vụ bạn cần nhậnapiCấu hình liên quan https://console.xfyun.cn/services/uts
3. Đối với các ứng dụng cần sử dụng(APPID)Mua các dịch vụ liên quan Ví dụ：Tổng hợp siêu hình người https://console.xfyun.cn/services/uts
5. Hỗ trợ giao tiếp hai luồng thời gian thực，Có độ trễ thấp hơn
6. Hỗ trợ cài đặt ngôn ngữ nói và điều chỉnh thông số âm thanh Lưu ý：V5Âm sắc không hỗ trợ các cấu hình thông tục liên quan
7. Hỗ trợ điều chỉnh âm lượng theo thời gian thực、tốc độ nói、Giai điệu và các thông số khác
' WHERE `id` = 'TTS_XunFeiStreamTTS';

-- Thêm âm thanh TTS phát trực tuyến của iFlytek
delete from `ai_tts_voice` where tts_model_id = 'TTS_XunFeiStreamTTS';

-- Vai trò cơ bản
INSERT INTO `ai_tts_voice` VALUES ('TTS_XunFeiStreamTTS_0001', 'TTS_XunFeiStreamTTS', 'Ling Xiaoxuan', 'x5_lingxiaoxuan_flow', 'Tiếng Trung', NULL, NULL, NULL, NULL, 1, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_XunFeiStreamTTS_0002', 'TTS_XunFeiStreamTTS', 'Hãy nghe Feiyi', 'x5_lingfeiyi_flow', 'Tiếng Trung', NULL, NULL, NULL, NULL, 2, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_XunFeiStreamTTS_0003', 'TTS_XunFeiStreamTTS', 'Hãy nghe Tiểu Nguyệt', 'x5_lingxiaoyue_flow', 'Tiếng Trung', NULL, NULL, NULL, NULL, 3, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_XunFeiStreamTTS_0004', 'TTS_XunFeiStreamTTS', 'Ling Yuzhao', 'x5_lingyuzhao_flow', 'Tiếng Trung', NULL, NULL, NULL, NULL, 4, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_XunFeiStreamTTS_0005', 'TTS_XunFeiStreamTTS', 'nghe lời ngọc', 'x5_lingyuyan_flow', 'Tiếng Trung', NULL, NULL, NULL, NULL, 5, NULL, NULL, NULL, NULL);

-- Cần thêm âm thanh ký tự tương ứng
INSERT INTO `ai_tts_voice` VALUES ('TTS_XunFeiStreamTTS_0006', 'TTS_XunFeiStreamTTS', 'Lăng Phi Triết', 'x4_lingfeizhe_oral', 'Tiếng Trung', NULL, NULL, NULL, NULL, 6, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_XunFeiStreamTTS_0007', 'TTS_XunFeiStreamTTS', 'Ling Xiaoli', 'x4_lingxiaoli_oral', 'Tiếng Trung', NULL, NULL, NULL, NULL, 7, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_XunFeiStreamTTS_0008', 'TTS_XunFeiStreamTTS', 'Hãy nghe Tiểu Đường', 'x5_lingxiaotang_flow', 'Tiếng Trung', NULL, NULL, NULL, NULL, 8, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_XunFeiStreamTTS_0009', 'TTS_XunFeiStreamTTS', 'Lăng Tiểu Thất', 'x4_lingxiaoqi_oral', 'Tiếng Trung', NULL, NULL, NULL, NULL, 9, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_XunFeiStreamTTS_0010', 'TTS_XunFeiStreamTTS', 'Ling Youyou-giọng nói của cô gái thời thơ ấu', 'x4_lingyouyou_oral', 'Tiếng Trung', NULL, NULL, NULL, NULL, 10, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_XunFeiStreamTTS_0011', 'TTS_XunFeiStreamTTS', 'Tử Kim', 'x4_zijin_oral', 'Phương ngữ Thiên Tân', NULL, NULL, NULL, NULL, 11, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_XunFeiStreamTTS_0012', 'TTS_XunFeiStreamTTS', 'Tử Dương', 'x4_ziyang_oral', 'phương ngữ Đông Bắc', NULL, NULL, NULL, NULL, 12, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_XunFeiStreamTTS_0013', 'TTS_XunFeiStreamTTS', 'Grant', 'x5_EnUs_Grant_flow', 'Tiếng Anh', NULL, NULL, NULL, NULL, 13, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_XunFeiStreamTTS_0014', 'TTS_XunFeiStreamTTS', 'Lila', 'x5_EnUs_Lila_flow', 'Tiếng Anh', NULL, NULL, NULL, NULL, 14, NULL, NULL, NULL, NULL);
