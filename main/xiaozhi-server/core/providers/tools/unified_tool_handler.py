"""thống nhấtcông cụxử lý"""

import json
from typing import Dict, List, Any, Optional
from config.logger import setup_logging
from plugins_func.loadplugins import auto_import_modules

from .base import ToolType
from plugins_func.register import Action, ActionResponse
from .unified_tool_manager import ToolManager
from .server_plugins import ServerPluginExecutor
from .server_mcp import ServerMCPExecutor
from .device_iot import DeviceIoTExecutor
from .device_mcp import DeviceMCPExecutor
from .mcp_endpoint import MCPEndpointExecutor
from core.handle.sendAudioHandle import send_display_message


class UnifiedToolHandler:
    """thống nhấtcông cụxử lý"""

    def __init__(self, conn):
        self.conn = conn
        self.config = conn.config
        self.logger = setup_logging()

        # tạocông cụ
        self.tool_manager = ToolManager(conn)

        # tạo
        self.server_plugin_executor = ServerPluginExecutor(conn)
        self.server_mcp_executor = ServerMCPExecutor(conn)
        self.device_iot_executor = DeviceIoTExecutor(conn)
        self.device_mcp_executor = DeviceMCPExecutor(conn)
        self.mcp_endpoint_executor = MCPEndpointExecutor(conn)

        # 
        self.tool_manager.register_executor(
            ToolType.SERVER_PLUGIN, self.server_plugin_executor
        )
        self.tool_manager.register_executor(
            ToolType.SERVER_MCP, self.server_mcp_executor
        )
        self.tool_manager.register_executor(
            ToolType.DEVICE_IOT, self.device_iot_executor
        )
        self.tool_manager.register_executor(
            ToolType.DEVICE_MCP, self.device_mcp_executor
        )
        self.tool_manager.register_executor(
            ToolType.MCP_ENDPOINT, self.mcp_endpoint_executor
        )

        # khởi tạocờ
        self.finish_init = False

    async def _initialize(self):
        """khởi tạo"""
        try:
            # vào
            auto_import_modules("plugins_func.functions")

            # khởi tạodịch vụMCP
            await self.server_mcp_executor.initialize()

            # khởi tạoMCPvào
            await self._initialize_mcp_endpoint()

            # khởi tạoHome Assistant（nhưcần）
            self._initialize_home_assistant()

            self.finish_init = True
            self.logger.debug("thống nhấtcông cụxử lýkhởi tạohoàn thành")

            # rahiện tạicủcócông cụ
            self.current_support_functions()

        except Exception as e:
            self.logger.error(f"thống nhấtcông cụxử lýkhởi tạothất bại: {e}")

    async def _initialize_mcp_endpoint(self):
        """khởi tạoMCPvào"""
        try:
            from .mcp_endpoint import connect_mcp_endpoint

            # từcấu hìnhtronglấyMCPvàoURL
            mcp_endpoint_url = self.config.get("mcp_endpoint", "")

            if (
                mcp_endpoint_url
                and "củ" not in mcp_endpoint_url
                and mcp_endpoint_url != "null"
            ):
                self.logger.info(f"tại/trongkhởi tạoMCPvào: {mcp_endpoint_url}")
                mcp_endpoint_client = await connect_mcp_endpoint(
                    mcp_endpoint_url, self.conn
                )

                if mcp_endpoint_client:
                    # sẽMCPvàomáy kháchlưuđếnkết nốivớitrong
                    self.conn.mcp_endpoint_client = mcp_endpoint_client
                    self.logger.info("MCPvàokhởi tạothành công")
                else:
                    self.logger.warning("MCPvàokhởi tạothất bại")

        except Exception as e:
            self.logger.error(f"khởi tạoMCPvàothất bại: {e}")

    def _initialize_home_assistant(self):
        """khởi tạoHome Assistantgợi ý"""
        try:
            from plugins_func.functions.hass_init import append_devices_to_prompt

            append_devices_to_prompt(self.conn)
        except ImportError:
            pass  # vàosai
        except Exception as e:
            self.logger.error(f"khởi tạoHome Assistantthất bại: {e}")

    def get_functions(self) -> List[Dict[str, Any]]:
        """lấycócông cụcủhàm"""
        return self.tool_manager.get_function_descriptions()

    def current_support_functions(self) -> List[str]:
        """lấyhiện tạicủhàm"""
        func_names = self.tool_manager.get_supported_tool_names()
        self.logger.info(f"hiện tạicủhàm: {func_names}")
        return func_names

    def upload_functions_desc(self):
        """làm mớihàm"""
        self.tool_manager.refresh_tools()
        self.logger.info("hàmđãlàm mới")

    def has_tool(self, tool_name: str) -> bool:
        """kiểm tralàcóchỉ địnhcông cụ"""
        return self.tool_manager.has_tool(tool_name)

    async def handle_llm_function_call(
        self, conn, function_call_data: Dict[str, Any]
    ) -> Optional[ActionResponse]:
        """xử lýLLMhàmsử dụng"""
        try:
            # xử lýnhiềuhàmsử dụng
            if "function_calls" in function_call_data:
                responses = []
                for call in function_call_data["function_calls"]:
                    result = await self.tool_manager.execute_tool(
                        call["name"], call.get("arguments", {})
                    )
                    responses.append(result)
                return self._combine_responses(responses)

            # xử lýhàmsử dụng
            function_name = function_call_data["name"]
            arguments = function_call_data.get("arguments", {})

            # nhưargumentslàký tự，thửphân tíchchoJSON
            if isinstance(arguments, str):
                try:
                    arguments = json.loads(arguments) if arguments else {}
                except json.JSONDecodeError:
                    self.logger.error(f"phân tíchhàmtham số: {arguments}")
                    return ActionResponse(
                        action=Action.ERROR,
                        response="phân tíchhàmtham số",
                    )

            self.logger.debug(f"sử dụnghàm: {function_name}, tham số: {arguments}")

            # gửicông cụsử dụnghiển thịtin nhắnđến
            try:
                await send_display_message(self.conn, f"% {function_name}")
            except Exception as e:
                self.logger.warning(f"gửicông cụsử dụnghiển thịtin nhắnthất bại: {e}")

            # công cụsử dụng
            result = await self.tool_manager.execute_tool(function_name, arguments)
            return result

        except Exception as e:
            self.logger.error(f"xử lýfunction callsai: {e}")
            return ActionResponse(action=Action.ERROR, response=str(e))

    def _combine_responses(self, responses: List[ActionResponse]) -> ActionResponse:
        """vànhiềuhàmsử dụngcủphản hồi"""
        if not responses:
            return ActionResponse(action=Action.NONE, response="phản hồi")

        # nhưcósai，trả vềmộtsai
        for response in responses:
            if response.action == Action.ERROR:
                return response

        # vàcóthành côngcủphản hồi
        contents = []
        responses_text = []

        for response in responses:
            if response.content:
                contents.append(response.content)
            if response.response:
                responses_text.append(response.response)

        # xác địnhcủ
        final_action = Action.RESPONSE
        for response in responses:
            if response.action == Action.REQLLM:
                final_action = Action.REQLLM
                break

        return ActionResponse(
            action=final_action,
            result="; ".join(contents) if contents else None,
            response="; ".join(responses_text) if responses_text else None,
        )

    async def register_iot_tools(self, descriptors: List[Dict[str, Any]]):
        """IoTcông cụ"""
        self.device_iot_executor.register_iot_tools(descriptors)
        self.tool_manager.refresh_tools()
        self.logger.info(f"{len(descriptors)}IoTcủcông cụ")

    def get_tool_statistics(self) -> Dict[str, int]:
        """lấycông cụthống kêthông tin"""
        return self.tool_manager.get_tool_statistics()

    async def cleanup(self):
        """dọn dẹptài nguyên"""
        try:
            await self.server_mcp_executor.cleanup()

            # dọn dẹpMCPvàokết nối
            if (
                hasattr(self.conn, "mcp_endpoint_client")
                and self.conn.mcp_endpoint_client
            ):
                await self.conn.mcp_endpoint_client.close()

            self.logger.info("công cụxử lýdọn dẹphoàn thành")
        except Exception as e:
            self.logger.error(f"công cụxử lýdọn dẹpthất bại: {e}")
