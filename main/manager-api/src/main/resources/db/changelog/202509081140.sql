-- Thêm cấu hình tham số ngưỡng tương tự nhận dạng giọng nói
delete from `sys_params` where id = 115;
INSERT INTO `sys_params` (id, param_code, param_value, value_type, param_type, remark)
VALUES (115, 'server.voiceprint_similarity_threshold', '0.4', 'string', 1, 'Ngưỡng tương tự nhận dạng giọng nói，phạm vi0.0-1.0，Mặc định0.4，Giá trị càng cao thì quy định càng nghiêm ngặt');
