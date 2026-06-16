import uuid
import re
from typing import List, Dict
from datetime import datetime


class Message:
    def __init__(
            self,
            role: str,
            content: str = None,
            uniq_id: str = None,
            tool_calls=None,
            tool_call_id=None,
            is_temporary=False,
    ):
        self.uniq_id = uniq_id if uniq_id is not None else str(uuid.uuid4())
        self.role = role
        self.content = content
        self.tool_calls = tool_calls
        self.tool_call_id = tool_call_id
        self.is_temporary = is_temporary  # tạm thờitin nhắn（nhưcông cụsử dụng）


class Dialogue:
    def __init__(self):
        self.dialogue: List[Message] = []
        # lấyhiện tạithời gian
        self.current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def put(self, message: Message):
        self.dialogue.append(message)

    def getMessages(self, m, dialogue):
        if m.tool_calls is not None:
            dialogue.append({"role": m.role, "tool_calls": m.tool_calls})
        elif m.role == "tool":
            dialogue.append(
                {
                    "role": m.role,
                    "tool_call_id": (
                        str(uuid.uuid4()) if m.tool_call_id is None else m.tool_call_id
                    ),
                    "content": m.content,
                }
            )
        else:
            dialogue.append({"role": m.role, "content": m.content})

    def get_llm_dialogue(self) -> List[Dict[str, str]]:
        # sử dụngget_llm_dialogue_with_memory，vàoNonechomemory_str
        # nàyđảm bảonóicó thểtạicósử dụngđường dẫn
        return self.get_llm_dialogue_with_memory(None, None)

    def update_system_message(self, new_content: str):
        """cập nhậthoặcthêmtin nhắn"""
        # mộttin nhắn
        system_msg = next((msg for msg in self.dialogue if msg.role == "system"), None)
        if system_msg:
            system_msg.content = new_content
        else:
            self.put(Message(role="system", content=new_content))

    def _ensure_tool_calls_complete(self, messages: List[Message]) -> List[Message]:
        """
        đảm bảocó tool_calls cótương ứng tool phản hồi
        bịngắt tool_calls，ngăn ngừamô hình API  400 lỗi
        """
        pending_tool_calls = set()
        result = []

        for msg in messages:
            result.append(msg)

            if msg.role == "assistant" and msg.tool_calls:
                for tc in msg.tool_calls:
                    tc_id = tc.get("id") if isinstance(tc, dict) else getattr(tc, "id", None)
                    if tc_id:
                        pending_tool_calls.add(tc_id)

            elif msg.role == "tool" and msg.tool_call_id:
                pending_tool_calls.discard(msg.tool_call_id)

        for missing_id in pending_tool_calls:
            dummy_tool_msg = Message(
                role="tool",
                content='{"status": "interrupted", "message": "đãhủy/bịngắt"}',
                tool_call_id=missing_id
            )
            result.append(dummy_tool_msg)

        return result

    def get_llm_dialogue_with_memory(
            self, memory_str: str = None, voiceprint_config: dict = None
    ) -> List[Dict[str, str]]:
        # xây dựnghội thoại
        dialogue = []

        # thêmgợi ývàký ức
        system_message = next(
            (msg for msg in self.dialogue if msg.role == "system"), None
        )

        if system_message:
            # bằng <context> cho， system prompt vàngữ cảnh
            # phần（、v.v.）không，trongtiền tốbộ nhớ đệm
            # phần（thời gian、、ký ứcv.v.）cho system tin nhắn， system 
            full_prompt = system_message.content
            context_match = re.search(r"<context>", full_prompt)
            if context_match:
                static_part = full_prompt[:context_match.start()]
                dynamic_part = full_prompt[context_match.start():]
            else:
                static_part = full_prompt
                dynamic_part = ""

            # ： system prompt（tiền tốbộ nhớ đệmtrong）
            dialogue.append({"role": "system", "content": static_part})

        # ：few-shot （phiêntrongkhông，bộ nhớ đệmtiền tốphần）
        non_system_messages = [m for m in self.dialogue if m.role != "system"]
        fewshot_messages = [m for m in non_system_messages if m.is_temporary]
        complete_fewshot = self._ensure_tool_calls_complete(fewshot_messages)
        for m in complete_fewshot:
            self.getMessages(m, dialogue)

        # ：ngữ cảnh system prompt（thời gian、ký ức、nóiv.v.）
        #  system bằngđảm bảomô hình，khôngcho user
        if system_message and dynamic_part:
            # thay thếthời gian
            dynamic_part = dynamic_part.replace(
                "{{current_time}}", datetime.now().strftime("%H:%M")
            )

            # ký ức
            if memory_str is not None:
                dynamic_part = re.sub(
                    r"<memory>.*?</memory>",
                    f"<memory>\n{memory_str}\n</memory>",
                    dynamic_part,
                    flags=re.DOTALL,
                )

            # nóithông tin
            try:
                speakers = voiceprint_config.get("speakers", [])
                if speakers:
                    dynamic_part += "\n<speakers_info>"
                    for speaker_str in speakers:
                        try:
                            parts = speaker_str.split(",", 2)
                            if len(parts) >= 2:
                                name = parts[1].strip()
                                description = (
                                    parts[2].strip() if len(parts) >= 3 else ""
                                )
                                dynamic_part += f"\n- {name}：{description}"
                        except:
                            pass
                    dynamic_part += "\n</speakers_info>"
            except:
                pass

            dialogue.append({"role": "system", "content": dynamic_part})

        # ：hội thoại（không few-shot）
        actual_messages = [m for m in non_system_messages if not m.is_temporary]
        complete_actual = self._ensure_tool_calls_complete(actual_messages)
        for m in complete_actual:
            self.getMessages(m, dialogue)

        return dialogue
