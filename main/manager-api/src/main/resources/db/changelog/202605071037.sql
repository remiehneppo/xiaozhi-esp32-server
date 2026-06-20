-- Xóa nhà cung cấp có mã_nhà cung cấp là ttson
DELETE FROM `ai_model_provider` WHERE `provider_code` = 'ttson';

-- Xóa cấu hình trong đó model_code là ACGNTTS
DELETE FROM `ai_model_config` WHERE `model_code` = 'ACGNTTS';
