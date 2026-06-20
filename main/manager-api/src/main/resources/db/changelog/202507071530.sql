-- Thêm nhà cung cấp TTS phát trực tuyến trên nền tảng đám mây của Alibaba
delete from `ai_model_provider` where id = 'SYSTEM_TTS_AliyunStreamTTS';
INSERT INTO `ai_model_provider` (`id`, `model_type`, `provider_code`, `name`, `fields`, `sort`, `creator`, `create_date`, `updater`, `update_date`) VALUES
('SYSTEM_TTS_AliyunStreamTTS', 'TTS', 'aliyun_stream', 'Tổng hợp giọng nói trên nền tảng đám mây của Alibaba(phát trực tuyến)', '[{"key":"appkey","label":"ứng dụngAppKey","type":"string"},{"key":"token","label":"tạm thờiToken","type":"string"},{"key":"access_key_id","label":"AccessKey ID","type":"string"},{"key":"access_key_secret","label":"AccessKey Secret","type":"string"},{"key":"host","label":"Địa chỉ dịch vụ","type":"string"},{"key":"voice","label":"Âm thanh mặc định","type":"string"},{"key":"format","label":"định dạng âm thanh","type":"string"},{"key":"sample_rate","label":"Tốc độ lấy mẫu","type":"number"},{"key":"volume","label":"khối lượng","type":"number"},{"key":"speech_rate","label":"tốc độ nói","type":"number"},{"key":"pitch_rate","label":"cao độ","type":"number"},{"key":"output_dir","label":"Thư mục đầu ra","type":"string"}]', 15, 1, NOW(), 1, NOW());

-- Thêm cấu hình mô hình TTS phát trực tuyến trên nền tảng đám mây của Alibaba
delete from `ai_model_config` where id = 'TTS_AliyunStreamTTS';
INSERT INTO `ai_model_config` VALUES ('TTS_AliyunStreamTTS', 'TTS', 'AliyunStreamTTS', 'Tổng hợp giọng nói trên nền tảng đám mây của Alibaba(phát trực tuyến)', 0, 1, '{\"type\": \"aliyun_stream\", \"appkey\": \"\", \"token\": \"\", \"access_key_id\": \"\", \"access_key_secret\": \"\", \"host\": \"nls-gateway-cn-beijing.aliyuncs.com\", \"voice\": \"longxiaochun\", \"format\": \"pcm\", \"sample_rate\": 16000, \"volume\": 50, \"speech_rate\": 0, \"pitch_rate\": 0, \"output_dir\": \"tmp/\"}', NULL, NULL, 18, NULL, NULL, NULL, NULL);

-- Đã cập nhật hướng dẫn cấu hình TTS phát trực tuyến trên nền tảng đám mây của Alibaba
UPDATE `ai_model_config` SET 
`doc_link` = 'https://nls-portal.console.aliyun.com/',
`remark` = 'Truyền phát trực tuyến trên nền tảng đám mây của AlibabaTTSHướng dẫn cấu hình：
1. Đám mây của AlibabaTTSvà Đám mây của Alibaba(phát trực tuyến)TTSSự khác biệt là：Đám mây của AlibabaTTSĐó là sự tổng hợp một lần，Đám mây của Alibaba(phát trực tuyến)TTSlà tổng hợp phát trực tuyến thời gian thực
2. phát trực tuyếnTTSCó độ trễ thấp hơn và hiệu suất thời gian thực tốt hơn，Thích hợp cho các tình huống tương tác bằng giọng nói
3. Bạn cần tạo một ứng dụng trong Bảng điều khiển tương tác giọng nói thông minh trên nền tảng đám mây của Alibaba và lấy thông tin xác thực.
4. hỗ trợCosyVoiceÂm thanh mô hình lớn，Chất lượng âm thanh tự nhiên hơn
5. Hỗ trợ điều chỉnh âm lượng theo thời gian thực、tốc độ nói、Giai điệu và các thông số khác
Các bước ứng dụng：
1. chuyến thăm https://nls-portal.console.aliyun.com/ Kích hoạt dịch vụ tương tác giọng nói thông minh
2. chuyến thăm https://nls-portal.console.aliyun.com/applist Tạo dự án và nhậnappkey
3. chuyến thăm https://nls-portal.console.aliyun.com/overview Nhận tạm thờitoken（hoặc cấu hìnhaccess_key_idvàaccess_key_secretNhận tự động）
4. Nếu bạn cần cập nhậttokenquản lý，Cấu hình đề xuấtaccess_key_idvàaccess_key_secret
5. Bạn có thể chọn Bắc Kinh、Máy chủ ở các khu vực khác nhau như Thượng Hải để tối ưu hóa độ trễ
6. voiceHỗ trợ thông sốCosyVoiceÂm thanh mô hình lớn，Chẳng hạn nhưlongxiaochun、longyueyueĐợi đã
Để biết thêm cấu hình tham số，Vui lòng tham khảo：https://help.aliyun.com/zh/isi/developer-reference/real-time-speech-synthesis
' WHERE `id` = 'TTS_AliyunStreamTTS';

-- Thêm âm thanh TTS phát trực tuyến trên nền tảng đám mây của Alibaba
delete from `ai_tts_voice` where tts_model_id = 'TTS_AliyunStreamTTS';
-- Dòng giọng nữ nhẹ nhàng
INSERT INTO `ai_tts_voice` VALUES ('TTS_AliyunStreamTTS_0001', 'TTS_AliyunStreamTTS', 'Long Tiểu Xuân-chị dịu dàng', 'longxiaochun', 'Tiếng Trung và tiếng Trung và tiếng Anh hỗn hợp', NULL, NULL, NULL, NULL, 1, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_AliyunStreamTTS_0002', 'TTS_AliyunStreamTTS', 'Long Tiểu Hạ-Giọng nữ nhẹ nhàng', 'longxiaoxia', 'Tiếng Trung và tiếng Trung và tiếng Anh hỗn hợp', NULL, NULL, NULL, NULL, 2, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_AliyunStreamTTS_0003', 'TTS_AliyunStreamTTS', 'Long Mai-Giọng nữ nhẹ nhàng', 'longmei', 'Tiếng Trung và tiếng Trung và tiếng Anh hỗn hợp', NULL, NULL, NULL, NULL, 3, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_AliyunStreamTTS_0004', 'TTS_AliyunStreamTTS', 'hoa hồng rồng-Giọng nữ nhẹ nhàng', 'longgui', 'Tiếng Trung và tiếng Trung và tiếng Anh hỗn hợp', NULL, NULL, NULL, NULL, 4, NULL, NULL, NULL, NULL);
-- Dòng giọng nữ Royal Sister
INSERT INTO `ai_tts_voice` VALUES ('TTS_AliyunStreamTTS_0005', 'TTS_AliyunStreamTTS', 'ngọc rồng-Giọng nữ hoàng gia', 'longyu', 'Tiếng Trung và tiếng Trung và tiếng Anh hỗn hợp', NULL, NULL, NULL, NULL, 5, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_AliyunStreamTTS_0006', 'TTS_AliyunStreamTTS', 'Long Giao-Giọng nữ hoàng gia', 'longjiao', 'Tiếng Trung và tiếng Trung và tiếng Anh hỗn hợp', NULL, NULL, NULL, NULL, 6, NULL, NULL, NULL, NULL);
-- Dòng giọng nam
INSERT INTO `ai_tts_voice` VALUES ('TTS_AliyunStreamTTS_0007', 'TTS_AliyunStreamTTS', 'Long Trần-Dịch giọng nam', 'longchen', 'Tiếng Trung và tiếng Trung và tiếng Anh hỗn hợp', NULL, NULL, NULL, NULL, 7, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_AliyunStreamTTS_0008', 'TTS_AliyunStreamTTS', 'Long Tú-giọng nam trẻ', 'longxiu', 'Tiếng Trung và tiếng Trung và tiếng Anh hỗn hợp', NULL, NULL, NULL, NULL, 8, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_AliyunStreamTTS_0009', 'TTS_AliyunStreamTTS', 'rồng cam-chàng trai tỏa nắng', 'longcheng', 'Tiếng Trung và tiếng Trung và tiếng Anh hỗn hợp', NULL, NULL, NULL, NULL, 9, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_AliyunStreamTTS_0010', 'TTS_AliyunStreamTTS', 'Long Triết-giọng nam trưởng thành', 'longzhe', 'Tiếng Trung và tiếng Trung và tiếng Anh hỗn hợp', NULL, NULL, NULL, NULL, 10, NULL, NULL, NULL, NULL);
-- Chuỗi phát sóng chuyên nghiệp
INSERT INTO `ai_tts_voice` VALUES ('TTS_AliyunStreamTTS_0011', 'TTS_AliyunStreamTTS', 'Bella2.0-cô gái bán báo', 'loongbella', 'Tiếng Trung và tiếng Trung và tiếng Anh hỗn hợp', NULL, NULL, NULL, NULL, 11, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_AliyunStreamTTS_0012', 'TTS_AliyunStreamTTS', 'Stella2.0-giọng nữ ngổ ngáo', 'loongstella', 'Tiếng Trung và tiếng Trung và tiếng Anh hỗn hợp', NULL, NULL, NULL, NULL, 12, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_AliyunStreamTTS_0013', 'TTS_AliyunStreamTTS', 'sách rồng-cậu bé bán báo', 'longshu', 'Tiếng Trung và tiếng Trung và tiếng Anh hỗn hợp', NULL, NULL, NULL, NULL, 13, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_AliyunStreamTTS_0014', 'TTS_AliyunStreamTTS', 'Long Tỉnh-giọng nữ nghiêm túc', 'longjing', 'Tiếng Trung và tiếng Trung và tiếng Anh hỗn hợp', NULL, NULL, NULL, NULL, 14, NULL, NULL, NULL, NULL);
-- Dòng giai điệu nổi bật
INSERT INTO `ai_tts_voice` VALUES ('TTS_AliyunStreamTTS_0015', 'TTS_AliyunStreamTTS', 'Long Kỳ-Giọng trẻ thơ sống động', 'longqi', 'Tiếng Trung và tiếng Trung và tiếng Anh hỗn hợp', NULL, NULL, NULL, NULL, 15, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_AliyunStreamTTS_0016', 'TTS_AliyunStreamTTS', 'long hoa-cô gái sôi nổi', 'longhua', 'Tiếng Trung và tiếng Trung và tiếng Anh hỗn hợp', NULL, NULL, NULL, NULL, 16, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_AliyunStreamTTS_0017', 'TTS_AliyunStreamTTS', 'Long Vũ-giọng nam vô nghĩa', 'longwu', 'Tiếng Trung và tiếng Trung và tiếng Anh hỗn hợp', NULL, NULL, NULL, NULL, 17, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_AliyunStreamTTS_0018', 'TTS_AliyunStreamTTS', 'Búa tạ rồng-Giọng nam hài hước', 'longdachui', 'Tiếng Trung và tiếng Trung và tiếng Anh hỗn hợp', NULL, NULL, NULL, NULL, 18, NULL, NULL, NULL, NULL);
-- Dòng tiếng Quảng Đông
INSERT INTO `ai_tts_voice` VALUES ('TTS_AliyunStreamTTS_0019', 'TTS_AliyunStreamTTS', 'Long Gia Nhất-Giọng nữ Quảng Đông', 'longjiayi', 'Hỗn hợp tiếng Quảng Đông và tiếng Quảng Đông-Anh', NULL, NULL, NULL, NULL, 19, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_AliyunStreamTTS_0020', 'TTS_AliyunStreamTTS', 'đào rồng-Giọng nữ Quảng Đông', 'longtao', 'Hỗn hợp tiếng Quảng Đông và tiếng Quảng Đông-Anh', NULL, NULL, NULL, NULL, 20, NULL, NULL, NULL, NULL);
