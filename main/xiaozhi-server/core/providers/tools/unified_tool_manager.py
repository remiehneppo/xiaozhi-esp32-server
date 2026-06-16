"""thống nhấtcông cụ"""

from typing import Dict, List, Optional, Any
from config.logger import setup_logging
from plugins_func.register import Action, ActionResponse
from .base import ToolType, ToolDefinition, ToolExecutor


class ToolManager:
    """thống nhấtcông cụ，cócông cụ"""

    def __init__(self, conn):
        self.conn = conn
        self.logger = setup_logging()
        self.executors: Dict[ToolType, ToolExecutor] = {}
        self._cached_tools: Optional[Dict[str, ToolDefinition]] = None
        self._cached_function_descriptions: Optional[List[Dict[str, Any]]] = None

    def register_executor(self, tool_type: ToolType, executor: ToolExecutor):
        """công cụ"""
        self.executors[tool_type] = executor
        self._invalidate_cache()
        self.logger.debug(f"công cụ: {tool_type.value}")

    def _invalidate_cache(self):
        """làm chobộ nhớ đệm"""
        self._cached_tools = None
        self._cached_function_descriptions = None

    def get_all_tools(self) -> Dict[str, ToolDefinition]:
        """lấycócông cụđịnh nghĩa"""
        if self._cached_tools is not None:
            return self._cached_tools

        all_tools = {}
        for tool_type, executor in self.executors.items():
            try:
                tools = executor.get_tools()
                for name, definition in tools.items():
                    if name in all_tools:
                        self.logger.warning(f"công cụ: {name}")
                    all_tools[name] = definition
            except Exception as e:
                self.logger.error(f"lấy{tool_type.value}công cụthờira: {e}")

        self._cached_tools = all_tools
        return all_tools

    def get_function_descriptions(self) -> List[Dict[str, Any]]:
        """lấycócông cụhàm（OpenAIđịnh dạng）"""
        if self._cached_function_descriptions is not None:
            return self._cached_function_descriptions

        descriptions = []
        tools = self.get_all_tools()
        for tool_definition in tools.values():
            descriptions.append(tool_definition.description)

        self._cached_function_descriptions = descriptions
        return descriptions

    def has_tool(self, tool_name: str) -> bool:
        """kiểm tracótạichỉ địnhcông cụ"""
        tools = self.get_all_tools()
        return tool_name in tools

    def get_tool_type(self, tool_name: str) -> Optional[ToolType]:
        """lấycông cụ"""
        tools = self.get_all_tools()
        tool_def = tools.get(tool_name)
        return tool_def.tool_type if tool_def else None

    async def execute_tool(
        self, tool_name: str, arguments: Dict[str, Any]
    ) -> ActionResponse:
        """công cụsử dụng"""
        try:
            # công cụ
            tool_type = self.get_tool_type(tool_name)
            if not tool_type:
                return ActionResponse(
                    action=Action.NOTFOUND,
                    response=f"công cụ {tool_name} không tồn tại",
                )

            # lấytương ứng
            executor = self.executors.get(tool_type)
            if not executor:
                return ActionResponse(
                    action=Action.ERROR,
                    response=f"công cụ {tool_type.value} ",
                )

            # công cụ
            self.logger.info(f"công cụ: {tool_name}，tham số: {arguments}")
            result = await executor.execute(self.conn, tool_name, arguments)
            self.logger.debug(f"công cụkết quả: {result}")
            return result

        except Exception as e:
            self.logger.error(f"công cụ {tool_name} thờira: {e}")
            return ActionResponse(action=Action.ERROR, response=str(e))

    def get_supported_tool_names(self) -> List[str]:
        """lấycócông cụ"""
        tools = self.get_all_tools()
        return list(tools.keys())

    def refresh_tools(self):
        """làm mớicông cụbộ nhớ đệm"""
        self._invalidate_cache()
        self.logger.debug("công cụbộ nhớ đệmđãlàm mới")

    def get_tool_statistics(self) -> Dict[str, int]:
        """lấycông cụthống kêthông tin"""
        stats = {}
        for tool_type, executor in self.executors.items():
            try:
                tools = executor.get_tools()
                stats[tool_type.value] = len(tools)
            except Exception as e:
                self.logger.error(f"lấy{tool_type.value}công cụthống kêthờira: {e}")
                stats[tool_type.value] = 0
        return stats
