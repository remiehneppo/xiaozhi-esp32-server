"""
Opusmã hóacông cụ
sẽPCMdữ liệu âm thanhmã hóachoOpusđịnh dạng
"""

import logging
import traceback
import numpy as np
from opuslib_next import Encoder
from opuslib_next import constants
from typing import Optional, Callable, Any

class OpusEncoderUtils:
    """PCMđếnOpusmã hóa"""

    def __init__(self, sample_rate: int, channels: int, frame_size_ms: int):
        """
        khởi tạoOpusmã hóa

        Args:
            sample_rate: tần số lấy mẫu (Hz)
            channels: số kênh (1=, 2=)
            frame_size_ms: khung ()
        """
        self.sample_rate = sample_rate
        self.channels = channels
        self.frame_size_ms = frame_size_ms
        # tính toánkhung = tần số lấy mẫu * khung() / 1000
        self.frame_size = (sample_rate * frame_size_ms) // 1000
        # khung = khung * số kênh
        self.total_frame_size = self.frame_size * channels

        # vàphức tạpđặt
        self.bitrate = 24000  # bps
        self.complexity = 10  # 

        # khởi tạocho
        self.buffer = np.array([], dtype=np.int16)

        try:
            # tạoOpusmã hóa
            self.encoder = Encoder(
                sample_rate, channels, constants.APPLICATION_AUDIO  # âm thanhchế độ
            )
            self.encoder.bitrate = self.bitrate
            self.encoder.complexity = self.complexity
            self.encoder.signal = constants.SIGNAL_VOICE  # giọng nói
        except Exception as e:
            logging.error(f"khởi tạoOpusmã hóathất bại: {e}")
            raise RuntimeError("khởi tạothất bại") from e

    def reset_state(self):
        """đặt lạimã hóatrạng thái"""
        self.encoder.reset_state()
        self.buffer = np.array([], dtype=np.int16)

    def encode_pcm_to_opus_stream(self, pcm_data: bytes, end_of_stream: bool, callback: Callable[[Any], Any]):
        """
        sẽPCMdữ liệumã hóachoOpusđịnh dạng，bằngluồngphương thứctiến hànhxử lý

        Args:
            pcm_data: PCMdữ liệu
            end_of_stream: cóchokết thúc,
            callback: opusxử lýphương pháp

        Returns:
            Opusdữ liệu
        """
        # sẽdữ liệuchuyển đổichoshort
        new_samples = self._convert_bytes_to_shorts(pcm_data)

        # kiểm traPCMdữ liệu
        self._validate_pcm_data(new_samples)

        # sẽdữ liệuđến
        self.buffer = np.append(self.buffer, new_samples)

        offset = 0

        # xử lýcóhoàn chỉnhkhung
        while offset <= len(self.buffer) - self.total_frame_size:
            frame = self.buffer[offset : offset + self.total_frame_size]
            output = self._encode(frame)
            if output:
                callback(output)
            offset += self.total_frame_size

        # giữ lạixử lý
        self.buffer = self.buffer[offset:]

        # kết thúcthờixử lýcòn lạidữ liệu
        if end_of_stream and len(self.buffer) > 0:
            # tạosaukhungvàsử dụng0
            last_frame = np.zeros(self.total_frame_size, dtype=np.int16)
            last_frame[: len(self.buffer)] = self.buffer

            output = self._encode(last_frame)
            if output:
                callback(output)
            self.buffer = np.array([], dtype=np.int16)

    def _encode(self, frame: np.ndarray) -> Optional[bytes]:
        """mã hóakhungdữ liệu âm thanh"""
        try:
            # mã hóađãgiải phóng，bỏ quamã hóa
            if not hasattr(self, 'encoder') or self.encoder is None:
                return None
            # sẽnumpychuyển đổichobytes
            frame_bytes = frame.tobytes()
            # opuslibphảiđầu vàochannels*2
            encoded = self.encoder.encode(frame_bytes, self.frame_size)
            return encoded
        except Exception as e:
            logging.error(f"Opusmã hóathất bại: {e}")
            traceback.print_exc()
            return None

    def _convert_bytes_to_shorts(self, bytes_data: bytes) -> np.ndarray:
        """sẽchuyển đổichoshort (16PCM)"""
        # đầu vào16PCM
        return np.frombuffer(bytes_data, dtype=np.int16)

    def _validate_pcm_data(self, pcm_shorts: np.ndarray) -> None:
        """xác thựcPCMdữ liệucóhiệu quả"""
        # 16PCMdữ liệu -32768 đến 32767
        if np.any((pcm_shorts < -32768) | (pcm_shorts > 32767)):
            invalid_samples = pcm_shorts[(pcm_shorts < -32768) | (pcm_shorts > 32767)]
            logging.warning(f"không hợp lệPCM: {invalid_samples[:5]}...")
            # tạiáp dụngtrongcó thểmàkhôngrangoại lệ
            # np.clip(pcm_shorts, -32768, 32767, out=pcm_shorts)

    def close(self):
        """đóngmã hóavàgiải phóngtài nguyên"""
        if hasattr(self, 'encoder') and self.encoder:
            try:
                del self.encoder
                self.encoder = None
            except Exception as e:
                logging.error(f"Error releasing Opus encoder: {e}")