-- Bảng điều khiển thông minh bật tính năng tăng tốc đánh thức từ
update `sys_params` set param_value = 'Xin chào Tiểu Chí;Xin chào Tiểu Chí;Bạn cùng lớp Tiểu Ái;Xin chào Tiểu Tân;Xin chào Tiểu Tân;Bạn cùng lớp Tiểu Mỹ;Tiểu Long Tiểu Long;Bạn cùng lớp Meo Meo;Obama Obama;Tiểu Băng Tiểu Băng;này xin chào' where param_code = 'wakeup_words';
update `sys_params` set param_value = 'true' where param_code = 'enable_wakeup_words_response_cache';
