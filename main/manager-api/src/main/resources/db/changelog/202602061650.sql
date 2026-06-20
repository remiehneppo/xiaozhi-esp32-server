-- Đặc tả thống nhất của dữ liệu loại ngôn ngữ ai_tts_voice
UPDATE ai_tts_voice
SET languages = CASE
    WHEN languages IN ('Tiếng Trung', 'tiếng quan thoại','phương ngữ Đông Bắc','Phương ngữ Thiên Tân','Tiếng Trung-giọng Bắc Kinh','Tiếng Trung-giọng Thanh Đảo','Tiếng Trung-giọng Hà Nam','Tiếng Trung-giọng Quảng Tây','Liêu Ninh','Thiểm Tây','Tiếng Trung-giọng Tứ Xuyên','Tiếng Trung-giọng Đài Loan','Tiếng Trung-Giọng Trường Sa') THEN 'tiếng quan thoại'
    WHEN languages IN ('Tiếng Trung và tiếng Trung và tiếng Anh hỗn hợp', 'Tiếng Trung、Tiếng Anh', 'Tiếng Trung、Tiếng Anh Mỹ','Tiếng Trung-giọng Bắc Kinh、Tiếng Anh','Tiếng Trung(Đông Bắc)và hỗn hợp tiếng Trung và tiếng Anh') THEN 'tiếng quan thoại、Tiếng Anh'
    WHEN languages IN ('Tiếng Anh của người Anh', 'Tiếng Anh của người Anh', 'Tiếng Anh Mỹ', 'Tiếng Anh Úc', 'Tiếng Anh') THEN 'Tiếng Anh'
    WHEN languages = 'tiếng Nhật' THEN 'tiếng Nhật'
    WHEN languages = 'tiếng Nhật、tiếng Tây Ban Nha' THEN 'tiếng Nhật、người Tây Ban Nha'
    WHEN languages = 'Tiếng Hàn' THEN 'Tiếng Hàn'
    WHEN languages IN ('tiếng Quảng Đông', 'Tiếng Trung-giọng Quảng Đông') THEN 'tiếng Quảng Đông'
    WHEN languages = 'Tiếng Trung(tiếng Quảng Đông)và hỗn hợp tiếng Trung và tiếng Anh' THEN 'tiếng Quảng Đông、Tiếng Anh'
    WHEN languages = 'Hỗn hợp tiếng Quảng Đông và tiếng Quảng Đông-Anh' THEN 'tiếng Quảng Đông、Tiếng Anh'
    ELSE languages
END;

-- Thêm các trường ngôn ngữ âm sắc, âm lượng, tốc độ nói và cao độ vào bảng ai_agent
SET @col_exists = (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'ai_agent' AND COLUMN_NAME = 'tts_language');
SET @sql = IF(@col_exists = 0, 'ALTER TABLE `ai_agent` ADD COLUMN `tts_language` VARCHAR(50) NULL COMMENT ''ngôn ngữ âm sắc'' AFTER `tts_voice_id`', 'SELECT ''Column tts_language already exists'' AS msg');
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_exists = (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'ai_agent' AND COLUMN_NAME = 'tts_volume');
SET @sql = IF(@col_exists = 0, 'ALTER TABLE `ai_agent` ADD COLUMN `tts_volume` INT NULL COMMENT ''TTSkhối lượng'' AFTER `tts_language`', 'SELECT ''Column tts_volume already exists'' AS msg');
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_exists = (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'ai_agent' AND COLUMN_NAME = 'tts_rate');
SET @sql = IF(@col_exists = 0, 'ALTER TABLE `ai_agent` ADD COLUMN `tts_rate` INT NULL COMMENT ''TTStốc độ nói'' AFTER `tts_volume`', 'SELECT ''Column tts_rate already exists'' AS msg');
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_exists = (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'ai_agent' AND COLUMN_NAME = 'tts_pitch');
SET @sql = IF(@col_exists = 0, 'ALTER TABLE `ai_agent` ADD COLUMN `tts_pitch` INT NULL COMMENT ''TTScao độ'' AFTER `tts_rate`', 'SELECT ''Column tts_pitch already exists'' AS msg');
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

-- Thêm các trường ngôn ngữ âm sắc, âm lượng, tốc độ nói và cao độ vào bảng ai_agent_template
SET @col_exists = (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'ai_agent_template' AND COLUMN_NAME = 'tts_language');
SET @sql = IF(@col_exists = 0, 'ALTER TABLE `ai_agent_template` ADD COLUMN `tts_language` VARCHAR(50) NULL COMMENT ''ngôn ngữ âm sắc'' AFTER `tts_voice_id`', 'SELECT ''Column tts_language already exists'' AS msg');
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_exists = (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'ai_agent_template' AND COLUMN_NAME = 'tts_volume');
SET @sql = IF(@col_exists = 0, 'ALTER TABLE `ai_agent_template` ADD COLUMN `tts_volume` INT NULL COMMENT ''TTSkhối lượng'' AFTER `tts_language`', 'SELECT ''Column tts_volume already exists'' AS msg');
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_exists = (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'ai_agent_template' AND COLUMN_NAME = 'tts_rate');
SET @sql = IF(@col_exists = 0, 'ALTER TABLE `ai_agent_template` ADD COLUMN `tts_rate` INT NULL COMMENT ''TTStốc độ nói'' AFTER `tts_volume`', 'SELECT ''Column tts_rate already exists'' AS msg');
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_exists = (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'ai_agent_template' AND COLUMN_NAME = 'tts_pitch');
SET @sql = IF(@col_exists = 0, 'ALTER TABLE `ai_agent_template` ADD COLUMN `tts_pitch` INT NULL COMMENT ''TTScao độ'' AFTER `tts_rate`', 'SELECT ''Column tts_pitch already exists'' AS msg');
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;