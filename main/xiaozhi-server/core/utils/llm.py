import os
import sys

# thêmthư mụcđếnPythonđường dẫn
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from config.logger import setup_logging
import importlib

logger = setup_logging()


def create_instance(class_name, *args, **kwargs):
    # tạoLLM
    provider_path = os.path.join(project_root, 'core', 'providers', 'llm', class_name, f'{class_name}.py')
    if os.path.exists(provider_path):
        lib_name = f'core.providers.llm.{class_name}.{class_name}'
        if lib_name not in sys.modules:
            sys.modules[lib_name] = importlib.import_module(f'{lib_name}')
        return sys.modules[lib_name].LLMProvider(*args, **kwargs)

    raise ValueError(f"khôngLLM: {class_name}，kiểm tracấu hìnhtypecóđặtđúng")
