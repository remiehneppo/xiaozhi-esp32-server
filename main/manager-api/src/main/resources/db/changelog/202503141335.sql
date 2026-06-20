DROP TABLE IF EXISTS sys_user;
DROP TABLE IF EXISTS sys_params;
DROP TABLE IF EXISTS sys_user_token;
DROP TABLE IF EXISTS sys_dict_type;
DROP TABLE IF EXISTS sys_dict_data;

-- người dùng hệ thống
CREATE TABLE sys_user (
  id bigint NOT NULL COMMENT 'id',
  username varchar(50) NOT NULL COMMENT 'Tên người dùng',
  password varchar(100) COMMENT 'Mật khẩu',
  super_admin tinyint unsigned COMMENT 'siêu quản trị viên   0：Không   1：Có',
  status tinyint COMMENT 'Trạng thái  0：vô hiệu hóa   1：bình thường',
  create_date datetime COMMENT 'thời gian sáng tạo',
  updater bigint COMMENT 'Trình cập nhật',
  creator bigint COMMENT 'Người sáng tạo',
  update_date datetime COMMENT 'Thời gian cập nhật',
  primary key (id),
  unique key uk_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='người dùng hệ thống';

-- Mã thông báo người dùng hệ thống
CREATE TABLE sys_user_token (
  id bigint NOT NULL COMMENT 'id',
  user_id bigint NOT NULL COMMENT 'người dùngid',
  token varchar(100) NOT NULL COMMENT 'người dùngtoken',
  expire_date datetime COMMENT 'Thời gian hết hạn',
  update_date datetime COMMENT 'Thời gian cập nhật',
  create_date datetime COMMENT 'thời gian sáng tạo',
  PRIMARY KEY (id),
  UNIQUE KEY user_id (user_id),
  UNIQUE KEY token (token)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='người dùng hệ thốngToken';

-- Quản lý thông số
create table sys_params
(
  id                   bigint NOT NULL COMMENT 'id',
  param_code           varchar(32) COMMENT 'Mã hóa thông số',
  param_value          varchar(2000) COMMENT 'Giá trị tham số',
  param_type           tinyint unsigned default 1 COMMENT 'loại   0：Thông số hệ thống   1：Thông số phi hệ thống',
  remark               varchar(200) COMMENT 'Bình luận',
  creator              bigint COMMENT 'Người sáng tạo',
  create_date          datetime COMMENT 'thời gian sáng tạo',
  updater              bigint COMMENT 'Trình cập nhật',
  update_date          datetime COMMENT 'Thời gian cập nhật',
  primary key (id),
  unique key uk_param_code (param_code)
)ENGINE=InnoDB DEFAULT CHARACTER SET utf8mb4 COMMENT='Quản lý thông số';

-- loại từ điển
create table sys_dict_type
(
    id                   bigint NOT NULL COMMENT 'id',
    dict_type            varchar(100) NOT NULL COMMENT 'loại từ điển',
    dict_name            varchar(255) NOT NULL COMMENT 'Tên từ điển',
    remark               varchar(255) COMMENT 'Bình luận',
    sort                 int unsigned COMMENT 'sắp xếp',
    creator              bigint COMMENT 'Người sáng tạo',
    create_date          datetime COMMENT 'thời gian sáng tạo',
    updater              bigint COMMENT 'Trình cập nhật',
    update_date          datetime COMMENT 'Thời gian cập nhật',
    primary key (id),
    UNIQUE KEY(dict_type)
)ENGINE=InnoDB DEFAULT CHARACTER SET utf8mb4 COMMENT='loại từ điển';

-- dữ liệu từ điển
create table sys_dict_data
(
    id                   bigint NOT NULL COMMENT 'id',
    dict_type_id         bigint NOT NULL COMMENT 'loại từ điểnID',
    dict_label           varchar(255) NOT NULL COMMENT 'thẻ từ điển',
    dict_value           varchar(255) COMMENT 'Giá trị từ điển',
    remark               varchar(255) COMMENT 'Bình luận',
    sort                 int unsigned COMMENT 'sắp xếp',
    creator              bigint COMMENT 'Người sáng tạo',
    create_date          datetime COMMENT 'thời gian sáng tạo',
    updater              bigint COMMENT 'Trình cập nhật',
    update_date          datetime COMMENT 'Thời gian cập nhật',
    primary key (id),
    unique key uk_dict_type_value (dict_type_id, dict_value),
    key idx_sort (sort)
)ENGINE=InnoDB DEFAULT CHARACTER SET utf8mb4 COMMENT='dữ liệu từ điển';