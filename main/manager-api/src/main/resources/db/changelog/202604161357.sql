-- Cập nhật tên model: qwen2.5-vl-3b-instruct thành qwen3.5-flash
UPDATE `ai_model_config` 
SET `config_json` = JSON_SET(`config_json`, '$.model_name', 'qwen3.5-flash')
WHERE `id` = 'VLLM_QwenVLVLLM' 
AND JSON_EXTRACT(`config_json`, '$.model_name') = 'qwen2.5-vl-3b-instruct';

-- Cập nhật tên model: qwen-turbo thành qwen-flash
UPDATE `ai_model_config` 
SET `config_json` = JSON_SET(`config_json`, '$.model_name', 'qwen-flash')
WHERE `id` = 'LLM_AliLLM' 
AND JSON_EXTRACT(`config_json`, '$.model_name') = 'qwen-turbo';

-- Ghi chú cập nhật: qwen-turbo được đổi thành qwen-flash
UPDATE `ai_model_config` 
SET `remark` = REPLACE(`remark`, 'qwen-turbo', 'qwen-flash')
WHERE `id` = 'LLM_AliLLM' 
AND `remark` LIKE '%qwen-turbo%';
