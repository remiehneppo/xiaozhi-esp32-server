-- Xóa cấu hình nhà cung cấp trong đó mã_nhà cung cấp là linkerai
DELETE FROM `ai_model_provider` WHERE `provider_code` = 'linkerai';

-- Xóa cấu hình mô hình model_code cho LinkeraiTTS
DELETE FROM `ai_model_config` WHERE `model_code` = 'LinkeraiTTS';

-- Xóa bản ghi giai điệu TTS được liên kết với LinkeraiTTS
DELETE FROM `ai_tts_voice` WHERE `tts_model_id` = 'TTS_LinkeraiTTS';
