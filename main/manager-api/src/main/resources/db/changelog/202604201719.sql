-- Đã thêm nhà cung cấp mô hình tổng hợp giọng nói Beanbao 2.0 (sử dụng ID tài nguyên Seed-tts-2.0)
-- Cấu hình tương tự như TTS luồng kép núi lửa, nhưng Resource_id được cố định thành Seed-tts-2.0

-- Chèn nhà cung cấp Mô hình tổng hợp giọng nói Beanbag 2.0
delete from `ai_model_provider` where id = 'SYSTEM_TTS_HSDSTTS_V2';
INSERT INTO `ai_model_provider` (`id`, `model_type`, `provider_code`, `name`, `fields`, `sort`, `creator`, `create_date`, `updater`, `update_date`) VALUES
('SYSTEM_TTS_HSDSTTS_V2', 'TTS', 'huoshan_double_stream', 'Mô hình tổng hợp giọng nói Doubao2.0', '[
  {"key": "ws_url", "type": "string", "label": "WebSocketđịa chỉ"},
  {"key": "appid", "type": "string", "label": "ứng dụngID"},
  {"key": "access_token", "type": "string", "label": "mã thông báo truy cập"},
  {"key": "resource_id", "type": "string", "label": "Tài nguyênID"},
  {"key": "speaker", "type": "string", "label": "Âm thanh mặc định"},
  {"key": "enable_ws_reuse", "type": "boolean", "label": "Có bật tái sử dụng liên kết hay không", "default": true},
  {"key": "audio_params", "type": "dict", "label": "Cấu hình đầu ra âm thanh"},
  {"key": "additions", "type": "dict", "label": "Cấu hình xử lý văn bản nâng cao"},
  {"key": "mix_speaker", "type": "dict", "label": "Cấu hình điều khiển trộn"}
]', 14, 1, NOW(), 1, NOW());

-- Chèn cấu hình mô hình tổng hợp giọng nói Beanbao 2.0
delete from `ai_model_config` where id = 'TTS_HSDSTTS_V2';
INSERT INTO `ai_model_config` VALUES ('TTS_HSDSTTS_V2', 'TTS', 'HuoshanDoubleStreamTTSV2', 'Mô hình tổng hợp giọng nói Doubao2.0', 0, 1, '{
  "type": "huoshan_double_stream",
  "ws_url": "wss://openspeech.bytedance.com/api/v3/tts/bidirection",
  "appid": "",
  "access_token": "",
  "resource_id": "seed-tts-2.0",
  "speaker": "zh_female_xiaohe_uranus_bigtts",
  "enable_ws_reuse": true,
  "audio_params": {
    "speech_rate": 0,
    "loudness_rate": 0
  },
  "additions": {
    "aigc_metadata": {},
    "cache_config": {},
    "post_process": {
      "pitch": 0
    }
  },
  "mix_speaker": {}
}', NULL, NULL, 17, NULL, NULL, NULL, NULL);

-- Tài liệu cấu hình mô hình tổng hợp giọng nói Doubao 2.0
UPDATE `ai_model_config` SET
`doc_link` = 'https://www.volcengine.com/docs/6561/1329505',
`remark` = 'Mô hình tổng hợp giọng nói Doubao2.0Hướng dẫn cấu hình（Dựa trên động cơ núi lửaseed-tts-2.0）：
1. chuyến thăm https://www.volcengine.com/ Đăng ký và mở tài khoản Volcano Engine
2. chuyến thăm https://console.volcengine.com/speech/service/10035 Mô hình lớn tổng hợp giọng nói mở，Mua âm thanh
3. Lấy nó ở cuối trangappidvàaccess_token
4. Tài nguyênIDcố định vào：seed-tts-2.0（Mô hình tổng hợp giọng nói Doubao2.0）
5. Tái sử dụng liên kết：bật lênWebSocketTái sử dụng kết nối，Mặc địnhtrueGiảm mất liên kết（Lưu ý：Sau khi sử dụng lại, khi thiết bị ở trạng thái lắng nghe, các liên kết nhàn rỗi sẽ chiếm số lượng kết nối đồng thời.）

Tài liệu tham số chi tiết：https://www.volcengine.com/docs/6561/1329505
【audio_params】Cấu hình đầu ra âm thanh - Người dùng có thể tùy chỉnh bất kỳ thông số âm thanh nào được hỗ trợ bởi công cụ Volcano
  - speech_rate: tốc độ nói(-50~100)，Mặc định0
  - loudness_rate: khối lượng(-50~100)，Mặc định0
  Ví dụ：{"speech_rate": 10, "loudness_rate": 5}

【additions】Cấu hình xử lý văn bản nâng cao - Người dùng có thể tùy chỉnh bất kỳ thông số nâng cao nào được hỗ trợ bởi công cụ Volcano
  - post_process.pitch: cao độ(-12~12)，Mặc định0
  - aigc_metadata: AIGCCấu hình siêu dữ liệu
  - cache_config: Cấu hình bộ đệm
  Ví dụ：{"post_process": {"pitch": 2}, "aigc_metadata": {}, "cache_config": {}}

Lưu ý：
- Mô hình tổng hợp giọng nói Doubao2.0sử dụngseed-tts-2.0Tài nguyênID，Dòng chảy đôi với núi lửaTTS（volc.service_type.10029）khác nhau
- Danh sách âm thanh liên quan：https://www.volcengine.com/docs/6561/1257544
- Người dùng có thể sử dụng động cơ núi lửaAPITài liệu tự bổ sung thêm nhiều tham số
' WHERE `id` = 'TTS_HSDSTTS_V2';

-- Đã thêm âm sắc mô hình tổng hợp giọng nói Beanbag 2.0 (giống như âm sắc TTS luồng kép của Volcano)
delete from `ai_tts_voice` where tts_model_id = 'TTS_HSDSTTS_V2';
INSERT INTO `ai_tts_voice` VALUES ('TTS_HSDSTTS_V2_0001', 'TTS_HSDSTTS_V2', 'Vivi', 'zh_female_vv_uranus_bigtts', 'tiếng quan thoại、tiếng Nhật、tiếng Indonesia、người Tây Ban Nha ở Mexico', 'https://lf3-static.bytednsdoc.com/obj/eden-cn/lm_hz_ihsph/ljhwZthlaukjlkulzlp/portal/bigtts/zh_female_vv_uranus_bigtts.wav', NULL, NULL, NULL, 1, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_HSDSTTS_V2_0002', 'TTS_HSDSTTS_V2', 'Tiểu Hà', 'zh_female_xiaohe_uranus_bigtts', 'Tiếng Phổ Thông, Tiếng Anh', 'https://lf3-static.bytednsdoc.com/obj/eden-cn/lm_hz_ihsph/ljhwZthlaukjlkulzlp/portal/bigtts/zh_female_xiaohe_uranus_bigtts.mp3', NULL, NULL, NULL, 2, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_HSDSTTS_V2_0003', 'TTS_HSDSTTS_V2', 'Vân Châu', 'zh_male_m191_uranus_bigtts', 'Tiếng Phổ Thông, Tiếng Anh', 'https://lf3-static.bytednsdoc.com/obj/eden-cn/lm_hz_ihsph/ljhwZthlaukjlkulzlp/portal/bigtts/zh_male_m191_uranus_bigtts.mp3', NULL, NULL, NULL, 3, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_HSDSTTS_V2_0004', 'TTS_HSDSTTS_V2', 'Tiểu Thiên', 'zh_male_taocheng_uranus_bigtts', 'Tiếng Phổ Thông, Tiếng Anh', 'https://lf3-static.bytednsdoc.com/obj/eden-cn/lm_hz_ihsph/ljhwZthlaukjlkulzlp/portal/bigtts/zh_male_taocheng_uranus_bigtts.mp3', NULL, NULL, NULL, 4, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_HSDSTTS_V2_0005', 'TTS_HSDSTTS_V2', 'Lưu Phi', 'zh_male_liufei_uranus_bigtts', 'Tiếng Phổ Thông, Tiếng Anh', 'https://lf3-static.bytednsdoc.com/obj/eden-cn/lm_hz_ihsph/ljhwZthlaukjlkulzlp/portal/bigtts/zh_male_liufei_uranus_bigtts.mp3', NULL, NULL, NULL, 5, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_HSDSTTS_V2_0006', 'TTS_HSDSTTS_V2', 'Sophie quyến rũ', 'zh_female_sophie_uranus_bigtts', 'Tiếng Phổ Thông, Tiếng Anh', 'https://lf3-static.bytednsdoc.com/obj/eden-cn/lm_hz_ihsph/ljhwZthlaukjlkulzlp/portal/bigtts/zh_male_sophie_uranus_bigtts.mp3', NULL, NULL, NULL, 6, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_HSDSTTS_V2_0007', 'TTS_HSDSTTS_V2', 'giọng nữ tươi trẻ', 'zh_female_qingxinnvsheng_uranus_bigtts', 'Tiếng Phổ Thông, Tiếng Anh', 'https://lf3-static.bytednsdoc.com/obj/eden-cn/lm_hz_ihsph/ljhwZthlaukjlkulzlp/portal/bigtts/zh_female_qingxinnvsheng_uranus_bigtts.mp3', NULL, NULL, NULL, 7, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_HSDSTTS_V2_0008', 'TTS_HSDSTTS_V2', 'Trí tuệ sáng chói', 'zh_female_cancan_uranus_bigtts', 'Tiếng Phổ Thông, Tiếng Anh', 'https://lf3-static.bytednsdoc.com/obj/eden-cn/lm_hz_ihsph/ljhwZthlaukjlkulzlp/portal/bigtts/zh_female_cancan_uranus_bigtts.mp3', NULL, NULL, NULL, 8, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_HSDSTTS_V2_0009', 'TTS_HSDSTTS_V2', 'Nữ sinh quyến rũ', 'zh_female_sajiaoxuemei_uranus_bigtts', 'Tiếng Phổ Thông, Tiếng Anh', 'https://lf3-static.bytednsdoc.com/obj/eden-cn/lm_hz_ihsph/ljhwZthlaukjlkulzlp/portal/bigtts/zh_female_sajiaoxuemei_uranus_bigtts.mp3', NULL, NULL, NULL, 9, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_HSDSTTS_V2_0010', 'TTS_HSDSTTS_V2', 'nguồn nhỏ ngọt ngào', 'zh_female_tianmeixiaoyuan_uranus_bigtts', 'Tiếng Phổ Thông, Tiếng Anh', 'https://lf3-static.bytednsdoc.com/obj/eden-cn/lm_hz_ihsph/ljhwZthlaukjlkulzlp/portal/bigtts/zh_female_tianmeixiaoyuan_uranus_bigtts.mp3', NULL, NULL, NULL, 10, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_HSDSTTS_V2_0011', 'TTS_HSDSTTS_V2', 'đào ngọt ngào', 'zh_female_tianmeitaozi_uranus_bigtts', 'Tiếng Phổ Thông, Tiếng Anh', 'https://lf3-static.bytednsdoc.com/obj/eden-cn/lm_hz_ihsph/ljhwZthlaukjlkulzlp/portal/bigtts/zh_female_tianmeitaozi_uranus_bigtts.mp3', NULL, NULL, NULL, 11, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_HSDSTTS_V2_0012', 'TTS_HSDSTTS_V2', 'suy nghĩ hạnh phúc', 'zh_female_shuangkuaisisi_uranus_bigtts', 'Tiếng Phổ Thông, Tiếng Anh', 'https://lf3-static.bytednsdoc.com/obj/eden-cn/lm_hz_ihsph/ljhwZthlaukjlkulzlp/portal/bigtts/zh_female_shuangkuaisisi_uranus_bigtts.mp3', NULL, NULL, NULL, 12, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_HSDSTTS_V2_0013', 'TTS_HSDSTTS_V2', 'lợn peppa', 'zh_female_peiqi_uranus_bigtts', 'Tiếng Phổ Thông, Tiếng Anh', 'https://lf3-static.bytednsdoc.com/obj/eden-cn/lm_hz_ihsph/ljhwZthlaukjlkulzlp/portal/bigtts/zh_female_peiqi_uranus_bigtts.mp3', NULL, NULL, NULL, 13, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_HSDSTTS_V2_0014', 'TTS_HSDSTTS_V2', 'cô gái nhà bên', 'zh_female_linjianvhai_uranus_bigtts', 'Tiếng Phổ Thông, Tiếng Anh', 'https://lf3-static.bytednsdoc.com/obj/eden-cn/lm_hz_ihsph/ljhwZthlaukjlkulzlp/portal/bigtts/zh_female_linjianvhai_uranus_bigtts.mp3', NULL, NULL, NULL, 14, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_HSDSTTS_V2_0015', 'TTS_HSDSTTS_V2', 'Tử Tân trẻ/Brayan', 'zh_male_shaonianzixin_uranus_bigtts', 'Tiếng Phổ Thông, Tiếng Anh', 'https://lf3-static.bytednsdoc.com/obj/eden-cn/lm_hz_ihsph/ljhwZthlaukjlkulzlp/portal/bigtts/zh_male_shaonianzixin_uranus_bigtts.mp3', NULL, NULL, NULL, 15, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_HSDSTTS_V2_0016', 'TTS_HSDSTTS_V2', 'Anh Khỉ', 'zh_male_sunwukong_uranus_bigtts', 'Tiếng Phổ Thông, Tiếng Anh', 'https://lf3-static.bytednsdoc.com/obj/eden-cn/lm_hz_ihsph/ljhwZthlaukjlkulzlp/portal/bigtts/zh_male_sunwukong_uranus_bigtts.mp3', NULL, NULL, NULL, 16, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_HSDSTTS_V2_0017', 'TTS_HSDSTTS_V2', 'Bạn gái quyến rũ', 'zh_female_meilinvyou_uranus_bigtts', 'Tiếng Phổ Thông, Tiếng Anh', 'https://lf3-static.bytednsdoc.com/obj/eden-cn/lm_hz_ihsph/ljhwZthlaukjlkulzlp/portal/bigtts/zh_female_meilinvyou_uranus_bigtts.mp3', NULL, NULL, NULL, 17, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_HSDSTTS_V2_0018', 'TTS_HSDSTTS_V2', 'Tim', 'en_male_tim_uranus_bigtts', 'Tiếng Anh', 'https://lf3-static.bytednsdoc.com/obj/eden-cn/lm_hz_ihsph/ljhwZthlaukjlkulzlp/portal/bigtts/en_male_tim_uranus_bigtts.mp3', NULL, NULL, NULL, 18, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_HSDSTTS_V2_0019', 'TTS_HSDSTTS_V2', 'Dacey', 'en_female_dacey_uranus_bigtts', 'Tiếng Anh', 'https://lf3-static.bytednsdoc.com/obj/eden-cn/lm_hz_ihsph/ljhwZthlaukjlkulzlp/portal/bigtts/en_female_dacey_uranus_bigtts.mp3', NULL, NULL, NULL, 19, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_HSDSTTS_V2_0020', 'TTS_HSDSTTS_V2', 'Stokie', 'en_female_stokie_uranus_bigtts', 'Tiếng Anh', 'https://lf3-static.bytednsdoc.com/obj/eden-cn/lm_hz_ihsph/ljhwZthlaukjlkulzlp/portal/bigtts/en_female_stokie_uranus_bigtts.mp3', NULL, NULL, NULL, 20, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_HSDSTTS_V2_0021', 'TTS_HSDSTTS_V2', 'Ấm Áp A Hổ/Alvin', 'zh_male_wennuanahu_uranus_bigtts', 'Tiếng Phổ Thông, Tiếng Anh', 'https://lf3-static.bytednsdoc.com/obj/eden-cn/lm_hz_ihsph/ljhwZthlaukjlkulzlp/portal/bigtts/zh_male_wennuanahu_uranus_bigtts.mp3', NULL, NULL, NULL, 21, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_HSDSTTS_V2_0022', 'TTS_HSDSTTS_V2', 'Bé Nhỏ Đáng Yêu', 'zh_male_naiqimengwa_uranus_bigtts', 'Tiếng Phổ Thông, Tiếng Anh', 'https://lf3-static.bytednsdoc.com/obj/eden-cn/lm_hz_ihsph/ljhwZthlaukjlkulzlp/portal/bigtts/zh_male_naiqimengwa_uranus_bigtts.mp3', NULL, NULL, NULL, 22, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_HSDSTTS_V2_0023', 'TTS_HSDSTTS_V2', 'Bà Nội', 'zh_female_popo_uranus_bigtts', 'Tiếng Phổ Thông, Tiếng Anh', 'https://lf3-static.bytednsdoc.com/obj/eden-cn/lm_hz_ihsph/ljhwZthlaukjlkulzlp/portal/bigtts/zh_female_popo_uranus_bigtts.mp3', NULL, NULL, NULL, 23, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_HSDSTTS_V2_0024', 'TTS_HSDSTTS_V2', 'Chị Gái Cởi Mở', 'zh_female_kailangjiejie_uranus_bigtts', 'Tiếng Phổ Thông, Tiếng Anh', 'https://lf3-static.bytednsdoc.com/obj/eden-cn/lm_hz_ihsph/ljhwZthlaukjlkulzlp/portal/bigtts/zh_female_kailangjiejie_uranus_bigtts.mp3', NULL, NULL, NULL, 24, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_HSDSTTS_V2_0025', 'TTS_HSDSTTS_V2', 'Đóa Đóa Nhẹ Nhàng', 'saturn_zh_female_qingyingduoduo_cs_tob', 'Tiếng Phổ Thông, Tiếng Anh', 'https://lf3-static.bytednsdoc.com/obj/eden-cn/lm_hz_ihsph/ljhwZthlaukjlkulzlp/portal/bigtts/ICL_zh_female_qingyingduoduo_cs_tob.mp3', NULL, NULL, NULL, 25, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_HSDSTTS_V2_0026', 'TTS_HSDSTTS_V2', 'San San Ôn Nhu', 'saturn_zh_female_wenwanshanshan_cs_tob', 'Tiếng Phổ Thông, Tiếng Anh', 'https://lf3-static.bytednsdoc.com/obj/eden-cn/lm_hz_ihsph/ljhwZthlaukjlkulzlp/portal/bigtts/ICL_zh_female_wenwanshanshan_cs_tob.mp3', NULL, NULL, NULL, 26, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_HSDSTTS_V2_0027', 'TTS_HSDSTTS_V2', 'Chú Thanh Bá Dự', 'zh_male_baqiqingshu_uranus_bigtts', 'Tiếng Phổ Thông, Tiếng Anh', 'https://lf3-static.bytednsdoc.com/obj/eden-cn/lm_hz_ihsph/ljhwZthlaukjlkulzlp/portal/bigtts/zh_male_baqiqingshu_uranus_bigtts.mp3', NULL, NULL, NULL, 27, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_HSDSTTS_V2_0028', 'TTS_HSDSTTS_V2', 'Thuyết Minh Huyền Bí', 'zh_male_xuanyijieshuo_uranus_bigtts', 'Tiếng Phổ Thông, Tiếng Anh', 'https://lf3-static.bytednsdoc.com/obj/eden-cn/lm_hz_ihsph/ljhwZthlaukjlkulzlp/portal/bigtts/zh_male_xuanyijieshuo_uranus_bigtts.mp3', NULL, NULL, NULL, 28, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_HSDSTTS_V2_0029', 'TTS_HSDSTTS_V2', 'Thiếu Ngự Cổ Phong', 'zh_female_gufengshaoyu_uranus_bigtts', 'Tiếng Phổ Thông, Tiếng Anh', 'https://lf3-static.bytednsdoc.com/obj/eden-cn/lm_hz_ihsph/ljhwZthlaukjlkulzlp/portal/bigtts/zh_female_gufengshaoyu_uranus_bigtts.mp3', NULL, NULL, NULL, 29, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_HSDSTTS_V2_0030', 'TTS_HSDSTTS_V2', 'Đường Tăng', 'zh_male_tangseng_uranus_bigtts', 'Tiếng Phổ Thông, Tiếng Anh', 'https://lf3-static.bytednsdoc.com/obj/eden-cn/lm_hz_ihsph/ljhwZthlaukjlkulzlp/portal/bigtts/zh_male_tangseng_uranus_bigtts.mp3', NULL, NULL, NULL, 30, NULL, NULL, NULL, NULL);
