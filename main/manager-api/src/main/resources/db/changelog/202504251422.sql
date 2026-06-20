-- Thêm server.ota để định cấu hình địa chỉ ota

delete from `sys_params` where id = 100;
delete from `sys_params` where id = 101;

delete from `sys_params` where id = 106;
INSERT INTO `sys_params` (id, param_code, param_value, value_type, param_type, remark) VALUES (106, 'server.websocket', 'null', 'string', 1, 'websocketđịa chỉ，Sử dụng nhiều lần;riêng biệt');

delete from `sys_params` where id = 107;
INSERT INTO `sys_params` (id, param_code, param_value, value_type, param_type, remark) VALUES (107, 'server.ota', 'null', 'string', 1, 'otađịa chỉ');


-- Thêm bảng thông tin firmware
CREATE TABLE IF NOT EXISTS `ai_ota` (
  `id` varchar(32) NOT NULL COMMENT 'ID',
  `firmware_name` varchar(100) DEFAULT NULL COMMENT 'Tên chương trình cơ sở',
  `type` varchar(50) DEFAULT NULL COMMENT 'Loại phần mềm',
  `version` varchar(50) DEFAULT NULL COMMENT 'số phiên bản',
  `size` bigint DEFAULT NULL COMMENT 'kích thước tập tin(Byte)',
  `remark` varchar(500) DEFAULT NULL COMMENT 'Bình luận/Mô tả',
  `firmware_path` varchar(255) DEFAULT NULL COMMENT 'Đường dẫn phần sụn',
  `sort` int unsigned DEFAULT '0' COMMENT 'sắp xếp',
  `updater` bigint DEFAULT NULL COMMENT 'Trình cập nhật',
  `update_date` datetime DEFAULT NULL COMMENT 'Thời gian cập nhật',
  `creator` bigint DEFAULT NULL COMMENT 'Người sáng tạo',
  `create_date` datetime DEFAULT NULL COMMENT 'thời gian sáng tạo',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Bảng thông tin phần mềm';

update ai_device set auto_update = 1;
