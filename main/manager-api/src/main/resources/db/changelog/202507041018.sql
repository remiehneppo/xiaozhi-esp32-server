DROP TABLE IF EXISTS ai_agent_voice_print;
create table ai_agent_voice_print (
  id varchar(32) NOT NULL COMMENT 'giọng nóiID',
  agent_id varchar(32)  NOT NULL COMMENT 'đại lý liên kếtID',
  source_name varchar(50)  NOT NULL COMMENT 'Tên của người có giọng nói đến từ',
  introduce varchar(200) COMMENT 'Mô tả người có giọng nói phát ra',
  create_date DATETIME COMMENT 'thời gian sáng tạo',
  creator bigint COMMENT 'Người sáng tạo',
  update_date DATETIME COMMENT 'thời gian sửa đổi',
  updater bigint COMMENT 'Công cụ sửa đổi',
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Bảng in giọng nói thông minh'