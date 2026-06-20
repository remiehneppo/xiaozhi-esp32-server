-- bảng nhân bản âm thanh
DROP TABLE IF EXISTS `ai_voice_clone`;
CREATE TABLE `ai_voice_clone` (
    `id` VARCHAR(32) NOT NULL COMMENT 'mã định danh duy nhất',
    `name` VARCHAR(64) COMMENT 'tên âm thanh',
    `model_id` VARCHAR(32) COMMENT 'người mẫuid',
    `voice_id` VARCHAR(32) COMMENT 'âm thanhid',
    `user_id` BIGINT COMMENT 'người dùng ID（Bảng người dùng liên quan）',
    `voice` LONGBLOB COMMENT 'âm thanh',
    `train_status` TINYINT(1) DEFAULT 0 COMMENT 'tình trạng đào tạo：0Để được đào tạo 1trong đào tạo 2Đào tạo thành công 3Đào tạo không thành công',
    `train_error` VARCHAR(255) COMMENT 'Nguyên nhân dẫn đến sai sót trong đào tạo',
    `creator` BIGINT COMMENT 'Người sáng tạo ID',
    `create_date` DATETIME COMMENT 'thời gian sáng tạo',
    PRIMARY KEY (`id`),
    INDEX idx_ai_voice_clone_user_id_model_id_train_status (model_id,user_id, train_status),
    INDEX idx_ai_voice_clone_voice_id (voice_id),
    INDEX idx_ai_voice_clone_user_id (user_id),
    INDEX idx_ai_voice_clone_model_id_voice_id (model_id, voice_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='bảng nhân bản âm thanh';