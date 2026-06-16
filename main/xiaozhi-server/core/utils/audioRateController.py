import time
import asyncio
from collections import deque
from config.logger import setup_logging

TAG = __name__
logger = setup_logging()


class AudioRateController:
    """
    âm thanh - theo60mskhungkhi/thờiâm thanhgửi
    vàcủkhi/thờitích lũy
    """

    def __init__(self, frame_duration=60):
        """
        Args:
            frame_duration: âm thanhkhungkhi/thời（），mặc định60ms
        """
        self.frame_duration = frame_duration
        self.queue = deque()
        self.play_position = 0  # vị trí（）
        self.start_timestamp = None  # bắt đầukhi/thời（chỉ，khôngsửa đổi）
        self.pending_send_task = None
        self.logger = logger
        self.queue_empty_event = asyncio.Event()  # hàng đợi
        self.queue_empty_event.set()  # chotrạng thái
        self.queue_has_data_event = asyncio.Event()  # hàng đợidữ liệu
        self._last_queue_empty_time = 0  # trênlầnhàng đợicủkhi/thời（）

    def reset(self):
        """đặt lạitrạng thái"""
        if self.pending_send_task and not self.pending_send_task.done():
            self.pending_send_task.cancel()
            # hủynhiệm vụsau，nhiệm vụsẽtại/tronglầnkhi/thờidọn dẹp，chờ

        self.queue.clear()
        self.play_position = 0
        self.start_timestamp = None  # âm thanhđặt
        self._last_queue_empty_time = 0  # đặt lạikhi/thời
        # xử lý
        self.queue_empty_event.set()
        self.queue_has_data_event.clear()

    def add_audio(self, opus_packet):
        """thêmâm thanhđếnhàng đợi"""
        # nhưhàng đợicho，cầnkhi/thờibằngkhi/thời
        # nàycông cụsử dụngchờ，vàocủâm thanhkhôngsẽ
        # như（<1khung），nóilàcủluồng，khôngcầnđặt lại
        if len(self.queue) == 0 and self.play_position > 0:
            elapsed_since_empty = (time.monotonic() - self._last_queue_empty_time) * 1000
            # chỉcóqua1khungkhi/thời，cholàcủ"tạm dừngtiếp tục"
            if elapsed_since_empty >= self.frame_duration:
                self.start_timestamp = time.monotonic() - (self.play_position / 1000)
                self.logger.bind(tag=TAG).debug(
                    f"hàng đợitừtiếp tục，đặt lạikhi/thời，hiện tạivị trí: {self.play_position}ms，: {elapsed_since_empty:.0f}ms"
                )

        self.queue.append(("audio", opus_packet))
        # xử lý
        self.queue_empty_event.clear()
        self.queue_has_data_event.set()

    def add_message(self, message_callback):
        """
        thêmtin nhắnđếnhàng đợi（gửi，khôngsử dụngkhi/thời）

        Args:
            message_callback: tin nhắngửihàm async def()
        """
        if len(self.queue) == 0 and self.play_position > 0:
            elapsed_since_empty = (time.monotonic() - self._last_queue_empty_time) * 1000
            if elapsed_since_empty >= self.frame_duration:
                self.start_timestamp = time.monotonic() - (self.play_position / 1000)
                self.logger.bind(tag=TAG).debug(
                    f"hàng đợitừtiếp tục，đặt lạikhi/thời，hiện tạivị trí: {self.play_position}ms，: {elapsed_since_empty:.0f}ms"
                )

        self.queue.append(("message", message_callback))
        # xử lý
        self.queue_empty_event.clear()
        self.queue_has_data_event.set()

    def _get_elapsed_ms(self):
        """lấyđãquacủkhi/thời（）"""
        if self.start_timestamp is None:
            return 0
        return (time.monotonic() - self.start_timestamp) * 1000

    async def check_queue(self, send_audio_callback):
        """
        kiểm trahàng đợivàtheokhi/thờigửiâm thanh/tin nhắn

        Args:
            send_audio_callback: gửiâm thanhcủhàm async def(opus_packet)
        """
        while self.queue:
            item = self.queue[0]
            item_type = item[0]

            if item_type == "message":
                # tin nhắn：gửi，khôngsử dụngkhi/thời
                _, message_callback = item
                self.queue.popleft()
                try:
                    await message_callback()
                except Exception as e:
                    self.logger.bind(tag=TAG).error(f"gửitin nhắnthất bại: {e}")
                    raise

            elif item_type == "audio":
                if self.start_timestamp is None:
                    self.start_timestamp = time.monotonic()

                _, opus_packet = item

                # chờđếnkhi/thờiđến
                while True:
                    # tính toánkhi/thời
                    elapsed_ms = self._get_elapsed_ms()
                    output_ms = self.play_position

                    if elapsed_ms < output_ms:
                        # cũngkhôngđếngửikhi/thời，tính toánchờkhi/thời
                        wait_ms = output_ms - elapsed_ms

                        # chờsautiếp tụckiểm tra（bịtrong）
                        try:
                            await asyncio.sleep(wait_ms / 1000)
                        except asyncio.CancelledError:
                            self.logger.bind(tag=TAG).debug("âm thanhgửinhiệm vụbịhủy")
                            raise
                        # chờkết thúcsaukiểm trakhi/thời（đến while True）
                    else:
                        # khi/thờiđãđến，rachờ
                        break

                # khi/thờiđãđến，từhàng đợiloại bỏvàgửi
                self.queue.popleft()
                self.play_position += self.frame_duration
                try:
                    await send_audio_callback(opus_packet)
                except Exception as e:
                    self.logger.bind(tag=TAG).error(f"gửiâm thanhthất bại: {e}")
                    raise

        # hàng đợixử lýsauxóa
        self.queue_empty_event.set()
        self.queue_has_data_event.clear()
        self._last_queue_empty_time = time.monotonic()  # ghi lạihàng đợikhi/thời

    def start_sending(self, send_audio_callback):
        """
        khởi độnggửinhiệm vụ

        Args:
            send_audio_callback: gửiâm thanhcủhàm

        Returns:
            asyncio.Task: gửinhiệm vụ
        """

        async def _send_loop():
            try:
                while True:
                    # chờhàng đợidữ liệu，khôngchờsử dụngCPU
                    await self.queue_has_data_event.wait()

                    await self.check_queue(send_audio_callback)
            except asyncio.CancelledError:
                self.logger.bind(tag=TAG).debug("âm thanhgửiđãdừng")
            except Exception as e:
                self.logger.bind(tag=TAG).error(f"âm thanhgửingoại lệ: {e}")

        self.pending_send_task = asyncio.create_task(_send_loop())
        return self.pending_send_task

    def stop_sending(self):
        """dừnggửinhiệm vụ"""
        if self.pending_send_task and not self.pending_send_task.done():
            self.pending_send_task.cancel()
            self.logger.bind(tag=TAG).debug("đãhủyâm thanhgửinhiệm vụ")
