-- Thêm tham số khóa thuật toán bí mật quốc gia SM2
-- Được sử dụng cho các chức năng mã hóa và giải mã SM2 phía máy chủ

-- Thêm tham số khóa SM2
INSERT INTO `sys_params` (id, param_code, param_value, value_type, param_type, remark) VALUES 
(120, 'server.public_key', '', 'string', 1, 'máy chủSM2khóa công khai'),
(121, 'server.private_key', '', 'string', 1, 'máy chủSM2khóa riêng');