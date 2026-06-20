-- Hướng dẫn cấu hình nhận dạng ý định LLM
UPDATE `ai_model_config` SET 
`doc_link` = NULL,
`remark` = 'LLMHướng dẫn cấu hình nhận dạng ý định：
1. Sử dụng độc lậpLLMThực hiện nhận dạng ý định
2. Được sử dụng theo mặc địnhselected_module.LLMngười mẫu
3. Có thể cấu hình để sử dụng độc lậpLLM（miễn phíChatGLMLLM）
4. Tính linh hoạt mạnh mẽ，Nhưng nó sẽ làm tăng thời gian xử lý
Hướng dẫn cấu hình：
1. trongllmtrường được chỉ định trongLLMngười mẫu
2. Nếu không được chỉ định，sau đó sử dụngselected_module.LLMngười mẫu' WHERE `id` = 'Intent_intent_llm';

-- Hướng dẫn cấu hình nhận dạng mục đích cuộc gọi chức năng
UPDATE `ai_model_config` SET 
`doc_link` = NULL,
`remark` = 'Hướng dẫn cấu hình nhận dạng mục đích cuộc gọi chức năng：
1. sử dụngLLMcủafunction_callchức năng nhận dạng ý định
2. Cần phải lựa chọnLLMhỗ trợfunction_call
3. Gọi công cụ theo yêu cầu，Tốc độ xử lý nhanh' WHERE `id` = 'Intent_function_call';