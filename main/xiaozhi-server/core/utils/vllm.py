import os
import sys

# thêmthư mụcđếnPythonđường dẫn
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
sys.path.insert(0, project_root)

from config.logger import setup_logging
import importlib

logger = setup_logging()


def create_instance(class_name, *args, **kwargs):
    # tạoLLM
    provider_path = os.path.join(project_root, "core", "providers", "vllm", f"{class_name}.py")
    if os.path.exists(provider_path):
        lib_name = f"core.providers.vllm.{class_name}"
        if lib_name not in sys.modules:
            sys.modules[lib_name] = importlib.import_module(f"{lib_name}")
        return sys.modules[lib_name].VLLMProvider(*args, **kwargs)

    raise ValueError(f"khôngVLLM: {class_name}，kiểm tracấu hìnhtypecóđặtđúng")
