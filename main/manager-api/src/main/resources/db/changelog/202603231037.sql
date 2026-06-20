-- Đã thêm nhà cung cấp mô hình bộ nhớ lịch sử trò chuyện chỉ báo cáo mới

delete from `ai_model_provider` where `id` = 'SYSTEM_Memory_mem_report_only';
delete from `ai_model_config` where `id` = 'Memory_mem_report_only';

INSERT INTO `ai_model_provider` VALUES ('SYSTEM_Memory_mem_report_only', 'Memory', 'mem_report_only', 'Chỉ báo cáo lịch sử trò chuyện', '[]', 4, 1, NOW(), 1, NOW());
INSERT INTO `ai_model_config` VALUES ('Memory_mem_report_only', 'Memory', 'mem_report_only', 'Chỉ báo cáo lịch sử trò chuyện', 0, 1, '{"type": "mem_report_only"}', NULL, 'Chỉ báo cáo lịch sử trò chuyện，Không tóm tắt bộ nhớ', 3, NULL, NULL, NULL, NULL);
