delete from `ai_model_config` where id = 'LLM_XunfeiSparkLLM';
INSERT INTO `ai_model_config` VALUES ('LLM_XunfeiSparkLLM', 'LLM', 'Mô hình lớn nhận thức iFlytek Spark', 'Mô hình lớn nhận thức iFlytek Spark', 0, 1, '{"type": "openai", "model_name": "generalv3.5", "base_url": "https://spark-api-open.xf-yun.com/v1", "api_password": "của bạnapi_password", "temperature": 0.5, "max_tokens": 2048, "top_p": 1.0, "frequency_penalty": 0.0}', 'https://www.xfyun.cn/doc/spark/HTTP%E8%B0%83%E7%94%A8%E6%96%87%E6%A1%A3.html', 'Mô hình lớn nhận thức iFlytek Spark，Hỗ trợ nhiều vòng đối thoại、Tạo văn bản và các chức năng khác', 14, NULL, NULL, NULL, NULL);

-- Tài liệu cập nhật cho cấu hình mô hình lớn nhận thức của iFlytek Spark
UPDATE `ai_model_config` SET
`doc_link` = 'https://www.xfyun.cn/doc/spark/HTTP%E8%B0%83%E7%94%A8%E6%96%87%E6%A1%A3.html',
`remark` = 'Hướng dẫn cấu hình mô hình lớn nhận thức iFlytek Spark：
1. Đăng nhập vào nền tảng mở iFlytek https://www.xfyun.cn/，Mỗi mô hình tương ứng với mỗiapi_password,Khi thay đổi model cần kiểm tra model tương ứngapi_password
2. Tạo ứng dụng mô hình lớn nhận thức Spark Nhận đượcAPI Password
3. Mô tả thông số：
   - api_password: API Password，Nhận được sau khi tạo ứng dụng trên nền tảng mở iFlytek
   - model_name: Tên mẫu，hỗ trợgeneralv3.5、generalv3Các phiên bản khác
   - base_url: APIđịa chỉ，Mặc địnhhttps://spark-api-open.xf-yun.com/v1
   - temperature: Thông số nhiệt độ，Kiểm soát tính ngẫu nhiên của thế hệ，phạm vi0-1，Mặc định0.5
   - max_tokens: sản lượng tối đatokencon số，Mặc định2048
   - top_p: Thông số lấy mẫu lõi，Kiểm soát sự đa dạng từ vựng，Mặc định1.0
   - frequency_penalty: hình phạt tần số，Giảm nội dung trùng lặp，Mặc định0.0
4. Mỗi mô hình tương ứng với mỗiapi_password,Khi thay đổi model cần kiểm tra model tương ứngapi_password。
' WHERE `id` = 'LLM_XunfeiSparkLLM';