-- Thêm nhà cung cấp TTS phát trực tuyến MinimaxHTTPStream
delete from `ai_model_provider` where id = 'SYSTEM_TTS_MinimaxStreamTTS';
INSERT INTO `ai_model_provider` (`id`, `model_type`, `provider_code`, `name`, `fields`, `sort`, `creator`, `create_date`, `updater`, `update_date`) VALUES
('SYSTEM_TTS_MinimaxStreamTTS', 'TTS', 'minimax_httpstream', 'Minimaxtổng hợp giọng nói trực tuyến', '[{"key":"group_id","label":"nhómID","type":"string"},{"key":"api_key","label":"APIchìa khóa","type":"string"},{"key":"model","label":"người mẫu","type":"string"},{"key":"voice_id","label":"âm sắcID","type":"string"},{"key":"output_dir","label":"Thư mục đầu ra","type":"string"},{"key":"voice_setting","label":"Cài đặt âm thanh","type":"dict","dict_name":"voice_setting"},{"key":"pronunciation_dict","label":"từ điển phát âm","type":"dict","dict_name":"pronunciation_dict"},{"key":"audio_setting","label":"Cài đặt âm thanh","type":"dict","dict_name":"audio_setting"},{"key":"timber_weights","label":"trọng lượng âm sắc","type":"string"}]', 18, 1, NOW(), 1, NOW());

-- Thêm cấu hình mô hình TTS phát trực tuyến Minimax
delete from `ai_model_config` where id = 'TTS_MinimaxStreamTTS';
INSERT INTO `ai_model_config` VALUES ('TTS_MinimaxStreamTTS', 'TTS', 'MinimaxStreamTTS', 'Minimaxtổng hợp giọng nói trực tuyến', 0, 1, '{"type": "minimax_httpstream", "group_id": "", "api_key": "", "model": "speech-01-turbo", "voice_id": "female-shaonv", "output_dir": "tmp/", "voice_setting": {"speed": 1, "vol": 1, "pitch": 0, "emotion": "happy"}, "pronunciation_dict": {"tone": ["Quy trình/(chu3)(li3)", "nguy hiểm/dangerous"]}, "audio_setting": {"sample_rate": 24000, "bitrate": 128000, "format": "pcm", "channel": 1}}', NULL, NULL, 21, NULL, NULL, NULL, NULL);

-- Đã cập nhật hướng dẫn cấu hình TTS phát trực tuyến Minimax
UPDATE `ai_model_config` SET 
`doc_link` = 'https://platform.minimaxi.com/',
`remark` = 'Minimaxphát trực tuyếnTTSHướng dẫn cấu hình：
1. Cần phải nộp đơn đầu tiênMinimax API Key
2. Cần điền vàoGroup ID
3. Hỗ trợ nhiều cài đặt âm thanh và điều chỉnh thông số âm thanh
4. Hỗ trợ tổng hợp phát trực tuyến theo thời gian thực，Có độ trễ thấp hơn
5. Hỗ trợ từ điển phát âm tùy chỉnh và trọng lượng âm sắc
6. Cấu hình tham số ẩn：cài đặt âm thanh(voice_setting)、từ điển phát âm(pronunciation_dict)、trọng lượng âm sắc(timber_weights)
   - tốc độ nói(speed): phạm vi[0.5,2]，Mặc định1.0，Giá trị càng lớn thì tốc độ nói càng nhanh.
   - khối lượng(vol): phạm vi(0,10]，Mặc định1.0，Giá trị càng lớn thì âm lượng càng cao.
   - cao độ(pitch): phạm vi[-12,12]，Mặc định0，Giá trị phải là số nguyên
   - cảm xúc(emotion): Kiểm soát cảm xúc của lời nói tổng hợp，hỗ trợ7Loại giá trị：["happy", "sad", "angry", "fearful", "disgusted", "surprised", "calm"]，Thông số này chỉ dành cho speech-2.5-hd-preview、speech-2.5-turbo-preview、speech-02-hd、speech-02-turbo、speech-01-turbo、speech-01-hd Có hiệu lực
   - timbre_weightsvớivoice_idChọn một trong hai yêu cầu
   - voice_id(âm sắc được yêu cầuid，SuwaweightCác thông số được điền đồng bộ)
   - weight(trọng lượng，Được hỗ trợ nhiều nhất4hỗn hợp âm sắc。phạm vi[1,100])
' WHERE `id` = 'TTS_MinimaxStreamTTS';

-- Đã thêm âm thanh TTS phát trực tuyến Minimax
delete from `ai_tts_voice` where tts_model_id = 'TTS_MinimaxStreamTTS';

-- Âm thanh mặc định
INSERT INTO `ai_tts_voice` VALUES ('TTS_MinimaxStreamTTS_0001', 'TTS_MinimaxStreamTTS', 'giọng nữ tính', 'female-shaonv', 'Tiếng Trung', NULL, NULL, NULL, NULL, 1, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_MinimaxStreamTTS_0002', 'TTS_MinimaxStreamTTS', 'Giọng nữ trưởng thành', 'female-chengshu', 'Tiếng Trung', NULL, NULL, NULL, NULL, 2, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_MinimaxStreamTTS_0003', 'TTS_MinimaxStreamTTS', 'Thiếu chủ độc đoán', 'badao_shaoye', 'Tiếng Trung', NULL, NULL, NULL, NULL, 3, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_MinimaxStreamTTS_0004', 'TTS_MinimaxStreamTTS', 'anh trai yandere', 'bingjiao_didi', 'Tiếng Trung', NULL, NULL, NULL, NULL, 4, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_MinimaxStreamTTS_0005', 'TTS_MinimaxStreamTTS', 'Thiếu niên ngây thơ', 'chunzhen_xuedi', 'Tiếng Trung', NULL, NULL, NULL, NULL, 5, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_MinimaxStreamTTS_0006', 'TTS_MinimaxStreamTTS', 'lạnh lùng', 'lengdan_xiongzhang', 'Tiếng Trung', NULL, NULL, NULL, NULL, 6, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_MinimaxStreamTTS_0007', 'TTS_MinimaxStreamTTS', 'Tiểu Linh ngọt ngào', 'tianxin_xiaoling', 'Tiếng Trung', NULL, NULL, NULL, NULL, 7, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_MinimaxStreamTTS_0008', 'TTS_MinimaxStreamTTS', 'Cô gái vui tính và dễ thương', 'qiaopi_mengmei', 'Tiếng Trung', NULL, NULL, NULL, NULL, 8, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_MinimaxStreamTTS_0009', 'TTS_MinimaxStreamTTS', 'Em gái hoàng gia quyến rũ', 'wumei_yujie', 'Tiếng Trung', NULL, NULL, NULL, NULL, 9, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_MinimaxStreamTTS_0010', 'TTS_MinimaxStreamTTS', 'Cô học trò dễ thương', 'diadia_xuemei', 'Tiếng Trung', NULL, NULL, NULL, NULL, 7, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_MinimaxStreamTTS_0011', 'TTS_MinimaxStreamTTS', 'Chị cao cấp thanh lịch', 'danya_xuejie', 'Tiếng Trung', NULL, NULL, NULL, NULL, 8, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_MinimaxStreamTTS_0012', 'TTS_MinimaxStreamTTS', 'Santa Claus', 'Santa_Claus', 'Tiếng Trung', NULL, NULL, NULL, NULL, 9, NULL, NULL, NULL, NULL);
INSERT INTO `ai_tts_voice` VALUES ('TTS_MinimaxStreamTTS_0013', 'TTS_MinimaxStreamTTS', 'Grinch', 'Grinch', 'Tiếng Trung', NULL, NULL, NULL, NULL, 10, NULL, NULL, NULL, NULL);
