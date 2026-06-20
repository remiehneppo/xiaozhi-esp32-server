-- Thêm cấu hình dịch vụ nhận dạng giọng nói theo thời gian thực của Alibaba Bailian Paraformer
delete from `ai_model_provider` where id = 'SYSTEM_ASR_AliyunBLStream';
INSERT INTO `ai_model_provider` (`id`, `model_type`, `provider_code`, `name`, `fields`, `sort`, `creator`, `create_date`, `updater`, `update_date`) VALUES
('SYSTEM_ASR_AliyunBLStream', 'ASR', 'aliyunbl_stream', 'Ali BailianParaformerNhận dạng giọng nói theo thời gian thực', '[{"key":"api_key","label":"APIchìa khóa","type":"password"},{"key":"model","label":"Tên mẫu","type":"string"},{"key":"format","label":"định dạng âm thanh","type":"string"},{"key":"sample_rate","label":"Tốc độ lấy mẫu","type":"number"},{"key":"output_dir","label":"Thư mục đầu ra","type":"string"}]', 18, 1, NOW(), 1, NOW());

delete from `ai_model_config` where id = 'ASR_AliyunBLStream';
INSERT INTO `ai_model_config` VALUES ('ASR_AliyunBLStream', 'ASR', 'AliyunBLStream', 'Ali BailianParaformerNhận dạng giọng nói theo thời gian thực', 0, 1, '{"type": "aliyunbl_stream", "api_key": "", "model": "paraformer-realtime-v2", "format": "pcm", "sample_rate": 16000, "disfluency_removal_enabled": false, "semantic_punctuation_enabled": false, "max_sentence_silence": 200, "multi_threshold_mode_enabled": false, "punctuation_prediction_enabled": true, "inverse_text_normalization_enabled": true, "output_dir": "tmp/"}', 'https://help.aliyun.com/zh/model-studio/websocket-for-paraformer-real-time-service', 'Hỗ trợ nhiều ngôn ngữ、Tùy chỉnh từ nóng、Các tính năng nâng cao như phân đoạn theo ngữ nghĩa', 21, NULL, NULL, NULL, NULL);

-- Tài liệu cập nhật về cấu hình mô hình Alibaba Bailian Paraformer
UPDATE `ai_model_config` SET
`doc_link` = 'https://help.aliyun.com/zh/model-studio/websocket-for-paraformer-real-time-service',
`remark` = 'Ali BailianParaformerHướng dẫn cấu hình nhận dạng giọng nói theo thời gian thực：
1. Đăng nhập vào Nền tảng Bailian trên nền tảng đám mây của Alibaba https://bailian.console.aliyun.com/
2. tạo raAPI-KEY https://bailian.console.aliyun.com/#/api-key
3. Mô hình hỗ trợ：paraformer-realtime-v2(Được đề xuất)、paraformer-realtime-8k-v2、paraformer-realtime-v1、paraformer-realtime-8k-v1
4. Tính năng：
   - Hỗ trợ đa ngôn ngữ(Tiếng Trung với các phương ngữ、Tiếng Anh、tiếng Nhật、Tiếng Hàn、tiếng đức、người Pháp、tiếng Nga)
   - Tùy chỉnh từ nóng(vocabulary_idthông số)，Để biết hướng dẫn chi tiết vui lòng tham khảo：https://help.aliyun.com/zh/model-studio/custom-hot-words?
   - phân đoạn ngữ nghĩa/VADngắt câu(semantic_punctuation_enabledthông số)
   - dấu câu tự động、ITN、Lọc các hạt phương thức, v.v.
5. Mô tả thông số：
   - model: Tên mẫu，Được đề xuấtparaformer-realtime-v2
   - sample_rate: Tốc độ lấy mẫu(Hz)，v2Hỗ trợ mọi tốc độ lấy mẫu，v1Chỉ hỗ trợ16000，8kPhiên bản chỉ hỗ trợ8000
   - semantic_punctuation_enabled: falsechoVADngắt câu(độ trễ thấp)，truePhân đoạn câu theo ngữ nghĩa(Độ chính xác cao)
   - max_sentence_silence: VADNgưỡng thời gian im lặng phân đoạn câu(200-6000ms)
' WHERE `id` = 'ASR_AliyunBLStream';


-- Cập nhật nhà cung cấp ASR phát trực tuyến Beanbag và thêm cấu hình
delete from `ai_model_provider` where id = 'SYSTEM_ASR_DoubaoStreamASR';
INSERT INTO `ai_model_provider` (`id`, `model_type`, `provider_code`, `name`, `fields`, `sort`, `creator`, `create_date`, `updater`, `update_date`) VALUES
('SYSTEM_ASR_DoubaoStreamASR', 'ASR', 'doubao_stream', 'Nhận dạng giọng nói động cơ núi lửa(phát trực tuyến)', '[{"key":"appid","label":"ứng dụngID","type":"string"},{"key":"access_token","label":"mã thông báo truy cập","type":"string"},{"key":"cluster","label":"cụm","type":"string"},{"key":"boosting_table_name","label":"Tên file từ nóng","type":"string"},{"key":"correct_table_name","label":"Thay thế tên file word","type":"string"},{"key":"output_dir","label":"Thư mục đầu ra","type":"string"},{"key":"end_window_size","label":"Thời gian phán xét im lặng(ms)","type":"number"},{"key":"enable_multilingual","label":"Có bật chế độ nhận dạng đa ngôn ngữ hay không","type":"boolean"},{"key":"language","label":"Chỉ định mã hóa ngôn ngữ","type":"string"}]', 3, 1, NOW(), 1, NOW());
UPDATE `ai_model_config` SET 
`remark` = 'túi đậuASRHướng dẫn cấu hình：
1. túi đậuASRvà bánh đậu(phát trực tuyến)ASRSự khác biệt là：túi đậuASRĐó là trả tiền cho mỗi lần xem，túi đậu(phát trực tuyến)ASRNó được tính phí đúng giờ
2. Trả tiền cho mỗi lần xem thường rẻ hơn，Nhưng túi đậu(phát trực tuyến)ASRCông nghệ mô hình lớn được sử dụng，hiệu ứng tốt hơn
3. Bạn cần tạo một ứng dụng trong bảng điều khiển Volcano Engine và lấyappidvàaccess_token
4. Hỗ trợ nhận dạng giọng nói tiếng Trung
5. Cần có kết nối Internet
6. Tệp đầu ra được lưu trongtmp/Thư mục
Các bước ứng dụng：
1. chuyến thăm https://console.volcengine.com/speech/app
2. Tạo ứng dụng mới
3. nhận đượcappidvàaccess_token
4. Điền vào tập tin cấu hình
Nếu bạn cần đặt những từ nóng，Vui lòng tham khảo：https://www.volcengine.com/docs/6561/155738
Nếu bạn bật chế độ nhận dạng đa ngôn ngữ，Vui lòng đặtlanguageKhi chìa khóa trống，Mô hình này hỗ trợ tiếng Trung và tiếng Anh、tiếng Thượng Hải、Phúc Kiến，Tứ Xuyên、Thiểm Tây、Nhận biết tiếng Quảng Đông。Vui lòng tham khảo các ngôn ngữ khác：https://www.volcengine.com/docs/6561/1354869
' WHERE `id` = 'ASR_DoubaoStreamASR';

-- Cập nhật cấu hình mô hình ASR phát trực tuyến Doubao và thêm giá trị mặc định Enable_multilingual
UPDATE `ai_model_config` SET
`config_json` = JSON_SET(
    `config_json`, 
    '$.enable_multilingual', false,
    '$.language', 'zh-CN'
)
WHERE `id` = 'ASR_DoubaoStreamASR' 
AND JSON_EXTRACT(`config_json`, '$.enable_multilingual') IS NULL 
AND JSON_EXTRACT(`config_json`, '$.language') IS NULL;


-- Đã cập nhật cấu hình nhà cung cấp HuoshanDoubleStreamTTS để thêm các tham số âm sắc đa cảm xúc
UPDATE `ai_model_provider`
SET `fields` = '[{"key": "ws_url", "type": "string", "label": "WebSocketđịa chỉ"}, {"key": "appid", "type": "string", "label": "ứng dụngID"}, {"key": "access_token", "type": "string", "label": "mã thông báo truy cập"}, {"key": "resource_id", "type": "string", "label": "Tài nguyênID"}, {"key": "speaker", "type": "string", "label": "Âm thanh mặc định"}, {"key": "enable_ws_reuse", "type": "boolean", "label": "Có bật tái sử dụng liên kết hay không", "default": true}, {"key": "speech_rate", "type": "number", "label": "tốc độ nói(-50~100)"}, {"key": "loudness_rate", "type": "number", "label": "khối lượng(-50~100)"}, {"key": "pitch", "type": "number", "label": "cao độ(-12~12)"}, {"key": "emotion_scale", "type": "number", "label": "cường độ cảm xúc(1-5)"}, {"key": "emotion", "type": "string", "label": "loại cảm xúc"}]'
WHERE `id` = 'SYSTEM_TTS_HSDSTTS';

-- Cập nhật giá trị mặc định
UPDATE `ai_model_config` SET
`config_json` = JSON_SET(
    `config_json`,
    '$.emotion', 'neutral',
    '$.emotion_scale', 4
)
WHERE `id` = 'TTS_HuoshanDoubleStreamTTS'
AND JSON_EXTRACT(`config_json`, '$.emotion') IS NULL 
AND JSON_EXTRACT(`config_json`, '$.emotion_scale') IS NULL;

-- Thêm liên kết tài liệu và ghi chú
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
10. Nhiều thông số cảm xúc（Hiện tại, chỉ có một số âm thanh hỗ trợ thiết lập cảm xúc.）：
   Danh sách âm thanh liên quan：https://www.volcengine.com/docs/6561/1257544
    - emotion_scale：cường độ cảm xúc，Các giá trị tùy chọn là：1~5，Giá trị mặc định là4
    - emotion：loại cảm xúc，Các giá trị tùy chọn là：neutral、happy、sad、angry、fearful、disgusted、surprised
' WHERE `id` = 'TTS_HuoshanDoubleStreamTTS';
