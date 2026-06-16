import os
from config.config_loader import read_config, get_project_dir, load_config


default_config_file = "config.yaml"
config_file_valid = False


def check_config_file():
    global config_file_valid
    if config_file_valid:
        return
    """
    cấu hìnhkiểm tra，chỉgợi ýsử dụngcấu hìnhtệplàm chosử dụng
    """
    custom_config_file = get_project_dir() + "data/." + default_config_file
    if not os.path.exists(custom_config_file):
        raise FileNotFoundError(
            "khôngđếndata/.config.yamltệp，xác nhậncấu hìnhtệpcótại"
        )

    # kiểm tracóAPIđọccấu hình
    config = load_config()
    if config.get("read_config_from_api", False):
        print("APIđọccấu hình")
        old_config_origin = read_config(custom_config_file)
        if old_config_origin.get("selected_module") is not None:
            error_msg = "cấu hìnhtệpcấu hìnhcục bộcấu hình：\n"
            error_msg += "\n：\n"
            error_msg += "1、sẽthư mụcconfig_from_api.yamltệpđếndata，cho.config.yaml\n"
            error_msg += "2、cấu hìnhđịa chỉvà\n"
            raise ValueError(error_msg)
    config_file_valid = True
