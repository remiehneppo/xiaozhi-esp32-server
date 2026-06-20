-- Cập nhật cấu hình nhà cung cấp HuoshanDoubleStreamTTS và thay đổi các tham số phân tán thành cấu hình từ điển JSON
-- Tích hợp speech_rate, noise_rate, pitch, cảm xúc, cảm xúc_scale và các thông số khác vào ba từ điển JSON: audio_params, bổ sung, mix_loa

UPDATE `ai_model_provider`
SET `fields` = '[
  {"key": "ws_url", "type": "string", "label": "WebSocketđịa chỉ"},
  {"key": "appid", "type": "string", "label": "ứng dụngID"},
  {"key": "access_token", "type": "string", "label": "mã thông báo truy cập"},
  {"key": "resource_id", "type": "string", "label": "Tài nguyênID"},
  {"key": "speaker", "type": "string", "label": "Âm thanh mặc định"},
  {"key": "enable_ws_reuse", "type": "boolean", "label": "Có bật tái sử dụng liên kết hay không", "default": true},
  {"key": "audio_params", "type": "dict", "label": "Cấu hình đầu ra âm thanh"},
  {"key": "additions", "type": "dict", "label": "Cấu hình xử lý văn bản nâng cao"},
  {"key": "mix_speaker", "type": "dict", "label": "Cấu hình điều khiển trộn"}
]'
WHERE `id` = 'SYSTEM_TTS_HSDSTTS';

-- Cập nhật cấu hình hiện có để di chuyển các tham số phân tán cũ sang cấu trúc từ điển JSON mới
UPDATE `ai_model_config`
SET `config_json` = JSON_SET(
    `config_json`,
    '$.audio_params', JSON_OBJECT(
        'speech_rate', CAST(COALESCE(NULLIF(JSON_UNQUOTE(JSON_EXTRACT(`config_json`, '$.speech_rate')), ''), '0') AS SIGNED),
        'loudness_rate', CAST(COALESCE(NULLIF(JSON_UNQUOTE(JSON_EXTRACT(`config_json`, '$.loudness_rate')), ''), '0') AS SIGNED)
    ),
    '$.additions', JSON_OBJECT(
        'aigc_metadata', JSON_OBJECT(),
        'cache_config', JSON_OBJECT(),
        'post_process', JSON_OBJECT(
            'pitch', CAST(COALESCE(NULLIF(JSON_UNQUOTE(JSON_EXTRACT(`config_json`, '$.pitch')), ''), '0') AS SIGNED)
        )
    ),
    '$.mix_speaker', JSON_OBJECT()
)
WHERE `id` = 'TTS_HuoshanDoubleStreamTTS';

-- Xóa trường tham số phân tán cũ
UPDATE `ai_model_config`
SET `config_json` = JSON_REMOVE(
    `config_json`,
    '$.speech_rate',
    '$.loudness_rate',
    '$.pitch',
    '$.emotion',
    '$.emotion_scale'
)
WHERE `id` = 'TTS_HuoshanDoubleStreamTTS';

-- Đã cập nhật liên kết tài liệu và ghi chú
UPDATE `ai_model_config` SET
`doc_link` = 'https://www.volcengine.com/docs/6561/1329505',
`remark` = 'Dòng chảy hai chiều động cơ núi lửaTTSHướng dẫn cấu hình：
1. chuyến thăm https://www.volcengine.com/ Đăng ký và mở tài khoản Volcano Engine
2. chuyến thăm https://console.volcengine.com/speech/service/10007 Mô hình lớn tổng hợp giọng nói mở，Mua âm thanh
3. Lấy nó ở cuối trangappidvàaccess_token
4. Tài nguyênIDcố định vào：volc.service_type.10029（Tổng hợp và trộn giọng nói mô hình lớn）
5. Tái sử dụng liên kết：bật lênWebSocketTái sử dụng kết nối，Mặc địnhtrueGiảm mất liên kết（Lưu ý：Sau khi sử dụng lại, khi thiết bị ở trạng thái lắng nghe, các liên kết nhàn rỗi sẽ chiếm số lượng kết nối đồng thời.）

Tài liệu tham số chi tiết：https://www.volcengine.com/docs/6561/1329505
【audio_params】Cấu hình đầu ra âm thanh - Người dùng có thể tùy chỉnh bất kỳ thông số âm thanh nào được hỗ trợ bởi công cụ Volcano
  - speech_rate: tốc độ nói(-50~100)，Mặc định0
  - loudness_rate: khối lượng(-50~100)，Mặc định0
  - emotion: loại cảm xúc（Chỉ một số âm thanh được hỗ trợ），Giá trị tùy chọn：neutral、happy、sad、angry、fearful、disgusted、surprised
  - emotion_scale: cường độ cảm xúc(1~5)，Mặc định4
  Ví dụ：{"speech_rate": 10, "loudness_rate": 5, "emotion": "happy", "emotion_scale": 4}

【additions】Cấu hình xử lý văn bản nâng cao - Người dùng có thể tùy chỉnh bất kỳ thông số nâng cao nào được hỗ trợ bởi công cụ Volcano
  - post_process.pitch: cao độ(-12~12)，Mặc định0
  - aigc_metadata: AIGCCấu hình siêu dữ liệu
  - cache_config: Cấu hình bộ đệm
  Ví dụ：{"post_process": {"pitch": 2}, "aigc_metadata": {}, "cache_config": {}}

【mix_speaker】Cấu hình điều khiển trộn - trộn đa thời gian（chỉ TTS 1.0）
  Ví dụ：
    {"speakers": [
      {"source_speaker": "zh_male_bvlazysheep","mix_factor": 0.3}, 
      {"source_speaker": "BV120_streaming","mix_factor": 0.3}, 
      {"source_speaker": "zh_male_ahu_conversation_wvae_bigtts","mix_factor": 0.4}
    ]}

Lưu ý：
- Thông số âm sắc đa cảm xúc（emotion、emotion_scale）Chỉ một số âm thanh được hỗ trợ
- Danh sách âm thanh liên quan：https://www.volcengine.com/docs/6561/1257544
- Người dùng có thể sử dụng động cơ núi lửaAPITài liệu tự bổ sung thêm nhiều tham số
- Chức năng trộn chủ yếu phù hợp với các mô hình tổng hợp giọng nói Doubao.1.0âm sắc，Khi sử dụng, bạn cầnreq_params.speakerđặt thànhcustom_mix_bigtts
'
WHERE `id` = 'TTS_HuoshanDoubleStreamTTS';
