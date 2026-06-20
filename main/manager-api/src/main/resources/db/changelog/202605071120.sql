-- Xóa cấu hình trong đó model_code là GizwitsTTS
DELETE FROM `ai_model_config` WHERE `model_code` = 'GizwitsTTS';

-- Xóa các bản ghi giai điệu TTS liên quan
DELETE FROM `ai_tts_voice` WHERE `tts_model_id` = 'TTS_GizwitsTTS';
DELETE FROM `ai_tts_voice` WHERE `tts_model_id` = 'TTS_ACGNTTS';
