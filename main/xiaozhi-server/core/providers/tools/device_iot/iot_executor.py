"""IoTcông cụ"""

import json
import asyncio
from typing import Dict, Any
from ..base import ToolType, ToolDefinition, ToolExecutor
from plugins_func.register import Action, ActionResponse


class DeviceIoTExecutor(ToolExecutor):
    """IoTcông cụ"""

    def __init__(self, conn):
        self.conn = conn
        self.iot_tools: Dict[str, ToolDefinition] = {}

    async def execute(
        self, conn, tool_name: str, arguments: Dict[str, Any]
    ) -> ActionResponse:
        """IoTcông cụ"""
        if not self.has_tool(tool_name):
            return ActionResponse(
                action=Action.NOTFOUND, response=f"IoTcông cụ {tool_name} không tồn tại"
            )

        try:
            # phân tíchcông cụ，lấyvà
            if tool_name.startswith("get_"):
                # ：get_devicename_property
                parts = tool_name.split("_", 2)
                if len(parts) >= 3:
                    device_name = parts[1]
                    property_name = parts[2]

                    value = await self._get_iot_status(device_name, property_name)
                    if value is not None:
                        # xử lýphản hồi
                        response_success = arguments.get(
                            "response_success", "thành công：{value}"
                        )
                        response = response_success.replace("{value}", str(value))

                        return ActionResponse(
                            action=Action.RESPONSE,
                            response=response,
                        )
                    else:
                        response_failure = arguments.get(
                            "response_failure", f"lấy{device_name}trạng thái"
                        )
                        return ActionResponse(
                            action=Action.ERROR, response=response_failure
                        )
            else:
                # kiểm soát：devicename_method
                parts = tool_name.split("_", 1)
                if len(parts) >= 2:
                    device_name = parts[0]
                    method_name = parts[1]

                    # kiểm soáttham số（phản hồitham số）
                    control_params = {
                        k: v
                        for k, v in arguments.items()
                        if k not in ["response_success", "response_failure"]
                    }

                    # gửiIoTkiểm soát
                    await self._send_iot_command(
                        device_name, method_name, control_params
                    )

                    # chờtrạng tháicập nhật
                    await asyncio.sleep(0.1)

                    response_success = arguments.get("response_success", "thành công")

                    # xử lýphản hồitrong
                    for param_name, param_value in control_params.items():
                        placeholder = "{" + param_name + "}"
                        if placeholder in response_success:
                            response_success = response_success.replace(
                                placeholder, str(param_value)
                            )
                        if "{value}" in response_success:
                            response_success = response_success.replace(
                                "{value}", str(param_value)
                            )
                            break

                    return ActionResponse(
                        action=Action.REQLLM,
                        result=response_success,
                    )

            return ActionResponse(action=Action.ERROR, response="phân tíchIoTcông cụ")

        except Exception as e:
            response_failure = arguments.get("response_failure", "thất bại")
            return ActionResponse(action=Action.ERROR, response=response_failure)

    async def _get_iot_status(self, device_name: str, property_name: str):
        """lấyIoTtrạng thái"""
        for key, value in self.conn.iot_descriptors.items():
            if key.lower() == device_name.lower():
                for property_item in value.properties:
                    if property_item["name"].lower() == property_name.lower():
                        return property_item["value"]
        return None

    async def _send_iot_command(
        self, device_name: str, method_name: str, parameters: Dict[str, Any]
    ):
        """gửiIoTkiểm soát"""
        for key, value in self.conn.iot_descriptors.items():
            if key.lower() == device_name.lower():
                for method in value.methods:
                    if method["name"].lower() == method_name.lower():
                        command = {
                            "name": key,
                            "method": method["name"],
                        }

                        if parameters:
                            command["parameters"] = parameters

                        send_message = json.dumps(
                            {"type": "iot", "commands": [command]}
                        )
                        await self.conn.websocket.send(send_message)
                        return

        raise Exception(f"đến{device_name}phương pháp{method_name}")

    def register_iot_tools(self, descriptors: list):
        """IoTcông cụ"""
        for descriptor in descriptors:
            device_name = descriptor["name"]
            device_desc = descriptor["description"]

            # công cụ
            if "properties" in descriptor:
                for prop_name, prop_info in descriptor["properties"].items():
                    tool_name = f"get_{device_name.lower()}_{prop_name.lower()}"

                    tool_desc = {
                        "type": "function",
                        "function": {
                            "name": tool_name,
                            "description": f"{device_desc}{prop_info['description']}",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "response_success": {
                                        "type": "string",
                                        "description": f"thành côngthời，làm chosử dụng{{value}}chođến",
                                    },
                                    "response_failure": {
                                        "type": "string",
                                        "description": f"thất bạithời",
                                    },
                                },
                                "required": ["response_success", "response_failure"],
                            },
                        },
                    }

                    self.iot_tools[tool_name] = ToolDefinition(
                        name=tool_name,
                        description=tool_desc,
                        tool_type=ToolType.DEVICE_IOT,
                    )

            # kiểm soátcông cụ
            if "methods" in descriptor:
                for method_name, method_info in descriptor["methods"].items():
                    tool_name = f"{device_name.lower()}_{method_name.lower()}"

                    # xây dựngtham số
                    parameters = {}
                    required_params = []

                    # thêmphương phápban đầutham số
                    if "parameters" in method_info:
                        parameters.update(
                            {
                                param_name: {
                                    "type": param_info["type"],
                                    "description": param_info["description"],
                                }
                                for param_name, param_info in method_info[
                                    "parameters"
                                ].items()
                            }
                        )
                        required_params.extend(method_info["parameters"].keys())

                    # thêmphản hồitham số
                    parameters.update(
                        {
                            "response_success": {
                                "type": "string",
                                "description": "thành côngthời",
                            },
                            "response_failure": {
                                "type": "string",
                                "description": "thất bạithời",
                            },
                        }
                    )
                    required_params.extend(["response_success", "response_failure"])

                    tool_desc = {
                        "type": "function",
                        "function": {
                            "name": tool_name,
                            "description": f"{device_desc} - {method_info['description']}",
                            "parameters": {
                                "type": "object",
                                "properties": parameters,
                                "required": required_params,
                            },
                        },
                    }

                    self.iot_tools[tool_name] = ToolDefinition(
                        name=tool_name,
                        description=tool_desc,
                        tool_type=ToolType.DEVICE_IOT,
                    )

    def get_tools(self) -> Dict[str, ToolDefinition]:
        """lấycóIoTcông cụ"""
        return self.iot_tools.copy()

    def has_tool(self, tool_name: str) -> bool:
        """kiểm tracócóchỉ địnhIoTcông cụ"""
        return tool_name in self.iot_tools
