update ai_agent_template set system_prompt = replace(system_prompt, 'tôi là', 'bạn là');

delete from sys_params where id in (500,501,402);
INSERT INTO `sys_params` (id, param_code, param_value, value_type, param_type, remark) VALUES (500, 'end_prompt.enable', 'true', 'boolean', 1, 'Có bật nhận xét kết luận hay không');
INSERT INTO `sys_params` (id, param_code, param_value, value_type, param_type, remark) VALUES (501, 'end_prompt.prompt', 'làm ơn“Thời gian trôi nhanh quá”người đứng đầu tương lai，với cảm xúc、Hãy kết thúc cuộc trò chuyện này bằng những lời miễn cưỡng.！', 'string', 1, 'lời nhắc kết thúc');

INSERT INTO `sys_params` (id, param_code, param_value, value_type, param_type, remark) VALUES (402, 'plugins.get_weather.api_host', 'mj7p3y7naa.re.qweatherapi.com', 'string', 1, 'Nhà phát triểnapihost');