import io
import wave
import json
import base64
import asyncio
import websockets
import numpy as np
from datetime import datetime
from config.logger import setup_logging
from core.providers.tts.base import TTSProviderBase



TAG = __name__
logger = setup_logging()


class TTSProvider(TTSProviderBase):
    TTS_PARAM_CONFIG = [
        ("ttsVolume", "volume", 0, 3, 1.0, lambda v: round(float(v), 1)),
        ("ttsRate", "speed", 0, 3, 1.0, lambda v: round(float(v), 1)),
    ]

    def __init__(self, config, delete_audio_file):
        super().__init__(config, delete_audio_file)
        self.url = config.get("url", "ws://192.168.1.10:8092/paddlespeech/tts/streaming")
        self.protocol = config.get("protocol", "websocket")
        
        if config.get("private_voice"):
            self.spk_id = int(config.get("private_voice"))
        else:
            self.spk_id = int(config.get("spk_id", "0"))

        speed = config.get("speed", 1.0)
        self.speed = float(speed) if speed else 1.0
        
        volume = config.get("volume", 1.0)
        self.volume = float(volume) if volume else 1.0
        
        self.delete_audio_file = config.get("delete_audio", True)

        # áp dụngphần trăm（nhưtại），làm chosử dụngcócấu hình
        self._apply_percentage_params(config)

        if not self.delete_audio_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = config.get("save_path")
            if save_path:
                if not save_path.endswith('.wav'):
                    save_path = f"{save_path}_{timestamp}.wav"
                else:
                    other_path = save_path[:-4]
                    save_path = f"{other_path}_{timestamp}.wav"
                self.save_path = save_path
            else:
                self.save_path = f"./streaming_tts_{timestamp}.wav"
        else:
            self.save_path = None

    async def pcm_to_wav(self, pcm_data: bytes, sample_rate: int = 24000, num_channels: int = 1,
                         bits_per_sample: int = 16) -> bytes:
        """
        sẽ PCM dữ liệuchuyển đổicho WAV tệpvàtrả vềdữ liệu
        :param pcm_data: PCM dữ liệu（ban đầu）
        :param sample_rate: âm thanhtần số lấy mẫu，mặc địnhcho24000
        :param num_channels: ，mặc địnhcho
        :param bits_per_sample: mỗi，mặc địnhcho16
        :return: WAV định dạngdữ liệu
        """
        byte_data = np.frombuffer(pcm_data, dtype=np.int16)  # 16PCM
        wav_io = io.BytesIO()

        with wave.open(wav_io, "wb") as wav_file:
            wav_file.setnchannels(num_channels)
            wav_file.setsampwidth(bits_per_sample // 8)
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(byte_data.tobytes())

        return wav_io.getvalue()

    async def text_to_speak(self, text, output_file):
        if self.protocol == "websocket":
            return await self.text_streaming(text, output_file)
        else:
            raise ValueError("Unsupported protocol. Please use 'websocket' or 'http'.")

    async def text_streaming(self, text, output_file):
        try:
            # làm chosử dụng websockets kết nốiđến WebSocket máy chủ
            async with websockets.connect(self.url) as ws:
                # gửibắt đầuyêu cầu
                start_request = {
                    "task": "tts",
                    "signal": "start"
                }
                await ws.send(json.dumps(start_request))

                # nhậnbắt đầuphản hồivà session_id
                start_response = await ws.recv()
                start_response = json.loads(start_response)  # phân tích JSON phản hồi
                if start_response.get("status") != 0:
                    raise Exception(f"kết nối thất bại: {start_response.get('signal')}")

                session_id = start_response.get("session")

                # gửivăn bảndữ liệu
                data_request = {
                    "text": text,
                    "spk_id": self.spk_id,
                }
                await ws.send(json.dumps(data_request))

                audio_chunks = b""
                timeout_seconds = 60  # đặtquá thời gian
                try:
                    while True:
                        response = await asyncio.wait_for(ws.recv(), timeout=timeout_seconds)
                        response = json.loads(response)  # phân tích JSON phản hồi
                        status = response.get("status")

                        if status == 2:  # saumộtdữ liệu
                            break
                        else:
                            # nốidữ liệu âm thanh（base64 mã hóa PCM dữ liệu）
                            audio_chunks += base64.b64decode(response.get("audio"))
                except asyncio.TimeoutError:
                    raise Exception(f"WebSocket quá thời gian：chờdữ liệu âm thanhvượt quá {timeout_seconds} ")

                # sẽnốisau PCM dữ liệuchuyển đổicho WAV định dạng
                wav_data = await self.pcm_to_wav(audio_chunks)

                # kết thúcyêu cầu
                end_request = {
                    "task": "tts",
                    "signal": "end",
                    "session": session_id  # phiên ID vớibắt đầuyêu cầutrong
                }
                await ws.send(json.dumps(end_request))

                # nhậnkết thúcphản hồidịch vụrangoại lệ
                await ws.recv()

                # theocấu hìnhcólưutệp
                if not self.delete_audio_file and self.save_path:
                    with open(self.save_path, "wb") as f:
                        f.write(wav_data)
                    logger.bind(tag=TAG).info(f"tệp âm thanhđãlưuđến: {self.save_path}")
                
                # trả vềhoặclưudữ liệu âm thanh
                if output_file:
                    with open(output_file, "wb") as file_to_save:
                        file_to_save.write(wav_data)
                else:
                    return wav_data

        except Exception as e:
            raise Exception(f"Error during TTS WebSocket request: {e} while processing text: {text}")