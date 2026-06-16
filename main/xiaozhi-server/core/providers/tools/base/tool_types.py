"""công cụđịnh nghĩa"""

from enum import Enum

from dataclasses import dataclass
from typing import Any, Dict, Optional
from plugins_func.register import Action


class ToolType(Enum):
    """công cụ"""

    SERVER_PLUGIN = "server_plugin"  # dịch vụ
    SERVER_MCP = "server_mcp"  # dịch vụMCP
    DEVICE_IOT = "device_iot"  # IoT
    DEVICE_MCP = "device_mcp"  # MCP
    MCP_ENDPOINT = "mcp_endpoint"  # MCPvào


@dataclass
class ToolDefinition:
    """công cụđịnh nghĩa"""

    name: str  # công cụ
    description: Dict[str, Any]  # công cụ（OpenAIhàmsử dụngđịnh dạng）
    tool_type: ToolType  # công cụ
    parameters: Optional[Dict[str, Any]] = None  # ngoàitham số
