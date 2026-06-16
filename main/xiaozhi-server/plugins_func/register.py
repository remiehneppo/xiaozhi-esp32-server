from config.logger import setup_logging
from enum import Enum

TAG = __name__

logger = setup_logging()


class ToolType(Enum):
    NONE = (1, "sử dụngcông cụsau，khôngnó")
    WAIT = (2, "sử dụngcông cụ，chờhàmtrả về")
    CHANGE_SYS_PROMPT = (3, "sửa đổigợi ý，hoặc")
    SYSTEM_CTL = (
        4,
        "kiểm soát，hội thoại，nhưthoát、v.v.，cầnconntham số",
    )
    IOT_CTL = (5, "IOTkiểm soát，cầnconntham số")
    MCP_CLIENT = (6, "MCPmáy khách")

    def __init__(self, code, message):
        self.code = code
        self.message = message


class Action(Enum):
    ERROR = (-1, "lỗi")
    NOTFOUND = (0, "không cóđếnhàm")
    NONE = (1, "không")
    RESPONSE = (2, "")
    REQLLM = (3, "sử dụnghàmsauyêu cầullmtạo")
    RECORD = (4, "ghi lạicông cụsử dụngđếnhội thoại，khôngsử dụngLLM")

    def __init__(self, code, message):
        self.code = code
        self.message = message


class ActionResponse:
    def __init__(self, action: Action, result=None, response=None):
        self.action = action  # 
        self.result = result  # kết quả
        self.response = response  # nội dung


class FunctionItem:
    def __init__(self, name, description, func, type):
        self.name = name
        self.description = description
        self.func = func
        self.type = type


class DeviceTypeRegistry:
    """，dùng choIOTvànóhàm"""

    def __init__(self):
        self.type_functions = {}  # type_signature -> {func_name: FunctionItem}

    def generate_device_type_id(self, descriptor):
        """thông quacó thểtạoID"""
        properties = sorted(descriptor["properties"].keys())
        methods = sorted(descriptor["methods"].keys())
        # làm chosử dụngvàphương phápcho
        type_signature = (
            f"{descriptor['name']}:{','.join(properties)}:{','.join(methods)}"
        )
        return type_signature

    def get_device_functions(self, type_id):
        """lấytương ứngcóhàm"""
        return self.type_functions.get(type_id, {})

    def register_device_type(self, type_id, functions):
        """vànóhàm"""
        if type_id not in self.type_functions:
            self.type_functions[type_id] = functions


# khởi tạohàm
all_function_registry = {}


def register_function(name, desc, type=None):
    """hàmđếnhàm"""

    def decorator(func):
        all_function_registry[name] = FunctionItem(name, desc, func, type)
        logger.bind(tag=TAG).debug(f"hàm '{name}' đãtải，có thểlàm chosử dụng")
        return func

    return decorator


def register_device_function(name, desc, type=None):
    """hàmđếnhàm"""

    def decorator(func):
        logger.bind(tag=TAG).debug(f"hàm '{name}' đãtải")
        return func

    return decorator


class FunctionRegistry:
    def __init__(self):
        self.function_registry = {}
        self.logger = setup_logging()

    def register_function(self, name, func_item=None):
        # nhưfunc_item，
        if func_item:
            self.function_registry[name] = func_item
            self.logger.bind(tag=TAG).debug(f"hàm '{name}' thành công")
            return func_item

        # all_function_registrytrong
        func = all_function_registry.get(name)
        if not func:
            self.logger.bind(tag=TAG).error(f"hàm '{name}' đến")
            return None
        self.function_registry[name] = func
        self.logger.bind(tag=TAG).debug(f"hàm '{name}' thành công")
        return func

    def unregister_function(self, name):
        # hàm，cótại
        if name not in self.function_registry:
            self.logger.bind(tag=TAG).error(f"hàm '{name}' đến")
            return False
        self.function_registry.pop(name, None)
        self.logger.bind(tag=TAG).info(f"hàm '{name}' thành công")
        return True

    def get_function(self, name):
        return self.function_registry.get(name)

    def get_all_functions(self):
        return self.function_registry

    def get_all_function_desc(self):
        return [func.description for _, func in self.function_registry.items()]
