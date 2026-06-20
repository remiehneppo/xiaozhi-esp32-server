-- Cấu hình mô hình VLLM
delete from `ai_model_config` where id = 'VLLM_QwenVLVLLM';
INSERT INTO `ai_model_config` VALUES ('VLLM_QwenVLVLLM', 'VLLM', 'QwenVLVLLM', 'Mô hình trực quan Qianwen', 0, 1, '{\"type\": \"openai\", \"model_name\": \"qwen2.5-vl-3b-instruct\", \"base_url\": \"https://dashscope.aliyuncs.com/compatible-mode/v1\", \"api_key\": \"của bạnapi_key\"}', NULL, NULL, 2, NULL, NULL, NULL, NULL);

-- Cập nhật tài liệu
UPDATE `ai_model_config` SET 
`doc_link` = 'https://bailian.console.aliyun.com/?tab=api#/api/?type=model&url=https%3A%2F%2Fhelp.aliyun.com%2Fdocument_detail%2F2845564.html&renderType=iframe',
`remark` = 'Hướng dẫn cấu hình mô hình tầm nhìn Qianwen：
1. chuyến thăm https://bailian.console.aliyun.com/?tab=model#/api-key
2. Đăng ký và nhậnAPIchìa khóa
3. Điền vào tập tin cấu hình' WHERE `id` = 'VLLM_QwenVLVLLM';

-- Xóa các tham số. Hai tham số này đã được chuyển sang tệp cấu hình python.
delete from `sys_params` where id  in (113,114);
