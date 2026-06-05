# Hướng dẫn sử dụng IndexStreamTTS

## Chuẩn bị môi trường
### 1. Sao chép dự án
```bash 
git clone https://github.com/Ksuriuri/index-tts-vllm.git
```
Nhập thư mục đã giải nén
```bash
cd index-tts-vllm
```
Chuyển sang phiên bản đã chỉ định (sử dụng phiên bản lịch sử của VLLM-0.10.2)
```bash
git checkout 224e8d5e5c8f66801845c66b30fa765328fd0be3
```

### 2. Tạo và kích hoạt môi trường conda
```bash 
conda create -n index-tts-vllm python=3.12
conda activate index-tts-vllm
```

### 3. Cài đặt PyTorch yêu cầu phiên bản 2.8.0 (phiên bản mới nhất)
#### Kiểm tra phiên bản card đồ họa được hỗ trợ cao nhất và phiên bản được cài đặt thực tế
```bash
nvidia-smi
nvcc --version
```
#### Phiên bản CUDA cao nhất được driver hỗ trợ
```bash
CUDA Version: 12.8
```
#### Phiên bản trình biên dịch CUDA được cài đặt thực tế
```bash
Cuda compilation tools, release 12.8, V12.8.89
```
#### Sau đó là lệnh cài đặt tương ứng (pytorch mặc định là phiên bản driver 12.8)
```bash
pip install torch torchvision
```
Yêu cầu pytorch phiên bản 2.8.0 (tương ứng với vllm 0.10.2). Để biết hướng dẫn cài đặt cụ thể, vui lòng tham khảo: [trang web chính thức của pytorch](https://pytorch.org/get-started/locally/)

### 4. Cài đặt phụ thuộc
```bash 
pip install -r requirements.txt
```

### 5. Tải trọng lượng mô hình xuống
### 方案一: 下载官方权重文件后转换
Đây là tập tin trọng lượng chính thức. Bạn có thể tải nó xuống bất kỳ đường dẫn cục bộ nào. Nó hỗ trợ trọng lượng của IndexTTS-1.5.
| Ôm Mặt | ModelScope |
|-----------------------------------------------------------------|--------------------------------------------------------------------------------|
| [IndexTTS](https://huggingface.co/IndexTeam/Index-TTS) | [IndexTTS](https://modelscope.cn/models/IndexTeam/Index-TTS) |
| [IndexTTS-1.5](https://huggingface.co/IndexTeam/IndexTTS-1.5) | [IndexTTS-1.5](https://modelscope.cn/models/IndexTeam/IndexTTS-1.5) |

Sau đây lấy phương pháp cài đặt ModelScope làm ví dụ.
#### Xin lưu ý: git cần được cài đặt và khởi tạo để kích hoạt lfs (bạn có thể bỏ qua nếu nó đã được cài đặt)
```bash
sudo apt-get install git-lfs
git lfs install
```
Tạo một thư mục mô hình và kéo mô hình
```bash 
mkdir model_dir
cd model_dir
git clone https://www.modelscope.cn/IndexTeam/IndexTTS-1.5.git
```

#### Chuyển đổi trọng lượng mẫu
```bash 
bash convert_hf_format.sh /path/to/your/model_dir
```
Ví dụ: model IndexTTS-1.5 bạn tải về được lưu trữ trong thư mục model_dir, sau đó thực hiện lệnh sau
```bash
bash convert_hf_format.sh model_dir/IndexTTS-1.5
```
Thao tác này sẽ chuyển đổi các trọng số mô hình chính thức thành một phiên bản tương thích với thư viện máy biến áp và lưu chúng vào thư mục vllm theo đường dẫn trọng lượng mô hình để tạo điều kiện thuận lợi cho việc tải các trọng số mô hình tiếp theo bằng thư viện vllm.

### 6. Thay đổi giao diện để thích ứng với dự án
Dữ liệu được giao diện trả về không phù hợp với dự án và cần được điều chỉnh để có thể trả về trực tiếp dữ liệu âm thanh.
```bash
vi api_server.py
```
``` bash
@app.post("/tts",response={
    200: {"nội dung": {"ứng dụng/octet-stream": {}}},
    500: {"nội dung": {"application/json": {}}}
})
async def tts_api(yêu cầu: Yêu cầu):
    thử:
        dữ liệu = đang chờ request.json()
        văn bản = dữ liệu["văn bản"]
        ký tự = dữ liệu["ký tự"]

        global tts
        sr, wav = await tts.infer_with_ref_audio_embed(character, text)

        return Response(content=wav.tobytes(), media_type="application/octet-stream")
        
    except Exception as ex:
        tb_str = ''.join(traceback.format_exception(type(ex), ex, ex.__traceback__))
        print(tb_str)
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "error": str(tb_str)
            }
        )
```

### 7. Viết script khởi động sh (lưu ý phải chạy trong môi trường conda tương ứng)
```bash 
vi start_api.sh
```
### Dán nội dung sau vào và nhấn: Enter wq để lưu
#### Vui lòng sửa đổi /home/system/index-tts-vllm/model_dir/IndexTTS-1.5 trong tập lệnh thành đường dẫn thực tế.
``` bash
# Kích hoạt môi trường conda
conda kích hoạt chỉ mục-tts-vllm
echo "Kích hoạt môi trường conda của dự án"
ngủ 2
# Tìm ID tiến trình chiếm cổng 11996
PID_VLLM=$(sudo netstat -tulnp | grep 11996 | awk '{print $7}' | cut -d'/' -f1)

# Kiểm tra xem có tìm thấy số tiến trình không
nếu [ -z "$PID_VLLM" ]; sau đó
  echo "Không tìm thấy quá trình chiếm cổng 11996"
khác
  echo "Tìm tiến trình chiếm cổng 11996, số tiến trình là: $PID_VLLM"
  # Thử tiêu diệt thông thường trước, đợi 2 giây
  giết $PID_VLLM
  ngủ 2
  # Kiểm tra xem tiến trình còn ở đó không
  nếu ps -p $PID_VLLM > /dev/null; sau đó
    echo "Tiến trình vẫn đang chạy, buộc chấm dứt..."
    giết -9 $PID_VLLM
  fi
  echo "Quy trình đã kết thúc $PID_VLLM"
fi

# Tìm các tiến trình chiếm VLLM::EngineCore
GPU_PIDS=$(ps aux | grep -E "VLLM|EngineCore" | grep -v grep | awk '{print $2}')

# Kiểm tra xem có tìm thấy số tiến trình không
nếu [ -z "$GPU_PIDS" ]; sau đó
  echo "Không tìm thấy quy trình liên quan đến VLLM"
khác
  echo "Đã tìm thấy quy trình liên quan đến VLLM, số quy trình là: $GPU_PIDS"
  # Thử tiêu diệt thông thường trước, đợi 2 giây
  tiêu diệt $GPU_PIDS
  ngủ 2
  # Kiểm tra xem tiến trình còn ở đó không
  nếu ps -p $GPU_PIDS > /dev/null; sau đó
    echo "Tiến trình vẫn đang chạy, buộc chấm dứt..."
    tiêu diệt -9 $GPU_PIDS
  fi
  echo "Quá trình đã chấm dứt $GPU_PIDS"
fi

#Tạo thư mục tmp (nếu chưa tồn tại)
mkdir -p tmp

# Chạy api_server.py ở chế độ nền và chuyển hướng nhật ký đến tmp/server.log
Nohup python api_server.py --model_dir /home/system/index-tts-vllm/model_dir/IndexTTS-1.5 --port 11996 > tmp/server.log 2>&1 &
echo "api_server.py đang chạy ẩn, vui lòng kiểm tra tmp/server.log để biết nhật ký"
```
给脚本执行权限并运行脚本
```bash
chmod +x start_api.sh
./start_api.sh
```
日志会在tmp/server.log中输出，可以通过以下命令查看日志情况
```bash
đuôi -f tmp/server.log
```
Nếu bộ nhớ card đồ họa đủ, bạn có thể thêm tham số khởi động ----gpu_memory_utilization trong tập lệnh để điều chỉnh tỷ lệ sử dụng bộ nhớ đồ họa. Giá trị mặc định là 0,25

## Cấu hình giai điệu
index-tts-vllm hỗ trợ đăng ký âm sắc tùy chỉnh thông qua các tệp cấu hình và hỗ trợ cấu hình âm sắc đơn và âm sắc hỗn hợp.
Định cấu hình âm thanh tùy chỉnh trong tệp assets/loa.json trong thư mục gốc của dự án
### Mô tả định dạng cấu hình
```bash
{
    "说话人名称1": [
        "音频文件路径1.wav",
        "音频文件路径2.wav"
    ],
    "说话人名称2": [
        "音频文件路径3.wav"
    ]
}
```
### Lưu ý (sau khi cấu hình role, bạn cần khởi động lại dịch vụ để đăng ký âm thanh)
Sau khi thêm, bạn cần thêm loa tương ứng vào bảng điều khiển thông minh (đối với một mô-đun duy nhất, hãy thay thế giọng nói tương ứng)
