-- Xóa cấu hình MiniMax TTS không phát trực tuyến, giữ lại phiên bản phát trực tuyến

-- Xóa cấu hình mô hình MiniMax TTS không phát trực tuyến cũ
DELETE FROM `ai_model_config` WHERE `id` = 'TTS_MinimaxTTS';

-- Xóa nội dung không phát trực tuyến cũMiniMax TTSCấu hình nhà cung cấp
DELETE FROM `ai_model_provider` WHERE `id` = 'SYSTEM_TTS_minimax';

-- Đã xóa cấu hình bản vá MiniMax TTS không phát trực tuyến cũ
DELETE FROM `ai_tts_voice` WHERE `tts_model_id` = 'TTS_MinimaxTTS';
