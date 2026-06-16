import time
import asyncio
import logging
import statistics
import base64
from typing import Dict
from tabulate import tabulate
from core.utils.vllm import create_instance
from config.settings import load_config

# đặttoàn cụcnhật kýchoWARNING，INFOnhật ký
logging.basicConfig(level=logging.WARNING)

description = "nhận dạngmô hìnhcó thểkiểm tra"


class AsyncVisionPerformanceTester:
    def __init__(self):
        self.config = load_config()

        self.test_images = [
            "../../docs/images/demo1.png",
            "../../docs/images/demo2.png",
        ]
        self.test_questions = [
            "nàytrongcógì？",
            "nàycủbên trong",
        ]

        # tảikiểm tra
        self.results = {"vllm": {}}

    async def _test_vllm(self, vllm_name: str, config: Dict) -> Dict:
        """kiểm tramô hìnhcó thể"""
        try:
            # kiểm traAPIcấu hình
            if "api_key" in config and any(
                x in config["api_key"] for x in ["củ", "placeholder", "sk-xxx"]
            ):
                print(f"⏭️  VLLM {vllm_name} cấu hìnhapi_key，đãqua")
                return {"name": vllm_name, "type": "vllm", "errors": 1}

            # lấy（cũcấu hình）
            module_type = config.get("type", vllm_name)
            vllm = create_instance(module_type, config)

            print(f"🖼️ kiểm tra VLLM: {vllm_name}")

            # tạocókiểm tranhiệm vụ
            test_tasks = []
            for question in self.test_questions:
                for image in self.test_images:
                    test_tasks.append(
                        self._test_single_vision(vllm_name, vllm, question, image)
                    )

            # vàcókiểm tra
            test_results = await asyncio.gather(*test_tasks)

            # xử lý kết quả
            valid_results = [r for r in test_results if r is not None]
            if not valid_results:
                print(f"⚠️  {vllm_name} hiệu quảdữ liệu，có thểcấu hìnhsai")
                return {"name": vllm_name, "type": "vllm", "errors": 1}

            response_times = [r["response_time"] for r in valid_results]

            # lọcngoại lệdữ liệu
            mean = statistics.mean(response_times)
            stdev = statistics.stdev(response_times) if len(response_times) > 1 else 0
            filtered_times = [t for t in response_times if t <= mean + 3 * stdev]

            if len(filtered_times) < len(test_tasks) * 0.5:
                print(f"⚠️  {vllm_name} hiệu quảdữ liệukhông，có thểkhông")
                return {"name": vllm_name, "type": "vllm", "errors": 1}

            return {
                "name": vllm_name,
                "type": "vllm",
                "avg_response": sum(response_times) / len(response_times),
                "std_response": (
                    statistics.stdev(response_times) if len(response_times) > 1 else 0
                ),
                "errors": 0,
            }

        except Exception as e:
            print(f"⚠️ VLLM {vllm_name} kiểm trathất bại: {str(e)}")
            return {"name": vllm_name, "type": "vllm", "errors": 1}

    async def _test_single_vision(
        self, vllm_name: str, vllm, question: str, image: str
    ) -> Dict:
        """kiểm tracủcó thể"""
        try:
            print(f"📝 {vllm_name} bắt đầukiểm tra: {question[:20]}...")
            start_time = time.time()

            # đọcvàchuyển đổichobase64
            with open(image, "rb") as image_file:
                image_data = image_file.read()
                image_base64 = base64.b64encode(image_data).decode("utf-8")

            # lấyphản hồi
            response = vllm.response(question, image_base64)
            response_time = time.time() - start_time
            print(f"✓ {vllm_name} hoàn thànhphản hồi: {response_time:.3f}s")

            return {
                "name": vllm_name,
                "type": "vllm",
                "response_time": response_time,
            }
        except Exception as e:
            print(f"⚠️ {vllm_name} kiểm trathất bại: {str(e)}")
            return None

    def _print_results(self):
        """kiểm trakết quả"""
        vllm_table = []
        for name, data in self.results["vllm"].items():
            if data["errors"] == 0:
                stability = data["std_response"] / data["avg_response"]
                vllm_table.append(
                    [
                        name,
                        f"{data['avg_response']:.3f}",
                        f"{stability:.3f}",
                    ]
                )

        if vllm_table:
            print("\nmô hìnhcó thể:\n")
            print(
                tabulate(
                    vllm_table,
                    headers=["mô hình", "phản hồikhi/thời", ""],
                    tablefmt="github",
                    colalign=("left", "right", "right"),
                    disable_numparse=True,
                )
            )
        else:
            print("\n⚠️ cókhả dụngcủmô hìnhtiến hànhkiểm tra。")

    async def run(self):
        """kiểm tra"""
        print("🔍 bắt đầukhả dụngmô hình...")

        if not self.test_images:
            print(f"\n⚠️  {self.image_root} đường dẫncótệp，tiến hànhkiểm tra")
            return

        # tạocókiểm tranhiệm vụ
        all_tasks = []

        # VLLMkiểm tranhiệm vụ
        if self.config.get("VLLM") is not None:
            for vllm_name, config in self.config.get("VLLM", {}).items():
                if "api_key" in config and any(
                    x in config["api_key"] for x in ["củ", "placeholder", "sk-xxx"]
                ):
                    print(f"⏭️  VLLM {vllm_name} cấu hìnhapi_key，đãqua")
                    continue
                print(f"🖼️ thêmVLLMkiểm tranhiệm vụ: {vllm_name}")
                all_tasks.append(self._test_vllm(vllm_name, config))

        print(f"\n✅ đến {len(all_tasks)} khả dụngmô hình")
        print(f"✅ làm chosử dụng {len(self.test_images)} kiểm tra")
        print(f"✅ làm chosử dụng {len(self.test_questions)} kiểm tra")
        print("\n⏳ bắt đầuvàkiểm tracómô hình...\n")

        # vàcókiểm tranhiệm vụ
        all_results = await asyncio.gather(*all_tasks, return_exceptions=True)

        # xử lý kết quả
        for result in all_results:
            if isinstance(result, dict) and result["errors"] == 0:
                self.results["vllm"][result["name"]] = result

        # kết quả
        print("\n📊 tạokiểm trabáo cáo...")
        self._print_results()


async def main():
    tester = AsyncVisionPerformanceTester()
    await tester.run()


if __name__ == "__main__":
    asyncio.run(main())
