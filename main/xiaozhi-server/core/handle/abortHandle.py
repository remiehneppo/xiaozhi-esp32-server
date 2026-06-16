import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.connection import ConnectionHandler
TAG = __name__


async def handleAbortMessage(conn: "ConnectionHandler"):
    conn.logger.bind(tag=TAG).info("Abort message received")
    # đặtngắttrạng thái，sẽngắtllm、ttsnhiệm vụ
    conn.close_after_chat = False
    conn.client_abort = True
    conn.clear_queues()
    # ngắtmáy kháchnóitrạng thái
    await conn.websocket.send(
        json.dumps({"type": "tts", "state": "stop", "session_id": conn.session_id})
    )
    conn.clearSpeakStatus()
    conn.logger.bind(tag=TAG).info("Abort message received-end")
