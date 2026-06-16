import asyncio
import time
import json
import uuid
import os
import websockets
import gzip
import random
from urllib import parse
from tabulate import tabulate
from config.settings import load_config
import tempfile
import wave
import hmac
import base64
import hashlib
from datetime import datetime
from wsgiref.handlers import format_date_time
from time import mktime
description = "luồngASRđộ trễkiểm tra"
try:
    import dashscope
except ImportError:
    dashscope = None

class BaseASRTester:
    def __init__(self, config_key: str):
        self.config = load_config()
        self.config_key = config_key
        self.asr_config = self.config.get("ASR", {}).get(config_key, {})
        self.test_audio_files = self._load_test_audio_files()
        self.results = []

    def _load_test_audio_files(self):
        audio_root = os.path.join(os.getcwd(), "config", "assets")
        test_files = []
        if os.path.exists(audio_root):
            for file_name in os.listdir(audio_root):
                if file_name.endswith(('.wav', '.pcm')):
                    file_path = os.path.join(audio_root, file_name)
                    with open(file_path, 'rb') as f:
                        test_files.append({
                            'data': f.read(),
                            'path': file_path,
                            'name': file_name
                        })
        return test_files

    async def test(self, test_count=5):
        raise NotImplementedError

    def _calculate_result(self, service_name, latencies, test_count):
        """tính toánkiểm trakết quả（：đúngxử lýNone，thất bạikiểm tra）"""
        # None（thất bạicủkiểm tra）vàkhông hiệu quảđộ trễ，chỉthống kêhiệu quảđộ trễ
        valid_latencies = [l for l in latencies if l is not None and l > 0]
        if valid_latencies:
            avg_latency = sum(valid_latencies) / len(valid_latencies)
            status = f"thành công（{len(valid_latencies)}/{test_count}lầnhiệu quả）"
        else:
            avg_latency = 0
            status = "thất bại: cókiểm trathất bại"
        return {"name": service_name, "latency": avg_latency, "status": status}


class DoubaoStreamASRTester(BaseASRTester):
    def __init__(self):
        super().__init__("DoubaoStreamASR")
        from core.providers.asr.doubao_stream import ASRProvider as DoubaoStreamProvider
        self.provider = DoubaoStreamProvider(self.asr_config, delete_audio_file=False)

    async def test(self, test_count=5):
        if not self.test_audio_files:
            return {"name": "luồngASR", "latency": 0, "status": "thất bại: đếnkiểm traâm thanh"}
        if not self.asr_config:
            return {"name": "luồngASR", "latency": 0, "status": "thất bại: cấu hình"}

        latencies = []
        for i in range(test_count):
            try:
                start_time = time.time()

                headers = self.provider.token_auth()

                async with websockets.connect(
                    self.provider.ws_url,
                    additional_headers=headers,
                    max_size=1000000000,
                    ping_interval=None,
                    ping_timeout=None,
                    close_timeout=10
                ) as ws:
                    request_params = self.provider.construct_request(str(uuid.uuid4()))

                    payload_bytes = str.encode(json.dumps(request_params))
                    payload_bytes = gzip.compress(payload_bytes)
                    full_client_request = bytearray(self.provider.generate_header())
                    full_client_request.extend((len(payload_bytes)).to_bytes(4, "big"))
                    full_client_request.extend(payload_bytes)
                    await ws.send(full_client_request)

                    init_res = await ws.recv()
                    result = self.provider.parse_response(init_res)
                    if "code" in result and result["code"] != 1000:
                        raise Exception(f"khởi tạothất bại: {result.get('payload_msg', {}).get('error', 'lỗi không xác định')}")

                    audio_data = self.test_audio_files[0]['data']
                    if audio_data.startswith(b'RIFF'):
                        audio_data = audio_data[44:]

                    # gửi dữ liệu âm thanh（làm chosử dụngsaukhung，dịch vụâm thanhđãkết thúc）
                    payload = gzip.compress(audio_data)
                    audio_request = bytearray(self.provider.generate_last_audio_default_header())
                    audio_request.extend(len(payload).to_bytes(4, "big"))
                    audio_request.extend(payload)
                    await ws.send(audio_request)

                    first_chunk = await ws.recv()
                    latency = time.time() - start_time
                    latencies.append(latency)
                    print(f"[ASR] {i+1}lần độ trễ: {latency:.3f}s")
                    await ws.close()

            except Exception as e:
                print(f"[ASR] {i+1}lầnkiểm trathất bại: {str(e)}")
                latencies.append(None)

        return self._calculate_result("luồngASR", latencies, test_count)


class QwenASRFlashTester(BaseASRTester):
    def __init__(self):
        super().__init__("Qwen3ASRFlash")

    async def _test_single(self, audio_file_info):
        temp_file_path = None

        try:
            audio_data = audio_file_info['data']

            # ：sẽtạm thờitệpđếnkhi/thời，IOvớicó thểkiểm tracủ
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
                temp_file_path = f.name

            with wave.open(temp_file_path, 'wb') as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(16000)
                wav_file.writeframes(audio_data)

            messages = [
                {
                    "role": "user",
                    "content": [
                        {"audio": temp_file_path}
                    ]
                }
            ]

            api_key = self.asr_config.get("api_key") or os.getenv("DASHSCOPE_API_KEY")
            if not api_key:
                raise ValueError("cấu hình api_key")

            if dashscope is None:
                raise RuntimeError(" dashscope ")

            dashscope.api_key = api_key

            # thống nhấtkhi/thời：tại/trongAPIsử dụngbắt đầukhi/thời（nhưngtệpđãhoàn thành）
            start_time = time.time()

            response = dashscope.MultiModalConversation.call(
                model="qwen3-asr-flash",
                messages=messages,
                result_format="message",
                asr_options={"enable_lid": True, "enable_itn": False},
                stream=True
            )

            for chunk in response:
                latency = time.time() - start_time
                return latency

            raise Exception("luồngkết thúc，đếnphản hồi")

        except Exception as e:
            raise Exception(f"ASRluồngthất bại: {str(e)}")

        finally:
            if temp_file_path and os.path.exists(temp_file_path):
                try:
                    os.unlink(temp_file_path)
                except:
                    pass

    async def test(self, test_count=5):
        if not self.test_audio_files:
            return {"name": "ASR", "latency": 0, "status": "thất bại: đếnkiểm traâm thanh"}
        if not self.asr_config and not os.getenv("DASHSCOPE_API_KEY"):
            return {"name": "ASR", "latency": 0, "status": "thất bại: cấu hình api_key"}

        latencies = []
        for i in range(test_count):
            try:
                # print(f"\n[ASR] bắt đầu {i+1} lầnkiểm tra...")
                latency = await self._test_single(self.test_audio_files[0])
                latencies.append(latency)
                print(f"[ASR] {i+1}lần độ trễ: {latency:.3f}s")
            except Exception as e:
                # print(f"[ASR] {i+1}lầnkiểm trathất bại: {str(e)}")
                latencies.append(None)

        return self._calculate_result("ASR", latencies, test_count)


class XunfeiStreamASRTester(BaseASRTester):
    def __init__(self):
        super().__init__("XunfeiStreamASR")

    def _create_url(self):
        url = "wss://iat-api.xfyun.cn/v2/iat"
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        signature_origin = f"host: iat-api.xfyun.cn\ndate: {date}\nGET /v2/iat HTTP/1.1"
        signature_sha = hmac.new(
            self.asr_config["api_secret"].encode('utf-8'),
            signature_origin.encode('utf-8'),
            hashlib.sha256
        ).digest()
        signature_sha = base64.b64encode(signature_sha).decode()

        authorization_origin = f'api_key="{self.asr_config["api_key"]}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha}"'
        authorization = base64.b64encode(authorization_origin.encode()).decode()

        v = {"authorization": authorization, "date": date, "host": "iat-api.xfyun.cn"}
        return url + "?" + parse.urlencode(v)

    async def test(self, test_count: int = 5):
        if not self.test_audio_files:
            return {"name": "luồngASR", "latency": 0, "status": "thất bại: đếnkiểm traâm thanh"}
        if not self.asr_config:
            return {"name": "luồngASR", "latency": 0, "status": "thất bại: cấu hình"}

        required = ["app_id", "api_key", "api_secret"]
        for k in required:
            if k not in self.asr_config:
                return {"name": "luồngASR", "latency": 0, "status": f"thất bại: cấu hình {k}"}

        latencies = []
        frame_size = 1280
        audio_raw = self.test_audio_files[0]['data']
        if audio_raw.startswith(b'RIFF'):
            audio_raw = audio_raw[44:]

        for i in range(test_count):
            try:
                start_time = time.time()
                ws_url = self._create_url()

                async with websockets.connect(
                    ws_url,
                    additional_headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
                    max_size=1 << 30,
                    ping_interval=None,
                    ping_timeout=None,
                    close_timeout=30,
                ) as ws:

                    # khung：loại bỏ punc ，không xác địnhtham sốsai
                    await ws.send(json.dumps({
                        "common": {"app_id": self.asr_config["app_id"]},
                        "business": {
                            "domain": "iat",
                            "language": "zh_cn",
                            "accent": "mandarin",
                            "dwa": "wpgs",
                            "vad_eos": 5000
                            # đãloại bỏ "punc": True
                        },
                        "data": {
                            "status": 0,
                            "format": "audio/L16;rate=16000",
                            "encoding": "raw",
                            "audio": base64.b64encode(audio_raw[:frame_size]).decode()
                        }
                    }, ensure_ascii=False))

                    # saucókhung
                    pos = frame_size
                    while pos < len(audio_raw):
                        chunk = audio_raw[pos:pos + frame_size]
                        status = 2 if (pos + frame_size >= len(audio_raw)) else 1
                        await ws.send(json.dumps({
                            "data": {
                                "status": status,
                                "format": "audio/L16;rate=16000",
                                "encoding": "raw",
                                "audio": base64.b64encode(chunk).decode()
                            }
                        }, ensure_ascii=False))
                        if status == 2:
                            break
                        pos += frame_size

                    # nhận
                    first_token = True
                    async for message in ws:
                        data = json.loads(message)
                        if data.get("code") != 0:
                            raise Exception(f"sai: {data.get('message')}")

                        ws_result = data.get("data", {}).get("result", {}).get("ws")
                        if ws_result:
                            text = "".join(cw.get("w", "") for seg in ws_result for cw in seg.get("cw", []))
                            if text.strip() and first_token:
                                latency = time.time() - start_time
                                latencies.append(latency)
                                print(f"[ASR] {i+1}lần độ trễ: {latency:.3f}s")
                                first_token = False
                                break

            except Exception as e:
                print(f"[ASR] {i+1}lầnkiểm trathất bại: {str(e)}")
                latencies.append(None)

        return self._calculate_result("luồngASR", latencies, test_count)
class ASRPerformanceSuite:
    def __init__(self):
        self.testers = []
        self.results = []

    def register_tester(self, tester_class):
        try:
            tester = tester_class()
            self.testers.append(tester)
            print(f"đãkiểm tra: {tester.config_key}")
        except Exception as e:
            name_map = {
                "DoubaoStreamASRTester": "luồngASR",
                "QwenASRFlashTester": "ASR",
                "XunfeiStreamASRTester": "luồngASR"
            }
            name = name_map.get(tester_class.__name__, tester_class.__name__)
            print(f"qua {name}: {str(e)}")

    def _print_results(self, test_count):
        if not self.results:
            print("cóhiệu quảcủASRkiểm trakết quả")
            return

        print(f"\n{'='*60}")
        print("luồngASRphản hồikhi/thờikiểm trakết quả")
        print(f"{'='*60}")
        print(f"kiểm tralần: mỗiASRdịch vụkiểm tra {test_count} lần")

        success_results = sorted(
            [r for r in self.results if "thành công" in r["status"]],
            key=lambda x: x["latency"]
        )
        failed_results = [r for r in self.results if "thành công" not in r["status"]]

        table_data = [
            [r["name"], f"{r['latency']:.3f}s" if r['latency'] > 0 else "N/A", r["status"]]
            for r in success_results + failed_results
        ]

        print(tabulate(table_data, headers=["ASRdịch vụ", "độ trễ", "trạng thái"], tablefmt="grid"))
        print("\nkiểm tranói：")
        print("- khi/thời: kết nối（、gửiâm thanh、nhậnnhận dạngkết quả）")
        print("- : tạm thờitệptại/trongkhi/thờihoàn thành，IOvớikiểm tracủ")
        print("- saixử lý: thất bạicủkiểm trakhôngvào，chỉthống kêthành côngkiểm tracủđộ trễ")
        print("- sắp xếp: thành côngcủtheođộ trễ，thất bạicủtại/trongsau")

    async def run(self, test_count=5):
        print(f"bắt đầuluồngASRphản hồikhi/thờikiểm tra...")
        print(f"mỗiASRdịch vụkiểm tralần: {test_count}lần\n")

        self.results = []
        for tester in self.testers:
            print(f"\n--- kiểm tra {tester.config_key} ---")
            result = await tester.test(test_count)
            self.results.append(result)

        self._print_results(test_count)


async def main():
    import argparse
    parser = argparse.ArgumentParser(description="luồngASRphản hồikhi/thờikiểm tracông cụ")
    parser.add_argument("--count", type=int, default=5, help="kiểm tralần")
    args = parser.parse_args()

    suite = ASRPerformanceSuite()
    suite.register_tester(DoubaoStreamASRTester)
    suite.register_tester(QwenASRFlashTester)
    suite.register_tester(XunfeiStreamASRTester)

    await suite.run(args.count)


if __name__ == "__main__":
    asyncio.run(main())