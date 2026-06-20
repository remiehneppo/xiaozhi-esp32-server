-- Tệp này được sử dụng để khởi tạo dữ liệu tham số hệ thống. Không cần thực hiện thủ công. Nó sẽ được thực hiện tự động khi dự án bắt đầu.
-- --------------------------------------------------------
-- Cấu hình quản lý tham số khởi tạo
DROP TABLE IF EXISTS sys_params;
-- Quản lý thông số
create table sys_params
(
  id                   bigint NOT NULL COMMENT 'id',
  param_code           varchar(100) COMMENT 'Mã hóa thông số',
  param_value          varchar(2000) COMMENT 'Giá trị tham số',
  value_type           varchar(20) default 'string' COMMENT 'loại giá trị：string-chuỗi，number-con số，boolean-Boolean，array-mảng',
  param_type           tinyint unsigned default 1 COMMENT 'loại   0：Thông số hệ thống   1：Thông số phi hệ thống',
  remark               varchar(200) COMMENT 'Bình luận',
  creator              bigint COMMENT 'Người sáng tạo',
  create_date          datetime COMMENT 'thời gian sáng tạo',
  updater              bigint COMMENT 'Trình cập nhật',
  update_date          datetime COMMENT 'Thời gian cập nhật',
  primary key (id),
  unique key uk_param_code (param_code)
)ENGINE=InnoDB DEFAULT CHARACTER SET utf8mb4 COMMENT='Quản lý thông số';

-- Cấu hình máy chủ
INSERT INTO `sys_params` (id, param_code, param_value, value_type, param_type, remark) VALUES (100, 'server.ip', '0.0.0.0', 'string', 1, 'Máy chủ lắng ngheIPđịa chỉ');
INSERT INTO `sys_params` (id, param_code, param_value, value_type, param_type, remark) VALUES (101, 'server.port', '8000', 'number', 1, 'Cổng nghe máy chủ');
INSERT INTO `sys_params` (id, param_code, param_value, value_type, param_type, remark) VALUES (102, 'server.secret', 'null', 'string', 1, 'khóa máy chủ');
INSERT INTO `sys_params` (id, param_code, param_value, value_type, param_type, remark) VALUES (201, 'log.log_format', '<green>{time:YYMMDD HH:mm:ss}</green>[<light-blue>{version}-{selected_module}</light-blue>][<light-blue>{extra[tag]}</light-blue>]-<level>{level}</level>-<light-green>{message}</light-green>', 'string', 1, 'Định dạng nhật ký bảng điều khiển');
INSERT INTO `sys_params` (id, param_code, param_value, value_type, param_type, remark) VALUES (202, 'log.log_format_file', '{time:YYYY-MM-DD HH:mm:ss} - {version}_{selected_module} - {name} - {level} - {extra[tag]} - {message}', 'string', 1, 'định dạng nhật ký tập tin');
INSERT INTO `sys_params` (id, param_code, param_value, value_type, param_type, remark) VALUES (203, 'log.log_level', 'INFO', 'string', 1, 'Cấp độ nhật ký');
INSERT INTO `sys_params` (id, param_code, param_value, value_type, param_type, remark) VALUES (204, 'log.log_dir', 'tmp', 'string', 1, 'Thư mục nhật ký');
INSERT INTO `sys_params` (id, param_code, param_value, value_type, param_type, remark) VALUES (205, 'log.log_file', 'server.log', 'string', 1, 'Tên tệp nhật ký');
INSERT INTO `sys_params` (id, param_code, param_value, value_type, param_type, remark) VALUES (206, 'log.data_dir', 'data', 'string', 1, 'thư mục dữ liệu');
INSERT INTO `sys_params` (id, param_code, param_value, value_type, param_type, remark) VALUES (301, 'delete_audio', 'true', 'boolean', 1, 'Có nên xóa file âm thanh sau khi sử dụng hay không');
INSERT INTO `sys_params` (id, param_code, param_value, value_type, param_type, remark) VALUES (302, 'close_connection_no_voice_time', '120', 'number', 1, 'Không có thời gian ngắt kết nối đầu vào bằng giọng nói(giây)');
INSERT INTO `sys_params` (id, param_code, param_value, value_type, param_type, remark) VALUES (303, 'tts_timeout', '10', 'number', 1, 'TTSYêu cầu hết thời gian(giây)');
INSERT INTO `sys_params` (id, param_code, param_value, value_type, param_type, remark) VALUES (304, 'enable_wakeup_words_response_cache', 'false', 'boolean', 1, 'Có bật tính năng tăng tốc từ đánh thức hay không');
INSERT INTO `sys_params` (id, param_code, param_value, value_type, param_type, remark) VALUES (305, 'enable_greeting', 'true', 'boolean', 1, 'Có bật tính năng trả lời mở đầu hay không');
INSERT INTO `sys_params` (id, param_code, param_value, value_type, param_type, remark) VALUES (306, 'enable_stop_tts_notify', 'false', 'boolean', 1, 'Có nên bật âm thanh nhắc nhở kết thúc hay không');
INSERT INTO `sys_params` (id, param_code, param_value, value_type, param_type, remark) VALUES (307, 'stop_tts_notify_voice', 'config/assets/tts_notify.mp3', 'string', 1, 'Đường dẫn file âm thanh kết thúc');
INSERT INTO `sys_params` (id, param_code, param_value, value_type, param_type, remark) VALUES (308, 'exit_commands', 'Thoát;Đóng', 'array', 1, 'Thoát khỏi danh sách lệnh');
INSERT INTO `sys_params` (id, param_code, param_value, value_type, param_type, remark) VALUES (309, 'xiaozhi', '{
  "type": "hello",
  "version": 1,
  "transport": "websocket",
  "audio_params": {
    "format": "opus",
    "sample_rate": 16000,
    "channels": 1,
    "frame_duration": 60
  }
}', 'json', 1, 'loại tro');
INSERT INTO `sys_params` (id, param_code, param_value, value_type, param_type, remark) VALUES (310, 'wakeup_words', 'Xin chào Tiểu Chí;Xin chào Tiểu Chí;Bạn cùng lớp Tiểu Ái;Xin chào Tiểu Tân;Xin chào Tiểu Tân;Bạn cùng lớp Tiểu Mỹ;Tiểu Long Tiểu Long;Bạn cùng lớp Meo Meo;Obama Obama;Tiểu Băng Tiểu Băng', 'array', 1, 'đánh thức danh sách từ，Được sử dụng để xác định các từ đánh thức');
INSERT INTO `sys_params` (id, param_code, param_value, value_type, param_type, remark) VALUES (400, 'plugins.get_weather.api_key', 'a861d0d5e7bf4ee1a83d9a9e4f96d4da', 'string', 1, 'plugin thời tiếtAPIchìa khóa');
INSERT INTO `sys_params` (id, param_code, param_value, value_type, param_type, remark) VALUES (401, 'plugins.get_weather.default_location', 'Quảng Châu', 'string', 1, 'Thành phố mặc định của plug-in thời tiết');
INSERT INTO `sys_params` (id, param_code, param_value, value_type, param_type, remark) VALUES (410, 'plugins.get_news.default_rss_url', 'https://www.chinanews.com.cn/rss/society.xml', 'string', 1, 'Mặc định plug-in tin tứcRSSđịa chỉ');
INSERT INTO `sys_params` (id, param_code, param_value, value_type, param_type, remark) VALUES (411, 'plugins.get_news.category_urls', '{"society":"https://www.chinanews.com.cn/rss/society.xml","world":"https://www.chinanews.com.cn/rss/world.xml","finance":"https://www.chinanews.com.cn/rss/finance.xml"}', 'json', 1, 'Phân loại plug-in tin tứcRSSđịa chỉ');
INSERT INTO `sys_params` (id, param_code, param_value, value_type, param_type, remark) VALUES (421, 'plugins.home_assistant.devices', 'phòng khách,đèn đồ chơi,switch.cuco_cn_460494544_cp1_on_p_2_1;phòng ngủ,đèn bàn,switch.iot_cn_831898993_socn1_on_p_2_1', 'array', 1, 'Home AssistantDanh sách thiết bị');
INSERT INTO `sys_params` (id, param_code, param_value, value_type, param_type, remark) VALUES (422, 'plugins.home_assistant.base_url', 'http://homeassistant.local:8123', 'string', 1, 'Home AssistantĐịa chỉ máy chủ');
INSERT INTO `sys_params` (id, param_code, param_value, value_type, param_type, remark) VALUES (423, 'plugins.home_assistant.api_key', 'của bạnhome assistant apimã thông báo truy cập', 'string', 1, 'Home Assistant APIchìa khóa');
INSERT INTO `sys_params` (id, param_code, param_value, value_type, param_type, remark) VALUES (430, 'plugins.play_music.music_dir', './music', 'string', 1, 'Đường dẫn lưu trữ file nhạc');
INSERT INTO `sys_params` (id, param_code, param_value, value_type, param_type, remark) VALUES (431, 'plugins.play_music.music_ext', 'mp3;wav;p3', 'array', 1, 'loại tập tin nhạc');
INSERT INTO `sys_params` (id, param_code, param_value, value_type, param_type, remark) VALUES (432, 'plugins.play_music.refresh_time', '300', 'number', 1, 'Khoảng thời gian làm mới danh sách nhạc(giây)');
