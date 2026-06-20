-- Xóa mô-đun máy chủ có bật tham số xác thực mã thông báo hay không
delete from `sys_params` where param_code = 'server.auth.enabled';

-- Thêm mô-đun máy chủ có bật tham số xác thực mã thông báo hay không
INSERT INTO `sys_params` (id, param_code, param_value, value_type, param_type, remark) VALUES 
(122, 'server.auth.enabled', 'true', 'boolean', 1, 'serverMô-đun có được kích hoạt không?tokenChứng nhận');