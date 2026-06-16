"""Processor endpoint MCPvào"""

import json
import asyncio
import re
import websockets
from config.logger import setup_logging
from .mcp_endpoint_client import MCPEndpointClient

TAG = __name__
logger = setup_logging()


async def connect_mcp_endpoint(mcp_endpoint_url: str, conn=None) -> MCPEndpointClient:
    """Kết nối đến MCPvào"""
    if not mcp_endpoint_url or "your" in mcp_endpoint_url or mcp_endpoint_url == "null":
        return None

    try:
        websocket = await websockets.connect(mcp_endpoint_url)

        mcp_client = MCPEndpointClient(conn)
        mcp_client.set_websocket(websocket)

        # Khởi động message monitor
        asyncio.create_task(_message_listener(mcp_client))

        # Gửi initialization message
        await send_mcp_endpoint_initialize(mcp_client)

        # Gửi notification initialization hoàn thành
        await send_mcp_endpoint_notification(mcp_client, "notifications/initialized")

        # Lấy danh sách tools
        await send_mcp_endpoint_tools_list(mcp_client)

        logger.bind(tag=TAG).info("MCPvào connection thành công")
        return mcp_client

    except Exception as e:
        logger.bind(tag=TAG).error(f"Kết nối MCPvào thất bại: {e}")
        return None


async def _message_listener(mcp_client: MCPEndpointClient):
    """Monitor MCPvào messages"""
    try:
        async for message in mcp_client.websocket:
            await handle_mcp_endpoint_message(mcp_client, message)
    except websockets.exceptions.ConnectionClosed:
        logger.bind(tag=TAG).info("MCPvào connection đã đóng")
    except Exception as e:
        logger.bind(tag=TAG).error(f"MCPvào message monitor lỗi: {e}")
    finally:
        await mcp_client.set_ready(False)


async def handle_mcp_endpoint_message(mcp_client: MCPEndpointClient, message: str):
    """Xử lý MCPvào messages"""
    try:
        payload = json.loads(message)
        logger.bind(tag=TAG).debug(f"Nhận MCPvào message: {payload}")

        if not isinstance(payload, dict):
            logger.bind(tag=TAG).error("MCPvào message format lỗi")
            return

        # Handle result
        if "result" in payload:
            result = payload["result"]
            # Lấy message ID an toàn, nếu là None thì dùng 0
            msg_id_raw = payload.get("id")
            msg_id = int(msg_id_raw) if msg_id_raw is not None else 0

            # Check for tool call response first
            if msg_id in mcp_client.call_results:
                logger.bind(tag=TAG).debug(
                    f"Nhận tool call response, ID: {msg_id}, kết quả: {result}"
                )
                await mcp_client.resolve_call_result(msg_id, result)
                return

            if msg_id == 1:  # mcpInitializeID
                logger.bind(tag=TAG).debug("Nhận MCPvào initialization response")
                if result is not None and isinstance(result, dict):
                    server_info = result.get("serverInfo")
                    if isinstance(server_info, dict):
                        name = server_info.get("name")
                        version = server_info.get("version")
                        logger.bind(tag=TAG).info(
                            f"MCPvào server info: name={name}, version={version}"
                        )
                else:
                    logger.bind(tag=TAG).warning(
                        "MCPvào initialization response kết quả là rỗng hoặc format lỗi"
                    )
                return

            elif msg_id == 2:  # mcpToolsListID
                logger.bind(tag=TAG).debug("đếnMCPvàocông cụphản hồi")
                if (
                    result is not None
                    and isinstance(result, dict)
                    and "tools" in result
                ):
                    tools_data = result["tools"]
                    if not isinstance(tools_data, list):
                        logger.bind(tag=TAG).error("công cụđịnh dạngsai")
                        return

                    logger.bind(tag=TAG).info(
                        f"MCPvàocủcông cụ: {len(tools_data)}"
                    )

                    for i, tool in enumerate(tools_data):
                        if not isinstance(tool, dict):
                            continue

                        name = tool.get("name", "")
                        description = tool.get("description", "")
                        input_schema = {
                            "type": "object",
                            "properties": {},
                            "required": [],
                        }

                        if "inputSchema" in tool and isinstance(
                            tool["inputSchema"], dict
                        ):
                            schema = tool["inputSchema"]
                            input_schema["type"] = schema.get("type", "object")
                            input_schema["properties"] = schema.get("properties", {})
                            input_schema["required"] = [
                                s
                                for s in schema.get("required", [])
                                if isinstance(s, str)
                            ]

                        new_tool = {
                            "name": name,
                            "description": description,
                            "inputSchema": input_schema,
                        }
                        await mcp_client.add_tool(new_tool)
                        logger.bind(tag=TAG).debug(f"MCPvàocông cụ #{i+1}: {name}")

                    # thay thếcócông cụtrongcủcông cụ
                    for tool_data in mcp_client.tools.values():
                        if "description" in tool_data:
                            description = tool_data["description"]
                            # duyệtcócông cụtiến hànhthay thế
                            for (
                                sanitized_name,
                                original_name,
                            ) in mcp_client.name_mapping.items():
                                description = description.replace(
                                    original_name, sanitized_name
                                )
                            tool_data["description"] = description

                    next_cursor = (
                        result.get("nextCursor", "") if result is not None else ""
                    )
                    if next_cursor:
                        logger.bind(tag=TAG).info(
                            f"cóhơnnhiềucông cụ，nextCursor: {next_cursor}"
                        )
                        await send_mcp_endpoint_tools_list_continue(
                            mcp_client, next_cursor
                        )
                    else:
                        await mcp_client.set_ready(True)
                        logger.bind(tag=TAG).info(
                            "cóMCPvàocông cụđãlấy，máy kháchthì"
                        )

                        # làm mớicông cụbộ nhớ đệm，đảm bảoMCPvàocông cụbịtại/tronghàmtrong
                        if (
                            hasattr(mcp_client, "conn")
                            and mcp_client.conn
                            and hasattr(mcp_client.conn, "func_handler")
                            and mcp_client.conn.func_handler
                        ):
                            mcp_client.conn.func_handler.tool_manager.refresh_tools()
                            mcp_client.conn.func_handler.current_support_functions()

                        logger.bind(tag=TAG).info(
                            f"MCPvàocông cụlấyhoàn thành， {len(mcp_client.tools)} công cụ"
                        )
                else:
                    logger.bind(tag=TAG).warning(
                        "MCPvàocông cụphản hồikết quảchohoặcđịnh dạngsai"
                    )
                return

        # Handle method calls (requests from the endpoint)
        elif "method" in payload:
            method = payload["method"]
            logger.bind(tag=TAG).info(f"đếnMCPvàoyêu cầu: {method}")

        elif "error" in payload:
            error_data = payload["error"]
            error_msg = error_data.get("message", "lỗi không xác định")
            logger.bind(tag=TAG).error(f"đếnMCPvàosaiphản hồi: {error_msg}")

            # Lấy message ID an toàn, nếu là None thì dùng 0
            msg_id_raw = payload.get("id")
            msg_id = int(msg_id_raw) if msg_id_raw is not None else 0

            if msg_id in mcp_client.call_results:
                await mcp_client.reject_call_result(
                    msg_id, Exception(f"MCPvàosai: {error_msg}")
                )

    except json.JSONDecodeError as e:
        logger.bind(tag=TAG).error(f"MCPvàotin nhắnJSONphân tíchthất bại: {e}")
    except Exception as e:
        logger.bind(tag=TAG).error(f"xử lýMCPvàotin nhắnkhi/thờira: {e}")
        import traceback

        logger.bind(tag=TAG).error(f"sai: {traceback.format_exc()}")


async def send_mcp_endpoint_initialize(mcp_client: MCPEndpointClient):
    """gửiMCPvàokhởi tạotin nhắn"""
    payload = {
        "jsonrpc": "2.0",
        "id": 1,  # mcpInitializeID
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "roots": {"listChanged": True},
                "sampling": {},
            },
            "clientInfo": {
                "name": "XiaozhiMCPEndpointClient",
                "version": "1.0.0",
            },
        },
    }
    message = json.dumps(payload)
    logger.bind(tag=TAG).info("gửiMCPvàokhởi tạotin nhắn")
    await mcp_client.send_message(message)


async def send_mcp_endpoint_notification(mcp_client: MCPEndpointClient, method: str):
    """gửiMCPvàothông báotin nhắn"""
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": {},
    }
    message = json.dumps(payload)
    logger.bind(tag=TAG).debug(f"gửiMCPvàothông báo: {method}")
    await mcp_client.send_message(message)


async def send_mcp_endpoint_tools_list(mcp_client: MCPEndpointClient):
    """gửiMCPvàocông cụyêu cầu"""
    payload = {
        "jsonrpc": "2.0",
        "id": 2,  # mcpToolsListID
        "method": "tools/list",
    }
    message = json.dumps(payload)
    logger.bind(tag=TAG).debug("gửiMCPvàocông cụyêu cầu")
    await mcp_client.send_message(message)


async def send_mcp_endpoint_tools_list_continue(
    mcp_client: MCPEndpointClient, cursor: str
):
    """gửicócursorcủMCPvàocông cụyêu cầu"""
    payload = {
        "jsonrpc": "2.0",
        "id": 2,  # mcpToolsListID (same ID for continuation)
        "method": "tools/list",
        "params": {"cursor": cursor},
    }
    message = json.dumps(payload)
    logger.bind(tag=TAG).info(f"gửicursorcủMCPvàocông cụyêu cầu: {cursor}")
    await mcp_client.send_message(message)


async def call_mcp_endpoint_tool(
    mcp_client: MCPEndpointClient, tool_name: str, args: str = "{}", timeout: int = 30
):
    """
    sử dụngchỉ địnhcủMCPvàocông cụ，vàchờphản hồi
    """
    if not await mcp_client.is_ready():
        raise RuntimeError("MCPvàomáy kháchthì")

    if not mcp_client.has_tool(tool_name):
        raise ValueError(f"công cụ {tool_name} khôngtại/trong")

    tool_call_id = await mcp_client.get_next_id()
    result_future = asyncio.Future()
    await mcp_client.register_call_result_future(tool_call_id, result_future)

    # xử lýtham số
    try:
        if isinstance(args, str):
            # đảm bảoký tựlàhiệu quảcủJSON
            if not args.strip():
                arguments = {}
            else:
                try:
                    # cố gắngphân tích
                    arguments = json.loads(args)
                except json.JSONDecodeError:
                    # nhưphân tíchthất bại，thửvànhiềuJSONvới
                    try:
                        # sử dụngkhớpcóJSONvới
                        json_objects = re.findall(r"\{[^{}]*\}", args)
                        if len(json_objects) > 1:
                            # vàcóJSONvới
                            merged_dict = {}
                            for json_str in json_objects:
                                try:
                                    obj = json.loads(json_str)
                                    if isinstance(obj, dict):
                                        merged_dict.update(obj)
                                except json.JSONDecodeError:
                                    continue
                            if merged_dict:
                                arguments = merged_dict
                            else:
                                raise ValueError(f"phân tíchhiệu quảcủJSONvới: {args}")
                        else:
                            raise ValueError(f"tham sốJSONphân tíchthất bại: {args}")
                    except Exception as e:
                        logger.bind(tag=TAG).error(
                            f"tham sốJSONphân tíchthất bại: {str(e)}, ban đầutham số: {args}"
                        )
                        raise ValueError(f"tham sốJSONphân tíchthất bại: {str(e)}")
        elif isinstance(args, dict):
            arguments = args
        else:
            raise ValueError(f"tham sốsai，ký tựhoặc，: {type(args)}")

        # đảm bảotham sốlà
        if not isinstance(arguments, dict):
            raise ValueError(f"tham sốlà，: {type(arguments)}")

    except Exception as e:
        if not isinstance(e, ValueError):
            raise ValueError(f"tham sốxử lýthất bại: {str(e)}")
        raise e

    actual_name = mcp_client.name_mapping.get(tool_name, tool_name)
    payload = {
        "jsonrpc": "2.0",
        "id": tool_call_id,
        "method": "tools/call",
        "params": {"name": actual_name, "arguments": arguments},
    }

    message = json.dumps(payload)
    logger.bind(tag=TAG).info(
        f"gửiMCPvàocông cụsử dụngyêu cầu: {actual_name}，tham số: {json.dumps(arguments, ensure_ascii=False)}"
    )
    await mcp_client.send_message(message)

    try:
        # Wait for response or timeout
        raw_result = await asyncio.wait_for(result_future, timeout=timeout)
        logger.bind(tag=TAG).info(
            f"MCPvàocông cụsử dụng {actual_name} thành công，ban đầukết quả: {raw_result}"
        )

        if isinstance(raw_result, dict):
            if raw_result.get("isError") is True:
                error_msg = raw_result.get(
                    "error", "công cụsử dụngtrả vềsai，nhưngsaithông tin"
                )
                raise RuntimeError(f"công cụsử dụngsai: {error_msg}")

            content = raw_result.get("content")
            if isinstance(content, list) and len(content) > 0:
                if isinstance(content[0], dict) and "text" in content[0]:
                    # trả vềvăn bảnbên trong，khôngtiến hànhJSONphân tích
                    return content[0]["text"]
        # nhưkết quảkhônglàcủđịnh dạng，sẽnó/của nóchuyển đổichoký tự
        return str(raw_result)
    except asyncio.TimeoutError:
        await mcp_client.cleanup_call_result(tool_call_id)
        raise TimeoutError("công cụsử dụngyêu cầuquá thời gian")
    except Exception as e:
        await mcp_client.cleanup_call_result(tool_call_id)
        raise e
