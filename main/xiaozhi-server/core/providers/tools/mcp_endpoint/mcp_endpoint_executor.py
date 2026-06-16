"""MCPvàocông cụ"""

from typing import Dict, Any
from ..base import ToolType, ToolDefinition, ToolExecutor
from plugins_func.register import Action, ActionResponse
from .mcp_endpoint_handler import call_mcp_endpoint_tool


class MCPEndpointExecutor(ToolExecutor):
    """MCPvàocông cụ"""

    def __init__(self, conn):
        self.conn = conn

    async def execute(
        self, conn, tool_name: str, arguments: Dict[str, Any]
    ) -> ActionResponse:
        """MCPvàocông cụ"""
        if not hasattr(conn, "mcp_endpoint_client") or not conn.mcp_endpoint_client:
            return ActionResponse(
                action=Action.ERROR,
                response="MCPvàomáy kháchkhởi tạo",
            )

        if not await conn.mcp_endpoint_client.is_ready():
            return ActionResponse(
                action=Action.ERROR,
                response="MCPvàomáy kháchthì",
            )

        try:
            # chuyển đổitham sốchoJSONký tự
            import json

            args_str = json.dumps(arguments) if arguments else "{}"

            # sử dụngMCPvàocông cụ
            result = await call_mcp_endpoint_tool(
                conn.mcp_endpoint_client, tool_name, args_str
            )

            resultJson = None
            if isinstance(result, str):
                try:
                    resultJson = json.loads(result)
                except Exception as e:
                    pass

            # mô hìnhkhôngqualầnLLMxử lý
            if (
                resultJson is not None
                and isinstance(resultJson, dict)
                and "action" in resultJson
            ):
                return ActionResponse(
                    action=Action[resultJson["action"]],
                    response=resultJson.get("response", ""),
                )

            return ActionResponse(action=Action.REQLLM, result=str(result))

        except ValueError as e:
            return ActionResponse(action=Action.NOTFOUND, response=str(e))
        except Exception as e:
            return ActionResponse(action=Action.ERROR, response=str(e))

    def get_tools(self) -> Dict[str, ToolDefinition]:
        """lấycóMCPvàocông cụ"""
        if (
            not hasattr(self.conn, "mcp_endpoint_client")
            or not self.conn.mcp_endpoint_client
        ):
            return {}

        tools = {}
        mcp_tools = self.conn.mcp_endpoint_client.get_available_tools()

        for tool in mcp_tools:
            func_def = tool.get("function", {})
            tool_name = func_def.get("name", "")

            if tool_name:
                tools[tool_name] = ToolDefinition(
                    name=tool_name, description=tool, tool_type=ToolType.MCP_ENDPOINT
                )

        return tools

    def has_tool(self, tool_name: str) -> bool:
        """kiểm tracócóchỉ địnhMCPvàocông cụ"""
        if (
            not hasattr(self.conn, "mcp_endpoint_client")
            or not self.conn.mcp_endpoint_client
        ):
            return False

        return self.conn.mcp_endpoint_client.has_tool(tool_name)
