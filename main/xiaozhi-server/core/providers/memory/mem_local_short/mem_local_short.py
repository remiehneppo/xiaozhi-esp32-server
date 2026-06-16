from ..base import MemoryProviderBase, logger
import time
import json
import os
import yaml
from config.config_loader import get_project_dir
from config.manage_api_client import generate_and_save_chat_summary
import asyncio
from core.utils.util import check_model_key


short_term_memory_prompt = """
# khi/thờiký ức

## làm cho
xây dựngcủký ức，tại/trongcóbên tronggiữ lạithông tincủkhi/thời，có thểthông tin
theovớighi lại，usercủquan trọngthông tin，bằngtại/trongđếncủvớitronghơncủdịch vụ

## ký ức
### 1. ký ức（lầncập nhật）
|        |                   |  |
|------------|---------------------------|--------|
| khi/thời     | thông tin（theovớilần） | 40%    |
|    | 💖/và/cũnglần     | 35%    |
|    | vớinó/của nóthông tincủkết nối      | 25%    |

### 2. cập nhật
**hơnxử lý：**
ban đầuký ức："sử dụng": [""], "sử dụng": ""
：đến「tôiX」「tôiY」v.v.khi/thời
：
1. sẽcũvào"sử dụng"
2. ghi lạikhi/thời："2024-02-15 14:32:sử dụng"
3. tại/trongký ức：「từđếncủ」

### 3. 
- **thông tinnén**：sử dụng
  - ✅"[//🐱]"
  - ❌"，"
- ****：≥900khi/thời
  1. xóa<60và3và/cũngcủthông tin
  2. và（giữ lạikhi/thờicủ）

## ký ức
rađịnh dạngchophân tíchcủjsonký tự，khôngcần、vànói，lưuký ứckhi/thờichỉtừvớithông tin，khôngphảivàobên trong
```json
{
  "khi/thời": {
    "": {
      "sử dụng": "",
      "": [] 
    },
    "ký ức": [
      {
        "": "vào",
        "khi/thời": "2024-03-20",
        "": 0.9,
        "": [""],
        "": 30 
      }
    ]
  },
  "": {
    "": {"": 12},
    "": [""]
  },
  "phản hồi": {
    "": ["xử lýcủnhiệm vụ"], 
    "tại/trong": ["củ"]
  },
  "": [
    "củ，củ，usercủ"
  ]
}
```
"""


def extract_json_data(json_code):
    start = json_code.find("```json")
    # từstartbắt đầuđếnmột```kết thúc
    end = json_code.find("```", start + 1)
    # print("start:", start, "end:", end)
    if start == -1 or end == -1:
        try:
            jsonData = json.loads(json_code)
            return json_code
        except Exception as e:
            print("Error:", e)
        return ""
    jsonData = json_code[start + 7 : end]
    return jsonData


TAG = __name__


class MemoryProvider(MemoryProviderBase):
    def __init__(self, config, summary_memory):
        super().__init__(config)
        self.short_memory = ""
        self.save_to_file = True
        self.memory_path = get_project_dir() + "data/.memory.yaml"
        self.load_memory(summary_memory)

    def init_memory(
        self, role_id, llm, summary_memory=None, save_to_file=True, **kwargs
    ):
        super().init_memory(role_id, llm, **kwargs)
        self.save_to_file = save_to_file
        self.load_memory(summary_memory)

    def load_memory(self, summary_memory):
        # apilấyđếnký ứcsautrả về
        if summary_memory or not self.save_to_file:
            self.short_memory = summary_memory
            return

        all_memory = {}
        if os.path.exists(self.memory_path):
            with open(self.memory_path, "r", encoding="utf-8") as f:
                all_memory = yaml.safe_load(f) or {}
        if self.role_id in all_memory:
            self.short_memory = all_memory[self.role_id]

    def save_memory_to_file(self):
        all_memory = {}
        if os.path.exists(self.memory_path):
            with open(self.memory_path, "r", encoding="utf-8") as f:
                all_memory = yaml.safe_load(f) or {}
        all_memory[self.role_id] = self.short_memory
        with open(self.memory_path, "w", encoding="utf-8") as f:
            yaml.dump(all_memory, f, allow_unicode=True)

    async def save_memory(self, msgs, session_id=None):
        # làm chosử dụngcủmô hìnhthông tin
        model_info = getattr(self.llm, "model_name", str(self.llm.__class__.__name__))
        logger.bind(tag=TAG).debug(f"làm chosử dụngký ứclưumô hình: {model_info}")
        api_key = getattr(self.llm, "api_key", None)
        memory_key_msg = check_model_key("ký ứcsử dụngLLM", api_key)
        if memory_key_msg:
            logger.bind(tag=TAG).error(memory_key_msg)
        if self.llm is None:
            logger.bind(tag=TAG).error("LLM is not set for memory provider")
            return None

        if len(msgs) < 2:
            return None

        msgStr = ""
        for msg in msgs:
            content = msg.content

            # Extract content from JSON format if present (for ASR with emotion/language tags)
            try:
                if content and content.strip().startswith("{") and content.strip().endswith("}"):
                    data = json.loads(content)
                    if "content" in data:
                        content = data["content"]
            except (json.JSONDecodeError, KeyError, TypeError):
                # If parsing fails, use original content
                pass

            if msg.role == "user":
                msgStr += f"User: {content}\n"
            elif msg.role == "assistant":
                msgStr += f"Assistant: {content}\n"
        if self.short_memory and len(self.short_memory) > 0:
            msgStr += "ký ức：\n"
            msgStr += self.short_memory

        # hiện tạikhi/thời
        time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        msgStr += f"hiện tạikhi/thời：{time_str}"

        if self.save_to_file:
            try:
                result = self.llm.response_no_stream(
                    short_term_memory_prompt,
                    msgStr,
                    max_tokens=2000,
                    temperature=0.2,
                )
                json_str = extract_json_data(result)
                json.loads(json_str)  # kiểm trajsonđịnh dạnglàđúng
                self.short_memory = json_str
                self.save_memory_to_file()
            except Exception as e:
                logger.bind(tag=TAG).error(f"Error in saving memory: {e}")
        else:
            # save_to_filechoFalsekhi/thời，sử dụngJavacủghi lại
            summary_id = session_id if session_id else self.role_id
            await generate_and_save_chat_summary(summary_id)
        logger.bind(tag=TAG).info(
            f"Save memory successful - Role: {self.role_id}, Session: {session_id}"
        )

        return self.short_memory

    async def query_memory(self, query: str) -> str:
        return self.short_memory
