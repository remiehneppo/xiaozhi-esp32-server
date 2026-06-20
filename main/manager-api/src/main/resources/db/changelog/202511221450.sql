-- Cập nhật cấu hình nhà cung cấp HuoshanDoubleStreamTTS và thêm tùy chọn cho phép sử dụng lại liên kết
UPDATE `ai_model_provider`
SET fields = '[{"key": "ws_url", "type": "string", "label": "WebSocketđịa chỉ"}, {"key": "appid", "type": "string", "label": "ứng dụngID"}, {"key": "access_token", "type": "string", "label": "mã thông báo truy cập"}, {"key": "resource_id", "type": "string", "label": "Tài nguyênID"}, {"key": "speaker", "type": "string", "label": "Âm thanh mặc định"}, {"key": "enable_ws_reuse", "type": "boolean", "label": "Có bật tái sử dụng liên kết hay không", "default": true}, {"key": "speech_rate", "type": "number", "label": "tốc độ nói(-50~100)"}, {"key": "loudness_rate", "type": "number", "label": "khối lượng(-50~100)"}, {"key": "pitch", "type": "number", "label": "cao độ(-12~12)"}]'
WHERE id = 'SYSTEM_TTS_HSDSTTS';

UPDATE `ai_model_config` SET 
`doc_link` = 'https://console.volcengine.com/speech/service/10007',
`remark` = 'Hướng dẫn cấu hình dịch vụ tổng hợp giọng nói động cơ núi lửa：
1. chuyến thăm https://www.volcengine.com/ Đăng ký và mở tài khoản Volcano Engine
2. chuyến thăm https://console.volcengine.com/speech/service/10007 Mô hình lớn tổng hợp giọng nói mở，Mua âm thanh
3. Lấy nó ở cuối trangappidvàaccess_token
5. Tài nguyênIDcố định vào：volc.service_type.10029（Tổng hợp và trộn giọng nói mô hình lớn）
6. Tái sử dụng liên kết：bật lênWebSocketTái sử dụng kết nối，Mặc địnhtrueGiảm mất liên kết（Lưu ý：Sau khi sử dụng lại, khi thiết bị ở trạng thái lắng nghe, các liên kết nhàn rỗi sẽ chiếm số lượng kết nối đồng thời.）
7. tốc độ nói：-50~100，Có thể để trống，mặc định bình thường0，Có thể điền vào-50~100
8. khối lượng：-50~100，Có thể để trống，mặc định bình thường0，Có thể điền vào-50~100
9. cao độ：-12~12，Có thể để trống，mặc định bình thường0，Có thể điền vào-12~12
10. Điền vào tập tin cấu hình' WHERE `id` = 'TTS_HuoshanDoubleStreamTTS';