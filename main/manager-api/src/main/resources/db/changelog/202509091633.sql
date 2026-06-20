-- Thêm cấu hình dịch vụ nhận dạng giọng nói Tongyi Qianwen Qwen3-ASR-Flash
delete from `ai_model_provider` where id = 'SYSTEM_ASR_Qwen3Flash';
INSERT INTO `ai_model_provider` (`id`, `model_type`, `provider_code`, `name`, `fields`, `sort`, `creator`, `create_date`, `updater`, `update_date`) VALUES
('SYSTEM_ASR_Qwen3Flash', 'ASR', 'qwen3_asr_flash', 'Qwen3-ASR-Flashnhận dạng giọng nói', '[{"key":"api_key","label":"APIchìa khóa","type":"password"},{"key":"base_url","label":"Địa chỉ dịch vụ","type":"string"},{"key":"model_name","label":"Tên mẫu","type":"string"},{"key":"output_dir","label":"Thư mục đầu ra","type":"string"}]', 17, 1, NOW(), 1, NOW());

delete from `ai_model_config` where id = 'ASR_Qwen3Flash';
INSERT INTO `ai_model_config` VALUES ('ASR_Qwen3Flash', 'ASR', 'Qwen3-ASR-Flash', 'Dịch vụ nhận dạng giọng nói Tongyi Qianwen', 0, 1, '{"type": "qwen3_asr_flash", "api_key": "", "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1", "model_name": "qwen3-asr-flash", "output_dir": "tmp/", "enable_lid": true, "enable_itn": true}', 'https://help.aliyun.com/zh/bailian/', 'Hỗ trợ nhận dạng đa ngôn ngữ、Nhận dạng giọng hát、Chức năng loại bỏ tiếng ồn', 20, NULL, NULL, NULL, NULL);

-- Tài liệu cập nhật về cấu hình model Qwen3-ASR-Flash
UPDATE `ai_model_config` SET 
`doc_link` = 'https://bailian.console.aliyun.com/?apiKey=1&tab=doc#/doc/?type=model&url=2979031',
`remark` = 'Tongyi QianwenQwen3-ASR-FlashHướng dẫn cấu hình：
1. Đăng nhập vào Nền tảng Bailian trên nền tảng đám mây của Alibabahttps://bailian.console.aliyun.com/
2. tạo raAPI-KEY  https://bailian.console.aliyun.com/#/api-key
3.Qwen3-ASR-FlashDựa trên cơ sở đa phương thức Tongyi Qianwen，Hỗ trợ nhận dạng đa ngôn ngữ、Nhận dạng giọng hát、Loại bỏ tiếng ồn và các chức năng khác
' WHERE `id` = 'ASR_Qwen3Flash';
