-- Điều chỉnh cấu hình nhận dạng ý định
delete from `ai_model_config` where id = 'Intent_function_call';
INSERT INTO `ai_model_config` VALUES ('Intent_function_call', 'Intent', 'function_call', 'Nhận dạng ý định cuộc gọi chức năng', 0, 1, '{\"type\": \"function_call\", \"functions\": \"change_role;get_weather;get_news;play_music\"}', NULL, NULL, 3, NULL, NULL, NULL, NULL);

-- Tăng số lượng câu chat tối đa mỗi ngày trên một thiết bị
delete from `sys_params` where  id = 105;
INSERT INTO `sys_params` (id, param_code, param_value, value_type, param_type, remark) VALUES (105, 'device_max_output_size', '0', 'number', 1, 'Số lượng từ tối đa được xuất ra mỗi ngày bởi một thiết bị，0Cho biết không có hạn chế');