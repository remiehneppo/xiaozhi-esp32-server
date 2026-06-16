import asyncio
import time
import json
import uuid
import aiohttp
import websockets
import hmac
import base64
import hashlib
import asyncio
from urllib.parse import urlparse, urlencode
from tabulate import tabulate
from config.settings import load_config

description = "Streaming TTS speech synthesis first word latency test"
class StreamTTSPerformanceTester:
    def __init__(self):
        self.config = load_config()
        self.test_texts = [
            "Xin chào, đây là một câu."
        ]
        self.results = []
    
    async def test_aliyun_tts(self, text=None, test_count=5):
        """Kiểm tratrong streaming TTS first word latency (test nhiều lần lấy trung bình)"""
        text = text or self.test_texts[0]
        latencies = []
        
        for i in range(test_count):
            try:
                tts_config = self.config["TTS"]["AliyunStreamTTS"]
                appkey = tts_config["appkey"]
                token = tts_config["token"]
                voice = tts_config["voice"]
                host = tts_config["host"]
                ws_url = f"wss://{host}/ws/v1"

                # Thống nhất điểm bắt đầu đếm thời gian: bắt đầu đếm trước khi tạo connection
                start_time = time.time()
                async with websockets.connect(ws_url, extra_headers={"X-NLS-Token": token}) as ws:
                    task_id = str(uuid.uuid4())
                    message_id = str(uuid.uuid4())

                    start_request = {
                        "header": {
                            "message_id": message_id,
                            "task_id": task_id,
                            "namespace": "FlowingSpeechSynthesizer",
                            "name": "StartSynthesis",
                            "appkey": appkey,
                        },
                        "payload": {
                            "voice": voice,
                            "format": "pcm",
                            "sample_rate": 16000,
                            "volume": 50,
                            "speech_rate": 0,
                            "pitch_rate": 0,
                            "enable_subtitle": True,
                        }
                    }
                    await ws.send(json.dumps(start_request))

                    start_response = json.loads(await ws.recv())
                    if start_response["header"]["name"] != "SynthesisStarted":
                        raise Exception("Khởi động synthesis thất bại")

                    run_request = {
                        "header": {
                            "message_id": str(uuid.uuid4()),
                            "task_id": task_id,
                            "namespace": "FlowingSpeechSynthesizer",
                            "name": "RunSynthesis",
                            "appkey": appkey,
                        },
                        "payload": {"text": text}
                    }
                    await ws.send(json.dumps(run_request))

                    while True:
                        response = await ws.recv()
                        if isinstance(response, bytes):
                            latency = time.time() - start_time
                            latencies.append(latency)
                            print(f"[trongTTS] Lần thứ {i+1} first word latency: {latency:.3f}s")
                            break
                        elif isinstance(response, str):
                            data = json.loads(response)
                            if data["header"]["name"] == "TaskFailed":
                                raise Exception(f"Synthesis thất bại: {data['payload']['error_info']}")

            except Exception as e:
                print(f"[trongTTS] Lần thứ {i+1} test thất bại: {str(e)}")
                latencies.append(None)
        
        return self._calculate_result("trongTTS", latencies, test_count)

    async def test_alibl_tts(self, text=None, test_count=5):
        """Kiểm tratrongCosyVoice streaming TTS first word latency"""
        text = text or self.test_texts[0]
        latencies = []

        for i in range(test_count):
            try:
                tts_config = self.config["TTS"]["AliBLTTS"]
                api_key = tts_config["api_key"]
                model = tts_config.get("model", "cosyvoice-v2")
                voice = tts_config.get("voice", "longxiaochun_v2")
                format_type = tts_config.get("format", "pcm")
                sample_rate = int(tts_config.get("sample_rate", "24000"))

                ws_url = "wss://dashscope.aliyuncs.com/api-ws/v1/inference/"
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "X-DashScope-DataInspection": "enable",
                }

                start_time = time.time()

                async with websockets.connect(
                    ws_url,
                    additional_headers=headers,
                    ping_interval=30,
                    ping_timeout=10,
                    close_timeout=10,
                    max_size=10 * 1024 * 1024,
                ) as ws:
                    session_id = uuid.uuid4().hex

                    # 1. Gửi run-task (khởi động task)
                    run_task_message = {
                        "header": {
                            "action": "run-task",
                            "task_id": session_id,
                            "streaming": "duplex",
                        },
                        "payload": {
                            "task_group": "audio",
                            "task": "tts",
                            "function": "SpeechSynthesizer",
                            "model": model,
                            "parameters": {
                                "text_type": "PlainText",
                                "voice": voice,
                                "format": format_type,
                                "sample_rate": sample_rate,
                                "volume": 50,
                                "rate": 1.0,
                                "pitch": 1.0,
                            },
                            "input": {}
                        },
                    }
                    await ws.send(json.dumps(run_task_message))

                    # 2. Đợi task-started event (quan trọng! phải đợi cái này rồi mới gửi text)
                    task_started = False
                    while not task_started:
                        msg = await ws.recv()
                        if isinstance(msg, str):
                            data = json.loads(msg)
                            header = data.get("header", {})
                            event = header.get("event")
                            if event == "task-started":
                                task_started = True
                                print(f"[trongTTS] Lần thứ {i+1} task khởi động thành công")
                            elif event == "task-failed":
                                raise Exception(f"Khởi động thất bại: {header.get('error_message', 'Lỗi không rõ')}")

                    # 3. Gửi continue-task (gửi text! đây là action đúng)
                    continue_task_message = {
                        "header": {
                            "action": "continue-task",  # quay lại continue-task
                            "task_id": session_id,
                            "streaming": "duplex",
                        },
                        "payload": {"input": {"text": text}},
                    }
                    await ws.send(json.dumps(continue_task_message))

                    # 4. gửi finish-task（kết thúcnhiệm vụ）
                    finish_task_message = {
                        "header": {
                            "action": "finish-task",
                            "task_id": session_id,
                            "streaming": "duplex",
                        },
                        "payload": {"input": {}}
                    }
                    await ws.send(json.dumps(finish_task_message))

                    # 5. chờmộtdữ liệu âm thanh
                    while True:
                        msg = await asyncio.wait_for(ws.recv(), timeout=15.0)
                        if isinstance(msg, (bytes, bytearray)) and len(msg) > 0:
                            latency = time.time() - start_time
                            print(f"[trongTTS] {i+1}lần độ trễ: {latency:.3f}s")
                            latencies.append(latency)
                            break
                        elif isinstance(msg, str):
                            data = json.loads(msg)
                            event = data.get("header", {}).get("event")
                            if event == "task-failed":
                                raise Exception(f"thất bại: {data}")
                            elif event == "task-finished":
                                if not latencies or latencies[-1] is None:
                                    raise Exception("nhiệm vụkết thúcnhưngđếnâm thanh")

            except Exception as e:
                print(f"[trongTTS] {i+1}lầnthất bại: {str(e)}")
                latencies.append(None)

        return self._calculate_result("trongTTS", latencies, test_count)

    async def test_doubao_tts(self, text=None, test_count=5):
        """kiểm traluồngTTSđộ trễ（kiểm tranhiềulần）"""
        text = text or self.test_texts[0]
        latencies = []
        
        for i in range(test_count):
            try:
                tts_config = self.config["TTS"]["HuoshanDoubleStreamTTS"]
                ws_url = tts_config["ws_url"]
                app_id = tts_config["appid"]
                access_token = tts_config["access_token"]
                resource_id = tts_config["resource_id"]
                speaker = tts_config["speaker"]

                start_time = time.time()
                ws_header = {
                    "X-Api-App-Key": app_id,
                    "X-Api-Access-Key": access_token,
                    "X-Api-Resource-Id": resource_id,
                    "X-Api-Connect-Id": str(uuid.uuid4()),
                }
                async with websockets.connect(ws_url, additional_headers=ws_header, max_size=1000000000) as ws:
                    session_id = uuid.uuid4().hex

                    # gửi yêu cầu khởi động phiên
                    header = bytes([
                        (0b0001 << 4) | 0b0001,  
                        0b0001 << 4 | 0b1011,     
                        0b0001 << 4 | 0b0000,
                    ])
                    optional = bytearray()
                    optional.extend((1).to_bytes(4, "big", signed=True))
                    session_id_bytes = session_id.encode()
                    optional.extend(len(session_id_bytes).to_bytes(4, "big", signed=True))
                    optional.extend(session_id_bytes)
                    payload = json.dumps({"speaker": speaker}).encode()
                    await ws.send(header + optional + len(payload).to_bytes(4, "big", signed=True) + payload)

                    # gửi văn bản
                    header = bytes([
                        (0b0001 << 4) | 0b0001,  
                        0b0001 << 4 | 0b1011,    
                        0b0001 << 4 | 0b0000,
                        0
                    ])
                    optional = bytearray()
                    optional.extend((200).to_bytes(4, "big", signed=True))
                    session_id_bytes = session_id.encode()
                    optional.extend(len(session_id_bytes).to_bytes(4, "big", signed=True))
                    optional.extend(session_id_bytes)
                    payload = json.dumps({"text": text, "speaker": speaker}).encode()
                    await ws.send(header + optional + len(payload).to_bytes(4, "big", signed=True) + payload)

                    first_chunk = await ws.recv()
                    latency = time.time() - start_time
                    latencies.append(latency)
                    print(f"[TTS] {i+1}lần độ trễ: {latency:.3f}s")

            except Exception as e:
                print(f"[TTS] {i+1}lầnkiểm trathất bại: {str(e)}")
                latencies.append(None)
        
        return self._calculate_result("TTS", latencies, test_count)

    async def test_paddlespeech_tts(self, text=None, test_count=5):
        """kiểm traPaddleSpeechluồngTTSđộ trễ（kiểm tranhiềulần）"""
        text = text or self.test_texts[0]
        latencies = []
        
        for i in range(test_count):
            try:
                tts_config = self.config["TTS"]["PaddleSpeechTTS"]
                tts_url = tts_config["url"]
                spk_id = tts_config["spk_id"]
                speed = tts_config["speed"]
                volume = tts_config["volume"]

                start_time = time.time()
                async with websockets.connect(tts_url) as ws:
                    # gửi yêu cầu bắt đầu
                    await ws.send(json.dumps({
                        "task": "tts",
                        "signal": "start"
                    }))
                    
                    start_response = json.loads(await ws.recv())
                    if start_response.get("status") != 0:
                        raise Exception("kết nốithất bại")
                    
                    # gửi văn bảndữ liệu
                    await ws.send(json.dumps({
                        "text": text,
                        "spk_id": spk_id,
                        "speed": speed,
                        "volume": volume
                    }))
                    
                    # nhận khối dữ liệu đầu tiên
                    first_chunk = await ws.recv()
                    latency = time.time() - start_time
                    latencies.append(latency)
                    print(f"[PaddleSpeechTTS] {i+1}lần độ trễ: {latency:.3f}s")

                    # gửi yêu cầu kết thúc
                    end_request = {
                        "task": "tts",
                        "signal": "end"
                    }
                    await ws.send(json.dumps(end_request))

                    # đảm bảo đóng kết nối bình thường
                    try:
                        await ws.recv()
                    except websockets.exceptions.ConnectionClosedOK:
                        pass

            except Exception as e:
                print(f"[PaddleSpeechTTS] {i+1}lầnkiểm trathất bại: {str(e)}")
                latencies.append(None)
        
        return self._calculate_result("PaddleSpeechTTS", latencies, test_count)
            
    async def test_indexstream_tts(self, text=None, test_count=5):
        """kiểm traIndexStreamluồngTTSđộ trễ（kiểm tranhiềulần）"""
        text = text or self.test_texts[0]
        latencies = []
        
        for i in range(test_count):
            try:
                tts_config = self.config["TTS"]["IndexStreamTTS"]
                api_url = tts_config.get("api_url")
                voice = tts_config.get("voice")

                # Thống nhất điểm bắt đầu đếm thời gian: bắt đầu đếm trước khi tạo connection
                start_time = time.time()

                async with aiohttp.ClientSession() as session:
                    payload = {"text": text, "character": voice}
                    async with session.post(api_url, json=payload, timeout=10) as resp:
                        if resp.status != 200:
                            raise Exception(f"yêu cầuthất bại: {resp.status}, {await resp.text()}")

                        async for chunk in resp.content.iter_any():
                            data = chunk[0] if isinstance(chunk, (list, tuple)) else chunk
                            if not data:
                                continue

                            latency = time.time() - start_time
                            latencies.append(latency)
                            print(f"[IndexStreamTTS] {i+1}lần độ trễ: {latency:.3f}s")
                            resp.close()
                            break
                        else:
                            latencies.append(None)

            except Exception as e:
                print(f"[IndexStreamTTS] {i+1}lầnkiểm trathất bại: {str(e)}")
                latencies.append(None)
        
        return self._calculate_result("IndexStreamTTS", latencies, test_count)

    async def test_linkerai_tts(self, text=None, test_count=5):
        """kiểm traLinkerailuồngTTSđộ trễ（kiểm tranhiềulần）"""
        text = text or self.test_texts[0]
        latencies = []
        
        for i in range(test_count):
            try:
                tts_config = self.config["TTS"]["LinkeraiTTS"]
                api_url = tts_config["api_url"]
                access_token = tts_config["access_token"]
                voice = tts_config["voice"]

                # Thống nhất điểm bắt đầu đếm thời gian: bắt đầu đếm trước khi tạo connection
                start_time = time.time()
                async with aiohttp.ClientSession() as session:
                    params = {
                        "tts_text": text,
                        "spk_id": voice,
                        "frame_durition": 60,
                        "stream": "true",
                        "target_sr": 16000,
                        "audio_format": "pcm",
                        "instruct_text": "tạocủgiọng nói",
                    }
                    headers = {
                        "Authorization": f"Bearer {access_token}",
                        "Content-Type": "application/json",
                    }

                    async with session.get(api_url, params=params, headers=headers, timeout=10) as resp:
                        if resp.status != 200:
                            raise Exception(f"yêu cầuthất bại: {resp.status}, {await resp.text()}")

                        # nhận khối dữ liệu đầu tiên
                        async for _ in resp.content.iter_any():
                            latency = time.time() - start_time
                            latencies.append(latency)
                            print(f"[LinkeraiTTS] {i+1}lần độ trễ: {latency:.3f}s")
                            break
                        else:
                            latencies.append(None)

            except Exception as e:
                print(f"[LinkeraiTTS] {i+1}lầnkiểm trathất bại: {str(e)}")
                latencies.append(None)
        
        return self._calculate_result("LinkeraiTTS", latencies, test_count)
    
    async def test_xunfei_tts(self, text=None, test_count=5):
        """kiểm traluồngTTSđộ trễ（kiểm tranhiềulần）"""
        text = text or self.test_texts[0]
        latencies = []
        
        for i in range(test_count):
            try:
                # sửa tên nút cấu hình, khớp với XunFeiTTS trong tệp cấu hình
                tts_config = self.config["TTS"]["XunFeiTTS"]
                app_id = tts_config["app_id"]
                api_key = tts_config["api_key"]
                api_secret = tts_config["api_secret"]
                api_url = tts_config.get("api_url", "wss://cbm01.cn-huabei-1.xf-yun.com/v1/private/mcd9m97e6")
                voice = tts_config.get("voice", "x5_lingxiaoxuan_flow")
                # tạo URL xác thực
                auth_url = self._create_xunfei_auth_url(api_key, api_secret, api_url)
                start_time = time.time()
                async with websockets.connect(
                    auth_url,
                    ping_interval=30,
                    ping_timeout=10,
                    close_timeout=10,
                    max_size=1000000000
                ) as ws:
                    # xây dựng yêu cầu
                    request = self._build_xunfei_request(app_id, text, voice)
                    await ws.send(json.dumps(request))
                    # chờ khối dữ liệu âm thanh đầu tiên
                    first_audio_received = False
                    while not first_audio_received:
                        msg = await asyncio.wait_for(ws.recv(), timeout=10)
                        data = json.loads(msg)
                        header = data.get("header", {})
                        code = header.get("code")

                        if code != 0:
                            message = header.get("message", "lỗi không xác định")
                            raise Exception(f"thất bại: {code} - {message}")

                        payload = data.get("payload", {})
                        audio_payload = payload.get("audio", {})

                        if audio_payload:
                            status = audio_payload.get("status", 0)
                            audio_data = audio_payload.get("audio", "")
                            if status == 1 and audio_data:
                                # nhận khối dữ liệu âm thanh đầu tiên
                                latency = time.time() - start_time
                                latencies.append(latency)
                                print(f"[TTS] {i+1}lần độ trễ: {latency:.3f}s")
                                first_audio_received = True
                                break
            except Exception as e:
                print(f"[TTS] {i+1}lầnkiểm trathất bại: {str(e)}")
                latencies.append(None)
        
        return self._calculate_result("TTS", latencies, test_count)
    
    def _create_xunfei_auth_url(self, api_key, api_secret, api_url):
        """tạoWebSocketxác thựcURL"""
        parsed_url = urlparse(api_url)
        host = parsed_url.netloc
        path = parsed_url.path
        
        # lấy thời gian UTC, Xunfei yêu cầu định dạng RFC1123
        now = time.gmtime()
        date = time.strftime('%a, %d %b %Y %H:%M:%S GMT', now)
        
        # xây dựng chuỗi ký tự chữ ký
        signature_origin = f"host: {host}\ndate: {date}\nGET {path} HTTP/1.1"
        
        # tính toán chữ ký
        signature_sha = hmac.new(
            api_secret.encode('utf-8'),
            signature_origin.encode('utf-8'),
            digestmod=hashlib.sha256
        ).digest()
        signature_sha_base64 = base64.b64encode(signature_sha).decode(encoding='utf-8')
        
        # xây dựng authorization
        authorization_origin = f'api_key="{api_key}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        
        # xây dựng URL WebSocket cuối cùng
        v = {
            "authorization": authorization,
            "date": date,
            "host": host
        }
        url = api_url + '?' + urlencode(v)
        return url
    
    def _build_xunfei_request(self, app_id, text, voice):
        """xây dựngTTSyêu cầu"""
        return {
            "header": {
                "app_id": app_id,
                "status": 2,
            },
            "parameter": {
                "oral": {
                    "oral_level": "mid",
                    "spark_assist": 1,
                    "stop_split": 0,
                    "remain": 0
                },
                "tts": {
                    "vcn": voice,
                    "speed": 50,
                    "volume": 50,
                    "pitch": 50,
                    "bgs": 0,
                    "reg": 0,
                    "rdn": 0,
                    "rhy": 0,
                    "audio": {
                        "encoding": "raw",
                        "sample_rate": 24000,
                        "channels": 1,
                        "bit_depth": 16,
                        "frame_size": 0
                    }
                }
            },
            "payload": {
                "text": {
                    "encoding": "utf8",
                    "compress": "raw",
                    "format": "plain",
                    "status": 2,
                    "seq": 1,
                    "text": base64.b64encode(text.encode('utf-8')).decode('utf-8')
                }
            }
        }


    def _calculate_result(self, service_name, latencies, test_count):
        """tính toánkiểm trakết quả（đúngxử lýNone，thất bạikiểm tra）"""
        # thất bạicủkiểm tra（Nonevà<=0độ trễ），chỉthống kêhiệu quảđộ trễ
        valid_latencies = [l for l in latencies if l is not None and l > 0]
        if valid_latencies:
            avg_latency = sum(valid_latencies) / len(valid_latencies)
            status = f"thành công（{len(valid_latencies)}/{test_count}lầnhiệu quả）"
        else:
            avg_latency = 0
            status = "thất bại: cókiểm trathất bại"
        return {"name": service_name, "latency": avg_latency, "status": status}

    def _print_results(self, test_text, test_count):
        """In kết quả kiểm tra"""
        if not self.results:
            print("cóhiệu quảcủTTSkiểm trakết quả")
            return

        print(f"\n{'='*60}")
        print("luồngTTSđộ trễkiểm trakết quả")
        print(f"{'='*60}")
        print(f"kiểm travăn bản: {test_text}")
        print(f"kiểm tralần: mỗiTTSdịch vụkiểm tra {test_count} lần")

        # sắp xếpkết quả：thành côngưu tiên，theođộ trễ
        success_results = sorted(
            [r for r in self.results if "thành công" in r["status"]],
            key=lambda x: x["latency"]
        )
        failed_results = [r for r in self.results if "thành công" not in r["status"]]

        table_data = [
            [r["name"], f"{r['latency']:.3f}", r["status"]]
            for r in success_results + failed_results
        ]

        print(tabulate(table_data, headers=["TTSdịch vụ", "độ trễ()", "trạng thái"], tablefmt="grid"))
        print("\nkiểm tranói：từkết nốiđếnnhậnmộtdữ liệu âm thanhcủkhi/thời（、、gửivăn bản），nhiềulầnkiểm tra")
        print("- khi/thời: WebSocket/HTTPkết nối（thống nhất、、gửivăn bản）")
        print("- quá thời gian: yêu cầuchờkhi/thờicho10")
        print("- saixử lý: thất bạicủkiểm trakhôngvào，chỉthống kêthành côngkiểm tracủđộ trễ")
        print("- sắp xếp: theokhi/thờitừđếnsắp xếp")


    async def run(self, test_text=None, test_count=5):
        """kiểm tra
        
        Args:
            test_text: phảikiểm tracủvăn bản，nhưchoNonelàm chosử dụngmặc địnhvăn bản
            test_count: mỗiTTSdịch vụcủkiểm tralần
        """
        test_text = test_text or self.test_texts[0]
        print(f"bắt đầuluồngTTSđộ trễkiểm tra...")
        print(f"kiểm travăn bản: {test_text}")
        print(f"mỗiTTSdịch vụkiểm tralần: {test_count}lần")
        
        if not self.config.get("TTS"):
            print("cấu hìnhtệptrongđếnTTScấu hình")
            return
        
        # kiểm traTTSdịch vụ
        self.results = []
        
        # kiểm tratrongTTS
        result = await self.test_aliyun_tts(test_text, test_count)
        self.results.append(result)

        # kiểm tratrongTTS
        if self.config.get("TTS", {}).get("AliBLTTS"):
            result = await self.test_alibl_tts(test_text, test_count)
            self.results.append(result)

        # kiểm traTTS
        result = await self.test_doubao_tts(test_text, test_count)
        self.results.append(result)
        
        # kiểm traPaddleSpeech TTS
        result = await self.test_paddlespeech_tts(test_text, test_count)
        self.results.append(result)
        
        # kiểm traLinkerai TTS
        result = await self.test_linkerai_tts(test_text, test_count)
        self.results.append(result)
        
        # kiểm traIndexStreamTTS
        result = await self.test_indexstream_tts(test_text, test_count)
        self.results.append(result)
        
        # kiểm traTTS
        if self.config.get("TTS", {}).get("XunFeiTTS"):
            result = await self.test_xunfei_tts(test_text, test_count)
            self.results.append(result)
        
        # In kết quả
        self._print_results(test_text, test_count)


async def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="luồngTTSđộ trễkiểm tracông cụ")
    parser.add_argument("--text", help="phảikiểm tracủvăn bảnbên trong")
    parser.add_argument("--count", type=int, default=5, help="mỗiTTSdịch vụcủkiểm tralần")
    
    args = parser.parse_args()
    await StreamTTSPerformanceTester().run(args.text, args.count)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())