import json
import time
import uuid
import hmac
import base64
import hashlib
import asyncio
import requests
import websockets
import opuslib_next
from urllib import parse
from datetime import datetime
from config.logger import setup_logging
from core.providers.asr.base import ASRProviderBase
from core.providers.asr.dto.dto import InterfaceType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.connection import ConnectionHandler

TAG = __name__
logger = setup_logging()


class AccessToken:
    @staticmethod
    def _encode_text(text):
        encoded_text = parse.quote_plus(text)
        return encoded_text.replace("+", "%20").replace("*", "%2A").replace("%7E", "~")

    @staticmethod
    def _encode_dict(dic):
        keys = dic.keys()
        dic_sorted = [(key, dic[key]) for key in sorted(keys)]
        encoded_text = parse.urlencode(dic_sorted)
        return encoded_text.replace("+", "%20").replace("*", "%2A").replace("%7E", "~")

    @staticmethod
    def create_token(access_key_id, access_key_secret):
        parameters = {
            "AccessKeyId": access_key_id,
            "Action": "CreateToken",
            "Format": "JSON",
            "RegionId": "cn-shanghai",
            "SignatureMethod": "HMAC-SHA1",
            "SignatureNonce": str(uuid.uuid1()),
            "SignatureVersion": "1.0",
            "Timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "Version": "2019-02-28",
        }
        query_string = AccessToken._encode_dict(parameters)
        string_to_sign = (
            "GET" + "&" + AccessToken._encode_text("/") + "&" + AccessToken._encode_text(query_string)
        )
        secreted_string = hmac.new(
            bytes(access_key_secret + "&", encoding="utf-8"),
            bytes(string_to_sign, encoding="utf-8"),
            hashlib.sha1,
        ).digest()
        signature = base64.b64encode(secreted_string)
        signature = AccessToken._encode_text(signature)
        full_url = "http://nls-meta.cn-shanghai.aliyuncs.com/?Signature=%s&%s" % (signature, query_string)
        response = requests.get(full_url)
        if response.ok:
            root_obj = response.json()
            if "Token" in root_obj:
                return root_obj["Token"]["Id"], root_obj["Token"]["ExpireTime"]
        return None, None


class ASRProvider(ASRProviderBase):
    def __init__(self, config, delete_audio_file):
        super().__init__()
        self.interface_type = InterfaceType.STREAM
        self.config = config
        self.text = ""
        self.decoder = opuslib_next.Decoder(16000, 1)
        self.asr_ws = None
        self.forward_task = None
        self.is_processing = False
        self.server_ready = False  # máy chủtrạng thái

        # cấu hình
        self.access_key_id = config.get("access_key_id")
        self.access_key_secret = config.get("access_key_secret")
        self.appkey = config.get("appkey")
        self.token = config.get("token")
        self.host = config.get("host", "nls-gateway-cn-shanghai.aliyuncs.com")
        # nhưcấu hìnhcủlàbên trongđịa chỉ（-internal.aliyuncs.com），làm chosử dụngwsgiao thức，mặc địnhlàwssgiao thức
        if "-internal." in self.host:
            self.ws_url = f"ws://{self.host}/ws/v1"
        else:
            # mặc địnhlàm chosử dụngwssgiao thức
            self.ws_url = f"wss://{self.host}/ws/v1"

        self.max_sentence_silence = config.get("max_sentence_silence")
        self.output_dir = config.get("output_dir", "./audio_output")
        self.delete_audio_file = delete_audio_file
        self.expire_time = None

        self.task_id = uuid.uuid4().hex

        # Token
        if self.access_key_id and self.access_key_secret:
            self._refresh_token()
        elif not self.token:
            raise ValueError("access_key_id+access_key_secrethoặctoken")

    def _refresh_token(self):
        """làm mớiToken"""
        self.token, expire_time_str = AccessToken.create_token(self.access_key_id, self.access_key_secret)
        if not self.token:
            raise ValueError("lấyhiệu quảcủToken")
        
        try:
            expire_str = str(expire_time_str).strip()
            if expire_str.isdigit():
                expire_time = datetime.fromtimestamp(int(expire_str))
            else:
                expire_time = datetime.strptime(expire_str, "%Y-%m-%dT%H:%M:%SZ")
            self.expire_time = expire_time.timestamp() - 60
        except:
            self.expire_time = None

    def _is_token_expired(self):
        """kiểm traTokenlàqua"""
        return self.expire_time and time.time() > self.expire_time

    async def open_audio_channels(self, conn):
        await super().open_audio_channels(conn)

    async def receive_audio(self, conn, audio, audio_have_voice):
        # sử dụngphương phápxử lý
        await super().receive_audio(conn, audio, audio_have_voice)

        # chỉtại/trongcóvàcókết nốikhi/thờikết nối（tại/trongdừngcủ）
        if audio_have_voice and not self.is_processing and not self.asr_ws:
            try:
                await self._start_recognition(conn)
            except Exception as e:
                logger.bind(tag=TAG).error(f"bắt đầunhận dạngthất bại: {str(e)}")
                await self._cleanup()
                return

        if self.asr_ws and self.is_processing and self.server_ready:
            try:
                pcm_frame = self.decoder.decode(audio, 960)
                await self.asr_ws.send(pcm_frame)
            except Exception as e:
                logger.bind(tag=TAG).warning(f"gửiâm thanhthất bại: {str(e)}")
                await self._cleanup()

    async def _start_recognition(self, conn: "ConnectionHandler"):
        """bắt đầunhận dạngphiên"""
        if self._is_token_expired():
            self._refresh_token()
        
        # kết nối
        headers = {"X-NLS-Token": self.token}
        self.asr_ws = await websockets.connect(
            self.ws_url,
            additional_headers=headers,
            max_size=1000000000,
            ping_interval=None,
            ping_timeout=None,
            close_timeout=5,
        )

        self.task_id = uuid.uuid4().hex

        logger.bind(tag=TAG).debug(f"WebSocketkết nốithành công, task_id: {self.task_id}")

        self.is_processing = True
        self.server_ready = False  # đặt lạimáy chủtrạng thái
        self.forward_task = asyncio.create_task(self._forward_results(conn))

        # gửibắt đầuyêu cầu
        start_request = {
            "header": {
                "namespace": "SpeechTranscriber",
                "name": "StartTranscription",
                "message_id": uuid.uuid4().hex,
                "task_id": self.task_id,
                "appkey": self.appkey
            },
            "payload": {
                "format": "pcm",
                "sample_rate": 16000,
                "enable_intermediate_result": True,
                "enable_punctuation_prediction": True,
                "enable_inverse_text_normalization": True,
                "max_sentence_silence": self.max_sentence_silence,
                "enable_voice_detection": False,
            }
        }
        await self.asr_ws.send(json.dumps(start_request, ensure_ascii=False))
        logger.bind(tag=TAG).debug("đãgửibắt đầuyêu cầu，chờmáy chủ...")

    async def _forward_results(self, conn: "ConnectionHandler"):
        """nhận dạngkết quả"""
        try:
            while not conn.stop_event.is_set():
                # lấyhiện tạikết nốicủdữ liệu âm thanh
                audio_data = conn.asr_audio
                try:
                    response = await self.asr_ws.recv()
                    result = json.loads(response)

                    header = result.get("header", {})
                    payload = result.get("payload", {})
                    message_name = header.get("name", "")
                    status = header.get("status", 0)

                    if status != 20000000:
                        if status == 40010004:
                            logger.bind(tag=TAG).warning(f"tại/trongdịch vụphản hồihoàn thànhsauđóng，trạng thái: {status}")
                            break
                        if status in [40000004, 40010003]:  # kết nốiquá thời gianhoặcmáy kháchngắt kết nối
                            logger.bind(tag=TAG).warning(f"kết nối，trạng thái: {status}")
                            break
                        elif status in [40270002, 40270003]:  # âm thanh
                            logger.bind(tag=TAG).warning(f"âm thanhxử lý，trạng thái: {status}")
                            continue
                        else:
                            logger.bind(tag=TAG).error(f"nhận dạngsai，trạng thái: {status}, tin nhắn: {header.get('status_text', '')}")
                            continue

                    # đếnTranscriptionStartedmáy chủnhậndữ liệu âm thanh
                    if message_name == "TranscriptionStarted":
                        self.server_ready = True
                        logger.bind(tag=TAG).debug("máy chủđã，bắt đầugửibộ nhớ đệmâm thanh...")

                        # gửibộ nhớ đệmâm thanh
                        if conn.asr_audio:
                            for cached_audio in conn.asr_audio[-10:]:
                                try:
                                    pcm_frame = self.decoder.decode(cached_audio, 960)
                                    await self.asr_ws.send(pcm_frame)
                                except Exception as e:
                                    logger.bind(tag=TAG).warning(f"gửibộ nhớ đệmâm thanhthất bại: {e}")
                                    break
                        continue
                    elif message_name == "SentenceEnd":
                        # câukết thúc（mỗicâusẽ）
                        text = payload.get("result", "")
                        if text:
                            logger.bind(tag=TAG).info(f"nhận dạngđếnvăn bản: {text}")

                            # chế độtích lũynhận dạngkết quả
                            if conn.client_listen_mode == "manual":
                                if self.text:
                                    self.text += text
                                else:
                                    self.text = text

                                # chế độ，chỉcótại/trongđếnstopsauxử lý（chỉxử lýlần）
                                if conn.client_voice_stop:
                                    logger.bind(tag=TAG).debug("đếnnhận dạngkết quả，xử lý")
                                    await self.handle_voice_stop(conn, audio_data)
                                    break
                            else:
                                # chế độ
                                self.text = text
                                await self.handle_voice_stop(conn, audio_data)
                                break

                except asyncio.TimeoutError:
                    logger.bind(tag=TAG).error("nhậnkết quảquá thời gian")
                    break
                except websockets.ConnectionClosed:
                    logger.bind(tag=TAG).info("ASRdịch vụkết nốiđãđóng")
                    self.is_processing = False
                    break
                except Exception as e:
                    logger.bind(tag=TAG).error(f"xử lýkết quảthất bại: {str(e)}")
                    break

        except Exception as e:
            logger.bind(tag=TAG).error(f"kết quảthất bại: {str(e)}")
        finally:
            # dọn dẹpkết nốicủâm thanhbộ nhớ đệm
            await self._cleanup()
            conn.reset_audio_states()

    async def _send_stop_request(self):
        """gửidừngnhận dạngyêu cầu（khôngđóngkết nối）"""
        if self.asr_ws:
            try:
                # dừngâm thanhgửi
                self.is_processing = False

                stop_msg = {
                    "header": {
                        "namespace": "SpeechTranscriber",
                        "name": "StopTranscription",
                        "message_id": uuid.uuid4().hex,
                        "task_id": self.task_id,
                        "appkey": self.appkey
                    }
                }
                logger.bind(tag=TAG).debug("dừngnhận dạngyêu cầuđãgửi")
                await self.asr_ws.send(json.dumps(stop_msg, ensure_ascii=False))
            except Exception as e:
                logger.bind(tag=TAG).error(f"gửidừngnhận dạngyêu cầuthất bại: {e}")

    async def _cleanup(self):
        """dọn dẹptài nguyên（đóngkết nối）"""
        logger.bind(tag=TAG).debug(f"bắt đầuASRphiêndọn dẹp | hiện tạitrạng thái: processing={self.is_processing}, server_ready={self.server_ready}")

        # trạng tháiđặt lại
        self.is_processing = False
        self.server_ready = False
        logger.bind(tag=TAG).debug("ASRtrạng tháiđãđặt lại")

        # đóngkết nối
        if self.asr_ws:
            try:
                logger.bind(tag=TAG).debug("tại/trongđóngWebSocketkết nối")
                await asyncio.wait_for(self.asr_ws.close(), timeout=2.0)
                logger.bind(tag=TAG).debug("WebSocketkết nốiđãđóng")
            except Exception as e:
                logger.bind(tag=TAG).error(f"đóngWebSocketkết nốithất bại: {e}")
            finally:
                self.asr_ws = None

        # dọn dẹpnhiệm vụsử dụng
        self.forward_task = None

        logger.bind(tag=TAG).debug("ASRphiêndọn dẹphoàn thành")

    async def speech_to_text(self, opus_data, session_id, audio_format, artifacts=None):
        """lấynhận dạngkết quả"""
        result = self.text
        self.text = ""
        return result, None

    async def close(self):
        """đóngtài nguyên"""
        await self._cleanup()
        if hasattr(self, 'decoder') and self.decoder is not None:
            try:
                del self.decoder
                self.decoder = None
                logger.bind(tag=TAG).debug("Aliyun decoder resources released")
            except Exception as e:
                logger.bind(tag=TAG).debug(f"giải phóngAliyun decodertài nguyênkhi/thờira: {e}")
