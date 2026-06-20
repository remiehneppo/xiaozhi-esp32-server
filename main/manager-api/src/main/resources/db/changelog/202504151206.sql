-- Chỉnh sửa thông số trước phiên bản 0.3.0
update `sys_params` set param_value = '.mp3;.wav;.p3' where  param_code = 'plugins.play_music.music_ext';
update `ai_model_config` set config_json =  '{\"type\": \"intent_llm\", \"llm\": \"LLM_ChatGLMLLM\"}' where  id = 'Intent_intent_llm';

-- Thêm âm thanh cạnh
delete from `ai_tts_voice` where tts_model_id = 'TTS_EdgeTTS';
INSERT INTO `ai_tts_voice` VALUES 
('TTS_EdgeTTS0001', 'TTS_EdgeTTS', 'EdgeTTSgiọng nữ-Tiểu Tiểu', 'zh-CN-XiaoxiaoNeural', 'tiếng quan thoại', NULL, NULL, 1, NULL, NULL, NULL, NULL),
('TTS_EdgeTTS0002', 'TTS_EdgeTTS', 'EdgeTTSgiọng nam-Vân Dương', 'zh-CN-YunyangNeural', 'tiếng quan thoại', NULL, NULL, 1, NULL, NULL, NULL, NULL),
('TTS_EdgeTTS0003', 'TTS_EdgeTTS', 'EdgeTTSgiọng nữ-Tiểu Nghĩa', 'zh-CN-XiaoyiNeural', 'tiếng quan thoại', NULL, NULL, 1, NULL, NULL, NULL, NULL),
('TTS_EdgeTTS0004', 'TTS_EdgeTTS', 'EdgeTTSgiọng nam-Vân Kiên', 'zh-CN-YunjianNeural', 'tiếng quan thoại', NULL, NULL, 1, NULL, NULL, NULL, NULL),
('TTS_EdgeTTS0005', 'TTS_EdgeTTS', 'EdgeTTSgiọng nam-Vân Hi', 'zh-CN-YunxiNeural', 'tiếng quan thoại', NULL, NULL, 1, NULL, NULL, NULL, NULL),
('TTS_EdgeTTS0006', 'TTS_EdgeTTS', 'EdgeTTSgiọng nam-Vân Hạ', 'zh-CN-YunxiaNeural', 'tiếng quan thoại', NULL, NULL, 1, NULL, NULL, NULL, NULL),
('TTS_EdgeTTS0007', 'TTS_EdgeTTS', 'EdgeTTSgiọng nữ-Liêu Ninh Tiểu Bắc', 'zh-CN-liaoning-XiaobeiNeural', 'Liêu Ninh', NULL, NULL, 1, NULL, NULL, NULL, NULL),
('TTS_EdgeTTS0008', 'TTS_EdgeTTS', 'EdgeTTSgiọng nữ-Thiểm Tây Tiểu Ni', 'zh-CN-shaanxi-XiaoniNeural', 'Thiểm Tây', NULL, NULL, 1, NULL, NULL, NULL, NULL),
('TTS_EdgeTTS0009', 'TTS_EdgeTTS', 'EdgeTTSgiọng nữ-Hồng Kông Hải Gia', 'zh-HK-HiuGaaiNeural', 'tiếng Quảng Đông', 'General', 'Friendly, Positive', 1, NULL, NULL, NULL, NULL),
('TTS_EdgeTTS0010', 'TTS_EdgeTTS', 'EdgeTTSgiọng nữ-Hồng Kông Hayman', 'zh-HK-HiuMaanNeural', 'tiếng Quảng Đông', 'General', 'Friendly, Positive', 1, NULL, NULL, NULL, NULL),
('TTS_EdgeTTS0011', 'TTS_EdgeTTS', 'EdgeTTSgiọng nam-Hồng Kông Vạn Long', 'zh-HK-WanLungNeural', 'tiếng Quảng Đông', 'General', 'Friendly, Positive', 1, NULL, NULL, NULL, NULL);

-- Thêm vào có cho phép tham số đăng ký người dùng hay không
delete from `sys_params` where  id in (103,104);
INSERT INTO `sys_params` (id, param_code, param_value, value_type, param_type, remark) VALUES (103, 'server.allow_user_register', 'false', 'boolean', 1, 'Có thực hiện đăng ký cho người khác ngoài quản trị viên hay không');
INSERT INTO `sys_params` (id, param_code, param_value, value_type, param_type, remark) VALUES (104, 'server.fronted_url', 'http://xiaozhi.server.com', 'string', 1, 'Địa chỉ bảng điều khiển được hiển thị khi cấp mã xác minh gồm sáu chữ số');

-- Đã sửa âm sắc CosyVoiceSiliconflow
delete from `ai_tts_voice` where tts_model_id = 'TTS_CosyVoiceSiliconflow';
INSERT INTO `ai_tts_voice` VALUES ('TTS_CosyVoiceSiliconflow0001', 'TTS_CosyVoiceSiliconflow', 'CosyVoicegiọng nam', 'FunAudioLLM/CosyVoice2-0.5B:alex', 'Tiếng Trung', 'https://example.com/cosyvoice/alex.mp3', NULL, 6, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_CosyVoiceSiliconflow0002', 'TTS_CosyVoiceSiliconflow', 'CosyVoicegiọng nữ', 'FunAudioLLM/CosyVoice2-0.5B:bella', 'Tiếng Trung', 'https://example.com/cosyvoice/bella.mp3', NULL, 6, NULL, NULL, NULL, NULL);
