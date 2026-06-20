-- bảng nhà cung cấp mô hình
DROP TABLE IF EXISTS `ai_model_provider`;
CREATE TABLE `ai_model_provider` (
    `id` VARCHAR(32) NOT NULL COMMENT 'khóa chính',
    `model_type` VARCHAR(20) COMMENT 'Loại mô hình(Memory/ASR/VAD/LLM/TTS)',
    `provider_code` VARCHAR(50) COMMENT 'loại nhà cung cấp',
    `name` VARCHAR(50) COMMENT 'tên nhà cung cấp',
    `fields` JSON COMMENT 'Danh sách trường nhà cung cấp(JSONđịnh dạng)',
    `sort` INT UNSIGNED DEFAULT 0 COMMENT 'sắp xếp',
    `creator` BIGINT COMMENT 'Người sáng tạo',
    `create_date` DATETIME COMMENT 'thời gian sáng tạo',
    `updater` BIGINT COMMENT 'Trình cập nhật',
    `update_date` DATETIME COMMENT 'Thời gian cập nhật',
    PRIMARY KEY (`id`),
    INDEX `idx_ai_model_provider_model_type` (`model_type`) COMMENT 'Tạo chỉ mục cho một loại mô hình，Được sử dụng để tìm nhanh tất cả thông tin nhà cung cấp theo một loại cụ thể'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Bảng cấu hình mô hình';

-- Bảng cấu hình mô hình
DROP TABLE IF EXISTS `ai_model_config`;
CREATE TABLE `ai_model_config` (
    `id` VARCHAR(32) NOT NULL COMMENT 'khóa chính',
    `model_type` VARCHAR(20) COMMENT 'Loại mô hình(Memory/ASR/VAD/LLM/TTS)',
    `model_code` VARCHAR(50) COMMENT 'mã hóa mô hình(Chẳng hạn nhưAliLLM、DoubaoTTS)',
    `model_name` VARCHAR(50) COMMENT 'Tên mẫu',
    `is_default` TINYINT(1) DEFAULT 0 COMMENT 'Nó có được cấu hình theo mặc định không?(0Không 1Có)',
    `is_enabled` TINYINT(1) DEFAULT 0 COMMENT 'Có bật hay không',
    `config_json` JSON COMMENT 'Cấu hình mô hình(JSONđịnh dạng)',
    `doc_link` VARCHAR(200) COMMENT 'Liên kết tài liệu chính thức',
    `remark` VARCHAR(255) COMMENT 'Bình luận',
    `sort` INT UNSIGNED DEFAULT 0 COMMENT 'sắp xếp',
    `creator` BIGINT COMMENT 'Người sáng tạo',
    `create_date` DATETIME COMMENT 'thời gian sáng tạo',
    `updater` BIGINT COMMENT 'Trình cập nhật',
    `update_date` DATETIME COMMENT 'Thời gian cập nhật',
    PRIMARY KEY (`id`),
    INDEX `idx_ai_model_config_model_type` (`model_type`) COMMENT 'Tạo chỉ mục cho một loại mô hình，Được sử dụng để tìm nhanh tất cả thông tin cấu hình theo một loại cụ thể'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Bảng cấu hình mô hình';

-- Bảng giai điệu TTS
DROP TABLE IF EXISTS `ai_tts_voice`;
CREATE TABLE `ai_tts_voice` (
    `id` VARCHAR(32) NOT NULL COMMENT 'khóa chính',
    `tts_model_id` VARCHAR(32) COMMENT 'tương ứng TTS Khóa chính của mô hình',
    `name` VARCHAR(20) COMMENT 'Tên giọng nói',
    `tts_voice` VARCHAR(50) COMMENT 'mã hóa âm sắc',
    `languages` VARCHAR(50) COMMENT 'Ngôn ngữ',
    `voice_demo` VARCHAR(500) DEFAULT NULL COMMENT 'âm sắc Demo',
    `remark` VARCHAR(255) COMMENT 'Bình luận',
    `sort` INT UNSIGNED DEFAULT 0 COMMENT 'sắp xếp',
    `creator` BIGINT COMMENT 'Người sáng tạo',
    `create_date` DATETIME COMMENT 'thời gian sáng tạo',
    `updater` BIGINT COMMENT 'Trình cập nhật',
    `update_date` DATETIME COMMENT 'Thời gian cập nhật',
    PRIMARY KEY (`id`),
    INDEX `idx_ai_tts_voice_tts_model_id` (`tts_model_id`) COMMENT 'tạo ra TTS Chỉ mục của khóa chính của mô hình，Dùng để tìm nhanh thông tin âm sắc của model tương ứng'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='TTS bảng giai điệu';

-- Bảng mẫu cấu hình đại lý
DROP TABLE IF EXISTS `ai_agent_template`;
CREATE TABLE `ai_agent_template` (
    `id` VARCHAR(32) NOT NULL COMMENT 'Mã định danh duy nhất của đại lý',
    `agent_code` VARCHAR(36) COMMENT 'mã hóa đại lý',
    `agent_name` VARCHAR(64) COMMENT 'Tên đại lý',
    `asr_model_id` VARCHAR(32) COMMENT 'Nhận dạng mô hình nhận dạng giọng nói',
    `vad_model_id` VARCHAR(64) COMMENT 'Logo phát hiện hoạt động giọng nói',
    `llm_model_id` VARCHAR(32) COMMENT 'Mã định danh mô hình ngôn ngữ lớn',
    `tts_model_id` VARCHAR(32) COMMENT 'Nhận dạng mô hình tổng hợp giọng nói',
    `tts_voice_id` VARCHAR(32) COMMENT 'nhận dạng âm sắc',
    `mem_model_id` VARCHAR(32) COMMENT 'mã định danh mô hình bộ nhớ',
    `intent_model_id` VARCHAR(32) COMMENT 'Mã nhận dạng mô hình ý định',
    `system_prompt` TEXT COMMENT 'Thông số cài đặt ký tự',
    `lang_code` VARCHAR(10) COMMENT 'mã hóa ngôn ngữ',
    `language` VARCHAR(10) COMMENT 'ngôn ngữ tương tác',
    `sort` INT UNSIGNED DEFAULT 0 COMMENT 'Phân loại trọng lượng',
    `creator` BIGINT COMMENT 'Người sáng tạo ID',
    `created_at` DATETIME COMMENT 'thời gian sáng tạo',
    `updater` BIGINT COMMENT 'Trình cập nhật ID',
    `updated_at` DATETIME COMMENT 'Thời gian cập nhật',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Bảng mẫu cấu hình đại lý';

-- Bảng cấu hình đại lý
DROP TABLE IF EXISTS `ai_agent`;
CREATE TABLE `ai_agent` (
    `id` VARCHAR(32) NOT NULL COMMENT 'Mã định danh duy nhất của đại lý',
    `user_id` BIGINT COMMENT 'người dùng ID',
    `agent_code` VARCHAR(36) COMMENT 'mã hóa đại lý',
    `agent_name` VARCHAR(64) COMMENT 'Tên đại lý',
    `asr_model_id` VARCHAR(32) COMMENT 'Nhận dạng mô hình nhận dạng giọng nói',
    `vad_model_id` VARCHAR(64) COMMENT 'Logo phát hiện hoạt động giọng nói',
    `llm_model_id` VARCHAR(32) COMMENT 'Mã định danh mô hình ngôn ngữ lớn',
    `tts_model_id` VARCHAR(32) COMMENT 'Nhận dạng mô hình tổng hợp giọng nói',
    `tts_voice_id` VARCHAR(32) COMMENT 'nhận dạng âm sắc',
    `mem_model_id` VARCHAR(32) COMMENT 'mã định danh mô hình bộ nhớ',
    `intent_model_id` VARCHAR(32) COMMENT 'Mã nhận dạng mô hình ý định',
    `system_prompt` TEXT COMMENT 'Thông số cài đặt ký tự',
    `lang_code` VARCHAR(10) COMMENT 'mã hóa ngôn ngữ',
    `language` VARCHAR(10) COMMENT 'ngôn ngữ tương tác',
    `sort` INT UNSIGNED DEFAULT 0 COMMENT 'Phân loại trọng lượng',
    `creator` BIGINT COMMENT 'Người sáng tạo ID',
    `created_at` DATETIME COMMENT 'thời gian sáng tạo',
    `updater` BIGINT COMMENT 'Trình cập nhật ID',
    `updated_at` DATETIME COMMENT 'Thời gian cập nhật',
    PRIMARY KEY (`id`),
    INDEX `idx_ai_agent_user_id` (`user_id`) COMMENT 'Tạo chỉ mục người dùng，Dùng để tìm kiếm nhanh thông tin đại lý theo người dùng'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Bảng cấu hình đại lý';

-- Bảng thông tin thiết bị
DROP TABLE IF EXISTS `ai_device`;
CREATE TABLE `ai_device` (
    `id` VARCHAR(32) NOT NULL COMMENT 'Mã định danh duy nhất của thiết bị',
    `user_id` BIGINT COMMENT 'Người dùng được liên kết ID',
    `mac_address` VARCHAR(50) COMMENT 'MAC địa chỉ',
    `last_connected_at` DATETIME COMMENT 'Lần kết nối cuối cùng',
    `auto_update` TINYINT UNSIGNED DEFAULT 0 COMMENT 'Công tắc cập nhật tự động(0 Đóng/1 bật lên)',
    `board` VARCHAR(50) COMMENT 'Mô hình phần cứng thiết bị',
    `alias` VARCHAR(64) DEFAULT NULL COMMENT 'Bí danh thiết bị',
    `agent_id` VARCHAR(32) COMMENT 'đại lý ID',
    `app_version` VARCHAR(20) COMMENT 'Số phiên bản phần sụn',
    `sort` INT UNSIGNED DEFAULT 0 COMMENT 'sắp xếp',
    `creator` BIGINT COMMENT 'Người sáng tạo',
    `create_date` DATETIME COMMENT 'thời gian sáng tạo',
    `updater` BIGINT COMMENT 'Trình cập nhật',
    `update_date` DATETIME COMMENT 'Thời gian cập nhật',
    PRIMARY KEY (`id`),
    INDEX `idx_ai_device_created_at` (`mac_address`) COMMENT 'tạo ramacChỉ số của，Dùng để tìm kiếm nhanh thông tin thiết bị'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Bảng thông tin thiết bị';

-- Mẫu nhận dạng giọng nói
DROP TABLE IF EXISTS `ai_voiceprint`;
CREATE TABLE `ai_voiceprint` (
    `id` VARCHAR(32) NOT NULL COMMENT 'Mã định danh duy nhất của giọng nói',
    `name` VARCHAR(64) COMMENT 'Tên dấu giọng nói',
    `user_id` BIGINT COMMENT 'người dùng ID（Bảng người dùng liên quan）',
    `agent_id` VARCHAR(32) COMMENT 'đại lý liên kết ID',
    `agent_code` VARCHAR(36) COMMENT 'Mã hóa tác nhân liên kết',
    `agent_name` VARCHAR(36) COMMENT 'Tên đại lý liên kết',
    `description` VARCHAR(255) COMMENT 'Mô tả giọng nói',
    `embedding` LONGTEXT COMMENT 'Vectơ đặc trưng của giọng nói（JSON định dạng mảng）',
    `memory` TEXT COMMENT 'dữ liệu bộ nhớ liên kết',
    `sort` INT UNSIGNED DEFAULT 0 COMMENT 'Phân loại trọng lượng',
    `creator` BIGINT COMMENT 'Người sáng tạo ID',
    `created_at` DATETIME COMMENT 'thời gian sáng tạo',
    `updater` BIGINT COMMENT 'Trình cập nhật ID',
    `updated_at` DATETIME COMMENT 'Thời gian cập nhật',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Mẫu nhận dạng giọng nói';

-- Bảng lịch sử hội thoại
DROP TABLE IF EXISTS `ai_chat_history`;
CREATE TABLE `ai_chat_history` (
    `id` VARCHAR(32) NOT NULL COMMENT 'Số cuộc trò chuyện',
    `user_id` BIGINT COMMENT 'Số người dùng',
    `agent_id` VARCHAR(32) DEFAULT NULL COMMENT 'vai trò trò chuyện',
    `device_id` VARCHAR(32) DEFAULT NULL COMMENT 'Số thiết bị',
    `message_count` INT COMMENT 'Tóm tắt thông tin',
    `creator` BIGINT COMMENT 'Người sáng tạo',
    `create_date` DATETIME COMMENT 'thời gian sáng tạo',
    `updater` BIGINT COMMENT 'Trình cập nhật',
    `update_date` DATETIME COMMENT 'Thời gian cập nhật',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Bảng lịch sử hội thoại';

-- Bảng thông tin hội thoại
DROP TABLE IF EXISTS `ai_chat_message`;
CREATE TABLE `ai_chat_message` (
    `id` VARCHAR(32) NOT NULL COMMENT 'Mã định danh duy nhất của bản ghi cuộc hội thoại',
    `user_id` BIGINT COMMENT 'Mã định danh duy nhất của người dùng',
    `chat_id` VARCHAR(64) COMMENT 'Lịch sử cuộc trò chuyện ID',
    `role` ENUM('user', 'assistant') COMMENT 'vai trò（người dùng hoặc trợ lý）',
    `content` TEXT COMMENT 'Nội dung hội thoại',
    `prompt_tokens` INT UNSIGNED DEFAULT 0 COMMENT 'Số lượng token nhắc nhở',
    `total_tokens` INT UNSIGNED DEFAULT 0 COMMENT 'tổng số token',
    `completion_tokens` INT UNSIGNED DEFAULT 0 COMMENT 'Số lượng token đầy đủ',
    `prompt_ms` INT UNSIGNED DEFAULT 0 COMMENT 'Lời khuyên tốn thời gian（mili giây）',
    `total_ms` INT UNSIGNED DEFAULT 0 COMMENT 'Tổng thời gian sử dụng（mili giây）',
    `completion_ms` INT UNSIGNED DEFAULT 0 COMMENT 'Thời gian thực hiện để hoàn thành（mili giây）',
    `creator` BIGINT COMMENT 'Người sáng tạo',
    `create_date` DATETIME COMMENT 'thời gian sáng tạo',
    `updater` BIGINT COMMENT 'Trình cập nhật',
    `update_date` DATETIME COMMENT 'Thời gian cập nhật',
    PRIMARY KEY (`id`),
    INDEX `idx_ai_chat_message_user_id_chat_id_role` (`user_id`, `chat_id`) COMMENT 'người dùng ID、phiên trò chuyện ID và chỉ số liên minh của vai trò，Được sử dụng để nhanh chóng truy xuất bản ghi cuộc trò chuyện',
    INDEX `idx_ai_chat_message_created_at` (`create_date`) COMMENT 'Chỉ số thời gian tạo，Được sử dụng để sắp xếp hoặc truy xuất các bản ghi cuộc hội thoại theo thời gian'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Bảng thông tin hội thoại';
