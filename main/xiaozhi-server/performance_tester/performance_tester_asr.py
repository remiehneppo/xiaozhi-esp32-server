import asyncio
import logging
import os
import time
import concurrent.futures
from typing import Dict, Optional
import aiohttp
from tabulate import tabulate
from core.utils.asr import create_instance as create_stt_instance

# đặttoàn cụcnhật kýchoWARNING，INFOnhật ký
logging.basicConfig(level=logging.WARNING)

description = "giọng nóinhận dạngmô hìnhcó thểkiểm tra"

class ASRPerformanceTester:
    def __init__(self):
        self.config = self._load_config_from_data_dir()
        self.test_wav_list = self._load_test_wav_files()
        self.results = {"stt": {}}
        
        # gỡ lỗinhật ký
        print(f"[DEBUG] tảicủASRcấu hình: {self.config.get('ASR', {})}")
        print(f"[DEBUG] âm thanhtệp: {len(self.test_wav_list)}")

    def _load_config_from_data_dir(self) -> Dict:
        """từ data thư mụctảicó .config.yaml tệpcủcấu hình"""
        config = {"ASR": {}}
        data_dir = os.path.join(os.getcwd(), "data")
        print(f"[DEBUG] cấu hìnhtệpthư mục: {data_dir}")

        for root, _, files in os.walk(data_dir):
            for file in files:
                if file.endswith(".config.yaml"):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            import yaml
                            file_config = yaml.safe_load(f)
                            # củ ASR/asr cấu hình
                            asr_config = file_config.get("ASR") or file_config.get("asr")
                            if asr_config:
                                config["ASR"].update(asr_config)
                                print(f"[DEBUG] từ {file_path} tải ASR cấu hìnhthành công")
                    except Exception as e:
                        print(f" tảicấu hìnhtệp {file_path} thất bại: {str(e)}")
        return config

    def _load_test_wav_files(self) -> list:
        """tảikiểm trasử dụngcủâm thanhtệp（thêmđường dẫngỡ lỗi）"""
        wav_root = os.path.join(os.getcwd(), "config", "assets")
        print(f"[DEBUG] âm thanhtệpthư mục: {wav_root}")
        test_wav_list = []
        
        if os.path.exists(wav_root):
            file_list = os.listdir(wav_root)
            print(f"[DEBUG] đếnâm thanhtệp: {file_list}")
            for file_name in file_list:
                file_path = os.path.join(wav_root, file_name)
                if os.path.getsize(file_path) > 300 * 1024:  # 300KB
                    with open(file_path, "rb") as f:
                        test_wav_list.append(f.read())
        else:
            print(f" thư mụckhôngtại/trong: {wav_root}")
        return test_wav_list

    async def _test_single_audio(self, stt_name: str, stt, audio_data: bytes) -> Optional[float]:
        """kiểm traâm thanhtệpcủcó thể"""
        try:
            start_time = time.time()
            text, _ = await stt.speech_to_text_wrapper([audio_data], "1", stt.audio_format)
            if text is None:
                return None
            
            duration = time.time() - start_time
            
            # 0.000scủngoại lệkhi/thời
            if abs(duration) < 0.001:  # tại1chongoại lệ
                print(f"{stt_name} đếnngoại lệkhi/thời: {duration:.6f}s (chosai)")
                return None
                
            return duration
        except Exception as e:
            error_msg = str(e).lower()
            if "502" in error_msg or "bad gateway" in error_msg:
                print(f"{stt_name} đến502sai")
                return None
            return None

    async def _test_stt_with_timeout(self, stt_name: str, config: Dict) -> Dict:
        """kiểm traSTTcó thể，quá thời gian"""
        try:
            # Kiểm tra tính hợp lệ của cấu hình
            token_fields = ["access_token", "api_key", "token"]
            if any(
                field in config
                and str(config[field]).lower() in ["củ", "placeholder", "none", "null", ""]
                for field in token_fields
            ):
                print(f"  STT {stt_name} cấu hìnhhiệu quảaccess_token/api_key，đãqua")
                return {
                    "name": stt_name,
                    "type": "stt",
                    "errors": 1,
                    "error_type": "Lỗi cấu hình"
                }

            module_type = config.get("type", stt_name)
            stt = create_stt_instance(module_type, config, delete_audio_file=True)
            stt.audio_format = "pcm"

            print(f" kiểm tra STT: {stt_name}")

            # sử dụngluồngvàquá thời gian
            loop = asyncio.get_event_loop()
            
            # kiểm tramộtâm thanhtệpchokiểm tra
            try:
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(
                        lambda: asyncio.run(self._test_single_audio(stt_name, stt, self.test_wav_list[0]))
                    )
                    first_result = await asyncio.wait_for(
                        asyncio.wrap_future(future), timeout=10.0
                    )
                    
                    if first_result is None:
                        print(f" {stt_name} kết nốithất bại")
                        return {
                            "name": stt_name,
                            "type": "stt",
                            "errors": 1,
                            "error_type": "Lỗi mạng"
                        }
            except asyncio.TimeoutError:
                print(f" {stt_name} kết nốiquá thời gian（10），qua")
                return {
                    "name": stt_name,
                    "type": "stt",
                    "errors": 1,
                    "error_type": "Hết thời gian kết nối"
                }
            except Exception as e:
                error_msg = str(e).lower()
                if "502" in error_msg or "bad gateway" in error_msg:
                    print(f" {stt_name} đến502sai，qua")
                    return {
                        "name": stt_name,
                        "type": "stt",
                        "errors": 1,
                        "error_type": "Lỗi mạng 502"
                    }
                print(f" {stt_name} kết nốingoại lệ: {str(e)}")
                return {
                    "name": stt_name,
                    "type": "stt",
                    "errors": 1,
                    "error_type": "Lỗi mạng"
                }

                       # kiểm tra，quá thời gian
            total_time = 0
            valid_tests = 0
            test_count = len(self.test_wav_list)
            
            for i, audio_data in enumerate(self.test_wav_list, 1):
                try:
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        future = executor.submit(
                            lambda: asyncio.run(self._test_single_audio(stt_name, stt, audio_data))
                        )
                        duration = await asyncio.wait_for(
                            asyncio.wrap_future(future), timeout=10.0
                        )
                        
                        if duration is not None and duration > 0.001:  
                            total_time += duration
                            valid_tests += 1
                            print(f" {stt_name} [{i}/{test_count}] khi/thời: {duration:.2f}s")
                        else:
                            print(f" {stt_name} [{i}/{test_count}] kiểm trathất bại(0.000sngoại lệ)")
                            
                except asyncio.TimeoutError:
                    print(f" {stt_name} [{i}/{test_count}] quá thời gian（10），qua")
                    continue
                except Exception as e:
                    error_msg = str(e).lower()
                    if "502" in error_msg or "bad gateway" in error_msg:
                        print(f" {stt_name} [{i}/{test_count}] 502sai，qua")
                        return {
                            "name": stt_name,
                            "type": "stt",
                            "errors": 1,
                            "error_type": "Lỗi mạng 502"
                        }
                    print(f" {stt_name} [{i}/{test_count}] ngoại lệ: {str(e)}")
                    continue
            # kiểm trahiệu quảkiểm tra
            if valid_tests < test_count * 0.3:  # 30%thành công
                print(f" {stt_name} thành côngkiểm traqua({valid_tests}/{test_count})，có thểkhông")
                return {
                    "name": stt_name,
                    "type": "stt",
                    "errors": 1,
                    "error_type": "Lỗi mạng"
                }

            if valid_tests == 0:
                return {
                    "name": stt_name,
                    "type": "stt",
                    "errors": 1,
                    "error_type": "Lỗi mạng"
                }

            avg_time = total_time / valid_tests
            return {
                "name": stt_name,
                "type": "stt",
                "avg_time": avg_time,
                "success_rate": f"{valid_tests}/{test_count}",
                "errors": 0,
            }

        except Exception as e:
            error_msg = str(e).lower()
            if "502" in error_msg or "bad gateway" in error_msg:
                error_type = "502sai"
            elif "timeout" in error_msg:
                error_type = "quá thời giankết nối"
            else:
                error_type = "sai"
            print(f"⚠️ {stt_name} kiểm trathất bại: {str(e)}")
            return {
                "name": stt_name,
                "type": "stt",
                "errors": 1,
                "error_type": error_type
            }

    def _print_results(self):
        """kiểm trakết quả，theophản hồikhi/thờisắp xếp"""
        print("\n" + "=" * 50)
        print("ASR có thểkiểm trakết quả")
        print("=" * 50)

        if not self.results.get("stt"):
            print("cókhả dụngcủkiểm trakết quả")
            return

        headers = ["mô hình", "khi/thời(s)", "thành công", "trạng thái"]
        table_data = []

        # Thu thập tất cả dữ liệu và phân loại
        valid_results = []
        error_results = []

        for name, data in self.results["stt"].items():
            if data["errors"] == 0:
                # kết quả
                avg_time = f"{data['avg_time']:.3f}"
                success_rate = data.get("success_rate", "N/A")
                status = "✅ Bình thường"
                
                # Lưu giá trị dùng để sắp xếp
                sort_key = data["avg_time"]
                
                valid_results.append({
                    "name": name,
                    "avg_time": avg_time,
                    "success_rate": success_rate,
                    "status": status,
                    "sort_key": sort_key,
                })
            else:
                # Kết quả lỗi
                avg_time = "-"
                success_rate = "0/N"
                
                # Lấy loại lỗi cụ thể
                error_type = data.get("error_type", "Lỗi mạng")
                status = f"❌ {error_type}"
                
                error_results.append([name, avg_time, success_rate, status])

        # theophản hồikhi/thờisắp xếp（từđến）
        valid_results.sort(key=lambda x: x["sort_key"])

        # Chuyển đổi kết quả hợp lệ sau khi sắp xếp thành dữ liệu bảng
        for result in valid_results:
            table_data.append([
                result["name"],
                result["avg_time"],
                result["success_rate"],
                result["status"],
            ])

        # Thêm kết quả lỗi vào cuối dữ liệu bảng
        table_data.extend(error_results)

        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        print("\nkiểm tranói:")
        print("- quá thời gian：âm thanhchờkhi/thờicho10")
        print("- saixử lý：qua502sai、quá thời gianvàngoại lệcủmô hình")
        print("- thành công：thành côngnhận dạngcủâm thanh/kiểm traâm thanh")
        print("- sắp xếp：theokhi/thờitừđếnsắp xếp，saimô hìnhsau")
        print("\nkiểm trahoàn thành！")

    async def run(self):
        """Thực hiện kiểm tra toàn bộ không đồng bộ""" 
        print("bắt đầukhả dụngASR...")
        if not self.config.get("ASR"):
            print("cấu hìnhtrongđến ASR ")
            return

        all_tasks = []
        for stt_name, config in self.config["ASR"].items():
            # Kiểm tra tính hợp lệ của cấu hình
            token_fields = ["access_token", "api_key", "token"]
            if any(
                field in config
                and str(config[field]).lower() in ["củ", "placeholder", "none", "null", ""]
                for field in token_fields
            ):
                print(f"ASR {stt_name} cấu hìnhhiệu quảaccess_token/api_key，đãqua")
                continue
            
            print(f"thêm ASR kiểm tranhiệm vụ: {stt_name}")
            all_tasks.append(self._test_stt_with_timeout(stt_name, config))

        if not all_tasks:
            print("cókhả dụngcủASRtiến hànhkiểm tra。")
            return

        print(f"\nđến {len(all_tasks)} khả dụngASR")
        print("\nbắt đầuvàkiểm tracóASR...")
        all_results = await asyncio.gather(*all_tasks, return_exceptions=True)

        # Xử lý kết quả
        for result in all_results:
            if isinstance(result, dict) and result.get("type") == "stt":
                self.results["stt"][result["name"]] = result

        # In kết quả
        self._print_results()


async def main():
    tester = ASRPerformanceTester()
    await tester.run()


if __name__ == "__main__":
    asyncio.run(main())