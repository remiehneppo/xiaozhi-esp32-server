-- Nhà cung cấp mô hình VLLM
delete from `ai_model_provider` where id = 'SYSTEM_VLLM_openai';
INSERT INTO `ai_model_provider` (`id`, `model_type`, `provider_code`, `name`, `fields`, `sort`, `creator`, `create_date`, `updater`, `update_date`) VALUES
('SYSTEM_VLLM_openai', 'VLLM', 'openai', 'OpenAIgiao diện', '[{"key":"base_url","label":"Khái niệm cơ bảnURL","type":"string"},{"key":"model_name","label":"Tên mẫu","type":"string"},{"key":"api_key","label":"APIchìa khóa","type":"string"}]', 9, 1, NOW(), 1, NOW());

-- Cấu hình mô hình VLLM
delete from `ai_model_config` where id = 'VLLM_ChatGLMVLLM';
INSERT INTO `ai_model_config` VALUES ('VLLM_ChatGLMVLLM', 'VLLM', 'ChatGLMVLLM', 'Tầm nhìn thông minhAI', 1, 1, '{\"type\": \"openai\", \"model_name\": \"glm-4v-flash\", \"base_url\": \"https://open.bigmodel.cn/api/paas/v4/\", \"api_key\": \"của bạnapi_key\"}', NULL, NULL, 1, NULL, NULL, NULL, NULL);

-- Cập nhật tài liệu
UPDATE `ai_model_config` SET 
`doc_link` = 'https://bigmodel.cn/usercenter/proj-mgmt/apikeys',
`remark` = 'Tầm nhìn thông minhAIHướng dẫn cấu hình：
1. chuyến thăm https://bigmodel.cn/usercenter/proj-mgmt/apikeys
2. Đăng ký và nhậnAPIchìa khóa
3. Điền vào tập tin cấu hình' WHERE `id` = 'VLLM_ChatGLMVLLM';


-- Thêm thông số
INSERT INTO `sys_params` (id, param_code, param_value, value_type, param_type, remark) VALUES (113, 'server.http_port', '8003', 'number', 1, 'httpcảng dịch vụ，Được sử dụng để khởi động giao diện phân tích trực quan');
INSERT INTO `sys_params` (id, param_code, param_value, value_type, param_type, remark) VALUES (114, 'server.vision_explain', 'null', 'string', 1, 'Địa chỉ giao diện phân tích trực quan，Dùng để giao tới thiết bị，Sử dụng nhiều lần;riêng biệt');

-- Thêm cấu hình mô hình VLLM vào bề mặt thân máy thông minh
ALTER TABLE `ai_agent` 
ADD COLUMN `vllm_model_id` varchar(32) NULL DEFAULT 'VLLM_ChatGLMVLLM' COMMENT 'Nhận dạng mô hình trực quan' AFTER `llm_model_id`;

-- Đã thêm cấu hình mô hình VLLM vào bảng mẫu tác nhân
ALTER TABLE `ai_agent_template` 
ADD COLUMN `vllm_model_id` varchar(32) NULL DEFAULT 'VLLM_ChatGLMVLLM' COMMENT 'Nhận dạng mô hình trực quan' AFTER `llm_model_id`;