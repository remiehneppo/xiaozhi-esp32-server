import importlib
import pkgutil
from config.logger import setup_logging

TAG = __name__

logger = setup_logging()

def auto_import_modules(package_name):
    """
    vàochỉ địnhtrongcó。

    Args:
        package_name (str): ，như 'functions'。
    """
    # lấyđường dẫn
    package = importlib.import_module(package_name)
    package_path = package.__path__

    # duyệttrongcó
    for _, module_name, _ in pkgutil.iter_modules(package_path):
        # vào
        full_module_name = f"{package_name}.{module_name}"
        importlib.import_module(full_module_name)
        #logger.bind(tag=TAG).info(f" '{full_module_name}' đãtải")