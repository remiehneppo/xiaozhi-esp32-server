import os
import sys
from loguru import logger
from config.config_loader import load_config
from config.settings import check_config_file
from datetime import datetime

SERVER_VERSION = "0.9.4"
_logger_initialized = False


def get_module_abbreviation(module_name, module_dict):
    """lấy，nhưchotrả về00
    nhưtrong，trả vềsauký tự
    """
    module_value = module_dict.get(module_name, "")
    if not module_value:
        return "00"
    if "_" in module_value:
        parts = module_value.split("_")
        return parts[-1][:2] if parts[-1] else "00"
    return module_value[:2]


def build_module_string(selected_module):
    """xây dựngký tự"""
    return (
        get_module_abbreviation("VAD", selected_module)
        + get_module_abbreviation("ASR", selected_module)
        + get_module_abbreviation("LLM", selected_module)
        + get_module_abbreviation("TTS", selected_module)
        + get_module_abbreviation("Memory", selected_module)
        + get_module_abbreviation("Intent", selected_module)
        + get_module_abbreviation("VLLM", selected_module)
    )


def formatter(record):
    """chokhông có tag nhật kýthêmmặc định，vàxử lýký tự"""
    record["extra"].setdefault("tag", record["name"])
    # nhưkhông cóđặt selected_module，làm chosử dụngmặc định
    record["extra"].setdefault("selected_module", "00000000000000")
    # sẽ selected_module  extra đến，bằng {selected_module} định dạng
    record["selected_module"] = record["extra"]["selected_module"]
    return record["message"]


def setup_logging():
    check_config_file()
    """cấu hìnhtệptrongđọcnhật kýcấu hình，vàđặtnhật kýrađịnh dạngvà"""
    config = load_config()
    log_config = config["log"]
    global _logger_initialized

    # lầnkhởi tạothờicấu hìnhnhật ký
    if not _logger_initialized:
        # làm chosử dụngmặc địnhký tựtiến hànhkhởi tạo
        logger.configure(
            extra={
                "selected_module": log_config.get("selected_module", "00000000000000"),
            }
        )

        log_format = log_config.get(
            "log_format",
            "<green>{time:YYMMDD HH:mm:ss}</green>[{version}_{extra[selected_module]}][<light-blue>{extra[tag]}</light-blue>]-<level>{level}</level>-<light-green>{message}</light-green>",
        )
        log_format_file = log_config.get(
            "log_format_file",
            "{time:YYYY-MM-DD HH:mm:ss} - {version}_{extra[selected_module]} - {name} - {level} - {extra[tag]} - {message}",
        )
        log_format = log_format.replace("{version}", SERVER_VERSION)
        log_format_file = log_format_file.replace("{version}", SERVER_VERSION)

        log_level = log_config.get("log_level", "INFO")
        log_dir = log_config.get("log_dir", "tmp")
        log_file = log_config.get("log_file", "server.log")
        data_dir = log_config.get("data_dir", "data")

        os.makedirs(log_dir, exist_ok=True)
        os.makedirs(data_dir, exist_ok=True)

        # cấu hìnhnhật kýra
        logger.remove()

        # rađếnkiểm soát
        logger.add(sys.stdout, format=log_format, level=log_level, filter=formatter)

        # rađếntệp - thống nhấtthư mục，
        # nhật kýtệphoàn chỉnhđường dẫn
        log_file_path = os.path.join(log_dir, log_file)

        # thêmnhật kýxử lý
        logger.add(
            log_file_path,
            format=log_format_file,
            level=log_level,
            filter=formatter,
            rotation="10 MB",  # mỗitệp10MB
            retention="30 days",  # giữ lại30
            compression=None,
            encoding="utf-8",
            enqueue=True,  # an toàn
            backtrace=True,
            diagnose=True,
        )
        _logger_initialized = True  # chođãkhởi tạo

    return logger


def create_connection_logger(selected_module_str):
    """chokết nốitạonhật ký，ký tự"""
    return logger.bind(selected_module=selected_module_str)
