-- Thêm cấu hình dịch vụ nhận dạng giọng nói trực tuyến iFlytek
delete from `ai_model_provider` where id = 'SYSTEM_ASR_XunfeiStream';
INSERT INTO `ai_model_provider` (`id`, `model_type`, `provider_code`, `name`, `fields`, `sort`, `creator`, `create_date`, `updater`, `update_date`) VALUES
('SYSTEM_ASR_XunfeiStream', 'ASR', 'xunfei_stream', 'Nhận dạng giọng nói trực tuyến iFlytek', '[{"key":"app_id","label":"ứng dụngID","type":"string"},{"key":"api_key","label":"API_KEY","type":"password"},{"key":"api_secret","label":"API_SECRET","type":"password"},{"key":"domain","label":"Xác định khu vực","type":"string"},{"key":"language","label":"Xác định ngôn ngữ","type":"string"},{"key":"accent","label":"phương ngữ","type":"string"},{"key":"dwa","label":"hiệu chỉnh động","type":"string"},{"key":"output_dir","label":"Thư mục đầu ra","type":"string"}]', 18, 1, NOW(), 1, NOW());

delete from `ai_model_config` where id = 'ASR_XunfeiStream';
INSERT INTO `ai_model_config` VALUES ('ASR_XunfeiStream', 'ASR', 'Nhận dạng giọng nói trực tuyến iFlytek', 'Dịch vụ nhận dạng giọng nói trực tuyến iFlytek', 0, 1, '{"type": "xunfei_stream", "app_id": "", "api_key": "", "api_secret": "", "domain": "slm", "language": "zh_cn", "accent": "mandarin", "dwa": "wpgs", "output_dir": "tmp/"}', 'https://www.xfyun.cn/doc/spark/spark_zh_iat.html', 'Hỗ trợ nhận dạng giọng nói trực tuyến theo thời gian thực，Thích hợp cho tiếng Quan Thoại và nhận dạng nhiều phương ngữ', 21, NULL, NULL, NULL, NULL);

-- Tài liệu cập nhật về cấu hình mô hình nhận dạng giọng nói trực tuyến iFlytek
UPDATE `ai_model_config` SET
`doc_link` = 'https://www.xfyun.cn/doc/spark/spark_zh_iat.html',
`remark` = 'Hướng dẫn cấu hình nhận dạng giọng nói trực tuyến iFlytek：
1. Đăng nhập vào nền tảng mở iFlytek https://www.xfyun.cn/
2. Tạo một ứng dụng nhận dạng giọng nói để có đượcAPPID、APISecret、APIKey
3. Mô tả thông số：
   - app_id: ứng dụngID，Nhận được sau khi tạo ứng dụng trên nền tảng mở iFlytek
   - api_key: APIchìa khóa，Được sử dụng để xác thực giao diện
   - api_secret: APIchìa khóa，được sử dụng để tạo chữ ký
   - domain: Xác định khu vực，Mặc địnhslm（Phiên âm giọng nói thông minh）
   - language: Xác định ngôn ngữ，Mặc địnhzh_cn（Tiếng Trung）
   - accent: kiểu phương ngữ，Mặc địnhmandarin（tiếng quan thoại），hỗ trợcantonese（tiếng Quảng Đông）Đợi đã
   - dwa: hiệu chỉnh động，Mặc địnhwpgs（Bật hiệu chỉnh động）
   - output_dir: Thư mục đầu ra tập tin âm thanh，Mặc địnhtmp/
4. Hỗ trợ nhận dạng phát trực tuyến theo thời gian thực，Thích hợp cho các tình huống tương tác bằng giọng nói theo thời gian thực
5. Hỗ trợ nhiều phương ngữ và nhận dạng ngôn ngữ
' WHERE `id` = 'ASR_XunfeiStream';