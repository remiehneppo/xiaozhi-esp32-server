-- Sửa đổi tên mô hình bộ nhớ

UPDATE `ai_model_config` SET `model_name` = 'trí nhớ ngắn hạn cục bộ（Bộ nhớ tóm tắt）' WHERE `id` = 'Memory_mem_local_short';
UPDATE `ai_model_provider` SET `name` = 'trí nhớ ngắn hạn cục bộ（Bộ nhớ tóm tắt）' WHERE `id` = 'SYSTEM_Memory_mem_local_short';

UPDATE `ai_model_config` SET `model_name` = 'Chỉ báo cáo lịch sử trò chuyện（Không tóm tắt bộ nhớ）' WHERE `id` = 'Memory_mem_report_only';
UPDATE `ai_model_provider` SET `name` = 'Chỉ báo cáo lịch sử trò chuyện（Không tóm tắt bộ nhớ）' WHERE `id` = 'SYSTEM_Memory_mem_report_only';
