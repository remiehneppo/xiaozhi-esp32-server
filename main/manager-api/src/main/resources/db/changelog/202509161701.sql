-- Thêm nhà cung cấp TTS phát trực tuyến Bailian của Alibaba
delete from `ai_model_provider` where id = 'SYSTEM_TTS_AliBLStreamTTS';
INSERT INTO `ai_model_provider` (`id`, `model_type`, `provider_code`, `name`, `fields`, `sort`, `creator`, `create_date`, `updater`, `update_date`) VALUES
('SYSTEM_TTS_AliBLStreamTTS', 'TTS', 'alibl_stream', 'Tổng hợp bài phát biểu trực tuyến của Alibaba Bailian', '[{"key":"api_key","label":"APIchìa khóa","type":"string"},{"key":"output_dir","label":"Thư mục đầu ra","type":"string"},{"key":"model","label":"người mẫu","type":"string"},{"key":"voice","label":"âm sắc","type":"string"},{"key":"format","label":"định dạng âm thanh","type":"string"},{"key":"sample_rate","label":"Tốc độ lấy mẫu","type":"number"},{"key": "volume", "type": "number", "label": "khối lượng"},{"key": "rate", "type": "number", "label": "tốc độ nói"},{"key": "pitch", "type": "number", "label": "cao độ"}]', 19, 1, NOW(), 1, NOW());

-- Thêm cấu hình mô hình TTS phát trực tuyến của Alibaba Bailian
delete from `ai_model_config` where id = 'TTS_AliBLStreamTTS';
INSERT INTO `ai_model_config` VALUES ('TTS_AliBLStreamTTS', 'TTS', 'AliBLStreamTTS', 'Tổng hợp bài phát biểu trực tuyến của Alibaba Bailian', 0, 1, '{\"type\": \"alibl_stream\", \"appkey\": \"\", \"output_dir\": \"tmp/\", \"model\": \"cosyvoice-v2\", \"voice\": \"longcheng_v2\", \"format\": \"pcm\", \"sample_rate\": 24000, \"volume\": 50, \"rate\": 1, \"pitch\": 1}', NULL, NULL, 22, NULL, NULL, NULL, NULL);

-- Đã cập nhật hướng dẫn cấu hình TTS phát trực tuyến của Alibaba Bailian
UPDATE `ai_model_config` SET 
`doc_link` = 'https://bailian.console.aliyun.com/?apiKey=1#/api-key',
`remark` = 'Phong cách dòng chảy Ali BailianTTSMô tả：
1. chuyến thăm https://bailian.console.aliyun.com/?apiKey=1#/api-key Tạo dự án và nhậnappkey
2. Hỗ trợ tổng hợp phát trực tuyến theo thời gian thực，Có độ trễ thấp hơn
3. Hỗ trợ nhiều cài đặt âm thanh và điều chỉnh thông số âm thanh
4. hỗ trợCosyVoice-V3Âm thanh mô hình lớn，Giá cả phải chăng(0.4Nhân dân tệ/chữ Vạn)
5. Hỗ trợ điều chỉnh âm lượng theo thời gian thực、tốc độ nói、Giai điệu và các thông số khác
6. Nếu cần sử dụngCosyVoice-V3mô hình và một số loại âm thanh bị hạn chế，Bạn cần liên hệ với bộ phận chăm sóc khách hàng của Alibaba Bailian để đăng ký
' WHERE `id` = 'TTS_AliBLStreamTTS';

-- Thêm âm thanh TTS phát trực tuyến Ali Bailian
delete from `ai_tts_voice` where tts_model_id = 'TTS_AliBLStreamTTS';

-- trợ lý giọng nói
INSERT INTO `ai_tts_voice` VALUES ('TTS_AliBLStreamTTS_0001', 'TTS_AliBLStreamTTS', 'Long Tiểu Xuân-Người phụ nữ trí tuệ và tích cực', 'longxiaochun_v2', 'Tiếng Trung và tiếng Trung và tiếng Anh hỗn hợp', NULL, NULL, NULL, NULL, 1, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_AliBLStreamTTS_0002', 'TTS_AliBLStreamTTS', 'Long Tiểu Hạ-Người phụ nữ điềm tĩnh và uy quyền', 'longxiaoxia_v2', 'Tiếng Trung và tiếng Trung và tiếng Anh hỗn hợp', NULL, NULL, NULL, NULL, 2, NULL, NULL, NULL, NULL);

-- Giao hàng trực tiếp
INSERT INTO `ai_tts_voice` VALUES ('TTS_AliBLStreamTTS_0003', 'TTS_AliBLStreamTTS', 'Long An Nhiên-Phụ nữ năng động và gợi cảm', 'longanran', 'Tiếng Trung và tiếng Trung và tiếng Anh hỗn hợp', NULL, NULL, NULL, NULL, 3, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_AliBLStreamTTS_0004', 'TTS_AliBLStreamTTS', 'Long An Xuân-Nữ phát sóng trực tiếp cổ điển', 'longanxuan', 'Tiếng Trung và tiếng Trung và tiếng Anh hỗn hợp', NULL, NULL, NULL, NULL, 4, NULL, NULL, NULL, NULL);

-- tình bạn xã hội
INSERT INTO `ai_tts_voice` VALUES ('TTS_AliBLStreamTTS_0005', 'TTS_AliBLStreamTTS', 'Long Hán-Người đàn ông ấm áp và say đắm', 'longhan_v2', 'Tiếng Trung và tiếng Trung và tiếng Anh hỗn hợp', NULL, NULL, NULL, NULL, 5, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_AliBLStreamTTS_0006', 'TTS_AliBLStreamTTS', 'Long Nham-Cô gái gió xuân ấm áp', 'longyan_v2', 'Tiếng Trung và tiếng Trung và tiếng Anh hỗn hợp', NULL, NULL, NULL, NULL, 6, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_AliBLStreamTTS_0007', 'TTS_AliBLStreamTTS', 'Long Phi Phi-Cô gái ngọt ngào và đạo đức giả', 'longfeifei_v2', 'Tiếng Trung và tiếng Trung và tiếng Anh hỗn hợp', NULL, NULL, NULL, NULL, 7, NULL, NULL, NULL, NULL);

-- phương ngữ
INSERT INTO `ai_tts_voice` VALUES ('TTS_AliBLStreamTTS_0008', 'TTS_AliBLStreamTTS', 'Long Lào Thiết-Người thẳng thắn Đông Bắc', 'longlaotie_v2', 'Tiếng Trung(Đông Bắc)và hỗn hợp tiếng Trung và tiếng Anh', NULL, NULL, NULL, NULL, 8, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_AliBLStreamTTS_0009', 'TTS_AliBLStreamTTS', 'Long Gia Nhất-Nữ trí thức Quảng Đông', 'longjiayi_v2', 'Tiếng Trung(tiếng Quảng Đông)và hỗn hợp tiếng Trung và tiếng Anh', NULL, NULL, NULL, NULL, 9, NULL, NULL, NULL, NULL);

-- giọng nói của đứa trẻ
INSERT INTO `ai_tts_voice` VALUES ('TTS_AliBLStreamTTS_0010', 'TTS_AliBLStreamTTS', 'Long giới Lidou-chàng trai nghịch ngợm đầy nắng', 'longjielidou_v2', 'Tiếng Trung và tiếng Trung và tiếng Anh hỗn hợp', NULL, NULL, NULL, NULL, 10, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_AliBLStreamTTS_0011', 'TTS_AliBLStreamTTS', 'chuông rồng-Cô gái trẻ con và ngốc nghếch', 'longling_v2', 'Tiếng Trung và tiếng Trung và tiếng Anh hỗn hợp', NULL, NULL, NULL, NULL, 11, NULL, NULL, NULL, NULL);

-- ngâm thơ
INSERT INTO `ai_tts_voice` VALUES ('TTS_AliBLStreamTTS_0012', 'TTS_AliBLStreamTTS', 'Lý Bạch-Tiên nhân thơ cổ', 'libai_v2', 'Tiếng Trung và tiếng Trung và tiếng Anh hỗn hợp', NULL, NULL, NULL, NULL, 12, NULL, NULL, NULL, NULL);

-- Tiếp thị ở nước ngoài
INSERT INTO `ai_tts_voice` VALUES ('TTS_AliBLStreamTTS_0013', 'TTS_AliBLStreamTTS', 'loongeva-Nữ trí thức Anh', 'loongeva_v2', 'Tiếng Anh của người Anh', NULL, NULL, NULL, NULL, 13, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_AliBLStreamTTS_0014', 'TTS_AliBLStreamTTS', 'loongbrian-Người đàn ông nói tiếng Anh bình tĩnh', 'loongbrian_v2', 'Tiếng Anh của người Anh', NULL, NULL, NULL, NULL, 14, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_AliBLStreamTTS_0015', 'TTS_AliBLStreamTTS', 'loongkyong-nữ Hàn Quốc', 'loongkyong_v2', 'Tiếng Hàn', NULL, NULL, NULL, NULL, 15, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_AliBLStreamTTS_0016', 'TTS_AliBLStreamTTS', 'loongtomoka-phụ nữ nhật bản', 'loongtomoka_v2', 'tiếng Nhật', NULL, NULL, NULL, NULL, 16, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_AliBLStreamTTS_0017', 'TTS_AliBLStreamTTS', 'loongtomoya-nam giới nhật bản', 'loongtomoya_v2', 'tiếng Nhật', NULL, NULL, NULL, NULL, 17, NULL, NULL, NULL, NULL);