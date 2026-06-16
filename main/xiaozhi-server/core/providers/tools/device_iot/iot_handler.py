"""IoT，IoTvàtrạng tháixử lý"""

import asyncio
from config.logger import setup_logging
from .iot_descriptor import IotDescriptor
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.connection import ConnectionHandler

TAG = __name__
logger = setup_logging()


async def handleIotDescriptors(conn: "ConnectionHandler", descriptors):
    """xử lý"""
    wait_max_time = 5
    while (
        not hasattr(conn, "func_handler")
        or conn.func_handler is None
        or not conn.func_handler.finish_init
    ):
        await asyncio.sleep(1)
        wait_max_time -= 1
        if wait_max_time <= 0:
            logger.bind(tag=TAG).debug("kết nốivớikhông cófunc_handler")
            return

    functions_changed = False

    for descriptor in descriptors:
        # nhưdescriptorkhông cópropertiesvàmethods，bỏ qua
        if "properties" not in descriptor and "methods" not in descriptor:
            continue

        # xử lýproperties
        if "properties" not in descriptor:
            descriptor["properties"] = {}
            # methodstrongcótham sốchoproperties
            if "methods" in descriptor:
                for method_name, method_info in descriptor["methods"].items():
                    if "parameters" in method_info:
                        for param_name, param_info in method_info["parameters"].items():
                            # sẽtham sốthông tinchuyển đổichothông tin
                            descriptor["properties"][param_name] = {
                                "description": param_info["description"],
                                "type": param_info["type"],
                            }

        # tạoIOT
        iot_descriptor = IotDescriptor(
            descriptor["name"],
            descriptor["description"],
            descriptor["properties"],
            descriptor["methods"],
        )
        conn.iot_descriptors[descriptor["name"]] = iot_descriptor
        functions_changed = True

    # nhưhàm，cập nhậtfunction
    if functions_changed and hasattr(conn, "func_handler"):
        # IoTcông cụđếnthống nhấtcông cụxử lý
        await conn.func_handler.register_iot_tools(descriptors)

        conn.func_handler.current_support_functions()


async def handleIotStatus(conn: "ConnectionHandler", states):
    """xử lýtrạng thái"""
    for state in states:
        for key, value in conn.iot_descriptors.items():
            if key == state["name"]:
                for property_item in value.properties:
                    for k, v in state["state"].items():
                        if property_item["name"] == k:
                            if type(v) != type(property_item["value"]):
                                logger.bind(tag=TAG).error(
                                    f"{property_item['name']}khôngkhớp"
                                )
                                break
                            else:
                                property_item["value"] = v
                                logger.bind(tag=TAG).info(
                                    f"trạng tháicập nhật: {key} , {property_item['name']} = {v}"
                                )
                            break
                break
