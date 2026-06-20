-- Cập nhật nhà cung cấp ASR phát trực tuyến Beanbag và thêm cấu hình end_window_size
delete from `ai_model_provider` where id = 'SYSTEM_ASR_DoubaoStreamASR';
INSERT INTO `ai_model_provider` (`id`, `model_type`, `provider_code`, `name`, `fields`, `sort`, `creator`, `create_date`, `updater`, `update_date`) VALUES
('SYSTEM_ASR_DoubaoStreamASR', 'ASR', 'doubao_stream', 'Nhận dạng giọng nói động cơ núi lửa(phát trực tuyến)', '[{"key":"appid","label":"ứng dụngID","type":"string"},{"key":"access_token","label":"mã thông báo truy cập","type":"string"},{"key":"cluster","label":"cụm","type":"string"},{"key":"boosting_table_name","label":"Tên file từ nóng","type":"string"},{"key":"correct_table_name","label":"Thay thế tên file word","type":"string"},{"key":"output_dir","label":"Thư mục đầu ra","type":"string"},{"key":"end_window_size","label":"Thời gian phán xét im lặng(ms)","type":"number"}]', 3, 1, NOW(), 1, NOW());


-- Cập nhật cấu hình mô hình ASR phát trực tuyến của Beanbao và tăng giá trị mặc định của end_window_size
UPDATE `ai_model_config` SET
`config_json` = JSON_SET(`config_json`, '$.end_window_size', 200)
WHERE `id` = 'ASR_DoubaoStreamASR' AND JSON_EXTRACT(`config_json`, '$.end_window_size') IS NULL;
