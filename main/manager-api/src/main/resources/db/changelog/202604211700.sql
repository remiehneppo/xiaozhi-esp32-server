-- Khắc phục sự cố trùng lặp của nhà cung cấp_code trong mô hình tổng hợp giọng nói Doubao 2.0 và thêm hỗ trợ ASR 2.0

-- ===================== Mô hình tổng hợp giọng nói Doubao 2.0 ======================
-- Đã xóa nhà cung cấp TTS 2.0 (không cần nhà cung cấp riêng nữa)
delete from `ai_model_provider` where id = 'SYSTEM_TTS_HSDSTTS_V2';

-- ===================== Nhận dạng giọng nói Doubao (Truyền phát) ======================
-- Sửa đổi nhà cung cấp nhận dạng giọng nói (phát trực tuyến) Doubao ban đầu, xóa trường cụm và thêm trường Resource_id
UPDATE `ai_model_provider` SET `fields` = '[{"key":"appid","type":"string","label":"ứng dụngID"},{"key":"access_token","type":"string","label":"mã thông báo truy cập"},{"key":"boosting_table_name","type":"string","label":"Tên file từ nóng"},{"key":"correct_table_name","type":"string","label":"Thay thế tên file word"},{"key":"output_dir","type":"string","label":"Thư mục đầu ra"},{"key":"end_window_size","type":"number","label":"Thời gian phán xét im lặng(ms)"},{"key":"enable_multilingual","type":"boolean","label":"Có bật chế độ nhận dạng đa ngôn ngữ hay không"},{"key":"language","type":"string","label":"Chỉ định mã hóa ngôn ngữ"},{"key":"resource_id","type":"string","label":"Tài nguyênID"}]' WHERE `id` = 'SYSTEM_ASR_DoubaoStreamASR';

-- Sửa cấu hình nhận dạng giọng nói (phát trực tuyến) ban đầu của Doubao, xóa trường cụm và thêm giá trị mặc định của Resource_id
UPDATE `ai_model_config` SET `config_json` = JSON_REMOVE(JSON_SET(`config_json`, '$.resource_id', 'volc.bigasr.sauc.duration'), '$.cluster') WHERE `id` = 'ASR_DoubaoStreamASR';

-- ===================== Mô hình nhận dạng giọng nói Doubao 2.0 ======================

-- Chèn cấu hình mô hình nhận dạng giọng nói Beanbao 2.0
delete from `ai_model_config` where id = 'ASR_DoubaoStreamASRV2';
INSERT INTO `ai_model_config` VALUES ('ASR_DoubaoStreamASRV2', 'ASR', 'DoubaoStreamASRV2', 'Mô hình nhận dạng giọng nói Beanbao2.0', 0, 1, '{
  "type": "doubao_stream",
  "appid": "",
  "access_token": "",
  "resource_id": "volc.seedasr.sauc.duration",
  "end_window_size": 200,
  "enable_multilingual": false,
  "language": "zh-CN",
  "output_dir": "tmp/"
}', NULL, NULL, 6, NULL, NULL, NULL, NULL);

-- Tài liệu cấu hình mô hình nhận dạng giọng nói Doubao 2.0
UPDATE `ai_model_config` SET
`doc_link` = 'https://www.volcengine.com/docs/6561/109979',
`remark` = 'Mô hình nhận dạng giọng nói Beanbao2.0Hướng dẫn cấu hình（Dựa trên động cơ núi lửaseed-asr）：
1. chuyến thăm https://www.volcengine.com/ Đăng ký và mở tài khoản Volcano Engine
2. chuyến thăm https://console.volcengine.com/speech/service/10038 Kích hoạt mô hình nhận dạng giọng nói trực tuyến Doubao2.0
3. Lấy nó ở cuối trangappidvàaccess_token
4. Tài nguyênIDCó hai loại：Phiên bản hàng giờ（volc.seedasr.sauc.duration）và phiên bản đồng thời（volc.seedasr.sauc.concurrent）
   - Phiên bản hàng giờ：cố định vào：volc.seedasr.sauc.duration（Mô hình nhận dạng giọng nói Beanbao2.0）
   - Phiên bản đồng thời：cố định vào：volc.seedasr.sauc.concurrent（Mô hình nhận dạng giọng nói Beanbao2.0）

Tài liệu tham số chi tiết：https://www.volcengine.com/docs/6561/109979

Lưu ý：
- Mô hình nhận dạng giọng nói Beanbao2.0sử dụngvolc.seedasr.sauc.durationTài nguyênID，Nhận dạng giọng nói bằng túi đậu(phát trực tuyến)（volc.bigasr.sauc.duration）khác nhau
- mô hình nhận dạng giọng nói2.0giá rẻ hơn，Nên sử dụng tài nguyên phiên bản đồng thời trong các tình huống có tính tương tranh caoID
' WHERE `id` = 'ASR_DoubaoStreamASRV2';
