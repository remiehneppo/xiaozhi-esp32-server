"""
Module quản lý GC toàn cục
Chạy thu gom rác định kỳ để tránh việc GC kích hoạt thường xuyên làm ảnh hưởng tới GIL
"""

import gc
import asyncio
import threading
from config.logger import setup_logging

TAG = __name__
logger = setup_logging()


class GlobalGCManager:
    """Trình quản lý thu gom rác toàn cục"""

    def __init__(self, interval_seconds=300):
        """
        Khởi tạo trình quản lý GC

        Args:
            interval_seconds: Khoảng cách chạy GC (giây), mặc định 300 giây (5 phút)
        """
        self.interval_seconds = interval_seconds
        self._task = None
        self._stop_event = asyncio.Event()
        self._lock = threading.Lock()

    async def start(self):
        """Khởi động tác vụ GC định kỳ"""
        if self._task is not None:
            logger.bind(tag=TAG).warning("Trình quản lý GC đã đang chạy")
            return

        logger.bind(tag=TAG).info(f"Khởi động trình quản lý GC toàn cục, khoảng cách {self.interval_seconds} giây")
        self._stop_event.clear()
        self._task = asyncio.create_task(self._gc_loop())

    async def stop(self):
        """Dừng tác vụ GC định kỳ"""
        if self._task is None:
            return

        logger.bind(tag=TAG).info("Đã dừng trình quản lý GC toàn cục")
        self._stop_event.set()

        if self._task and not self._task.done():
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass

        self._task = None

    async def _gc_loop(self):
        """Vòng lặp tác vụ GC"""
        try:
            while not self._stop_event.is_set():
                # Chờ theo khoảng cách đã chỉ định
                try:
                    await asyncio.wait_for(
                        self._stop_event.wait(), timeout=self.interval_seconds
                    )
                    # Nếu stop_event được set thì thoát vòng lặp
                    break
                except asyncio.TimeoutError:
                    # Hết thời gian nghĩa là tới lúc chạy GC
                    pass

                # Thực thi GC
                await self._run_gc()

        except asyncio.CancelledError:
            logger.bind(tag=TAG).info("Vòng lặp GC đã bị hủy")
            raise
        except Exception as e:
            logger.bind(tag=TAG).error(f"Vòng lặp GC gặp lỗi: {e}")
        finally:
            logger.bind(tag=TAG).info("Vòng lặp GC đã thoát")

    async def _run_gc(self):
        """Thực thi thu gom rác"""
        try:
            # Chạy GC trong thread pool để không chặn event loop
            loop = asyncio.get_running_loop()

            def do_gc():
                with self._lock:
                    before = len(gc.get_objects())
                    collected = gc.collect()
                    after = len(gc.get_objects())
                    return before, collected, after

            before, collected, after = await loop.run_in_executor(None, do_gc)
            logger.bind(tag=TAG).debug(
                f"GC toàn cục hoàn tất - đối tượng thu gom: {collected}, "
                f"số lượng đối tượng: {before} -> {after}"
            )
        except Exception as e:
            logger.bind(tag=TAG).error(f"Lỗi khi thực thi GC: {e}")


# Singleton toàn cục
_gc_manager_instance = None


def get_gc_manager(interval_seconds=300):
    """
    Lấy instance trình quản lý GC toàn cục (singleton)

    Args:
        interval_seconds: Khoảng cách chạy GC (giây), mặc định 300 giây (5 phút)

    Returns:
        Instance GlobalGCManager
    """
    global _gc_manager_instance
    if _gc_manager_instance is None:
        _gc_manager_instance = GlobalGCManager(interval_seconds)
    return _gc_manager_instance
