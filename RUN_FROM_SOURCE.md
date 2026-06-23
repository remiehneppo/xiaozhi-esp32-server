# Hướng Dẫn Chạy Xiaozhi-ESP32-Server Từ Source

Hướng dẫn này giúp bạn build và khởi chạy toàn bộ hệ thống xiaozhi-esp32-server từ source code **không sử dụng Docker**.

## Yêu Cầu Hệ Thống

### Phần mềm bắt buộc
- **Python 3.12+** 
- **Java 21** (OpenJDK)
- **Node.js 18+** và **npm**
- **MySQL 8.0+** (có thể chạy qua Docker)
- **Redis 6.0+** (có thể chạy qua Docker)

### Phần cứng khuyến nghị
- **RAM**: Tối thiểu 8GB (khuyến nghị 16GB nếu chạy full-stack)
- **Disk**: 10GB trống (cho models và dependencies)
- **CPU**: 4 cores+ (hỗ trợ AVX2 để tăng tốc inference)
- **GPU**: Tùy chọn (CUDA-compatible GPU để tăng tốc TTS)

## Chuẩn Bị

### 1. Clone Repository
```bash
git clone https://github.com/your-repo/xiaozhi-esp32-server.git
cd xiaozhi-esp32-server
```

### 2. Cài Đặt Dependencies Hệ Thống

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv \
    openjdk-21-jdk maven nodejs npm \
    portaudio19-dev libsndfile1 lsof curl
```

**macOS:**
```bash
brew install python@3.12 openjdk@21 maven node portaudio libsndfile
```

### 3. Tạo Python Virtual Environment (Khuyến nghị)

Script `run-source.sh` sẽ tự động tạo và quản lý virtualenv, nhưng bạn có thể tạo trước:

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r main/xiaozhi-server/requirements.txt
```

### 4. Chuẩn Bị Database (Nếu Chạy Full-stack)

Bạn có thể:
- **Option A**: Sử dụng Docker containers (script sẽ tự động khởi động)
- **Option B**: Cài đặt MySQL và Redis local

**Option A - Docker (Khuyến nghị):**
```bash
# Script sẽ tự động tạo và khởi động containers khi cần
# Hoặc chạy thủ công:
docker run -d --name xiaozhi-db \
  -e MYSQL_ROOT_PASSWORD=123456 \
  -e MYSQL_DATABASE=xiaozhi_esp32_server \
  -p 3306:3306 mysql:latest

docker run -d --name xiaozhi-redis \
  -p 6379:6379 redis:8-alpine
```

## Sử Dụng Script Tự Động

### Khởi Chạy

```bash
chmod +x run-source.sh
./run-source.sh
```

### Menu Tương Tác

#### Bước 1: Chọn Chế Độ Chạy

**[1] Standalone Server**
- Chỉ chạy core `xiaozhi-server`
- Cấu hình từ file `main/xiaozhi-server/data/.config.yaml`
- Không cần database/Redis
- Phù hợp: Phát triển local, testing đơn giản

**[2] Full-stack Management**
- Chạy đầy đủ: `xiaozhi-server` + `manager-api` + `manager-web`
- Quản lý tập trung qua web UI
- Yêu cầu: MySQL (port 3306) và Redis (port 6379)
- Phù hợp: Production, quản lý nhiều thiết bị

#### Bước 2: Chọn Dịch Vụ Phụ Thuộc (Tùy chọn)

**Whisper ASR Server** (Port 8005)
- Nhận dạng giọng nói tiếng Việt offline
- Model: PhoWhisper-small-ct2-fasterWhisper
- RAM: ~2GB khi chạy
- Khởi động: ~10 giây (download model lần đầu: ~500MB)

**VieNeu TTS Server** (Port 8004)
- Tổng hợp giọng nói tiếng Việt offline
- Model: VieNeu-TTS-v2-Turbo-GGUF
- Hỗ trợ: CPU và CUDA GPU
- RAM: ~1-2GB

**Digital Human** (Port 8006)
- Wake word detection (Sherpa-ONNX)
- Web-based testing interface
- RAM: ~500MB

#### Bước 3: Tải Models (Tự động)

Script sẽ tự động hỏi và download các models cần thiết:

- **SenseVoiceSmall** (~300MB): Model ASR chất lượng cao (nếu dùng FunASR)
- **Sherpa-ONNX Wake Word** (~15MB): Model wake word detection

## Cấu Hình Dịch Vụ

### Cổng Mặc Định

| Dịch Vụ | Cổng | Giao Thức | Mô Tả |
|---------|------|-----------|-------|
| Manager Web | 8001 | HTTP | Vue.js dev server (development) |
| Manager API | 8002 | HTTP | Spring Boot REST API |
| VieNeu TTS | 8004 | HTTP | TTS service |
| Whisper ASR | 8005 | HTTP | ASR service |
| Digital Human | 8006 | HTTP/WS | Wake word + web UI |
| Xiaozhi Server | 8010 | WebSocket | Main ESP32 communication |
| Xiaozhi Server | 8013 | HTTP | OTA updates + vision API |

### File Cấu Hình

**Standalone Mode:**
```
main/xiaozhi-server/data/.config.yaml
```
Tự động copy từ `config_vi_whisper.yaml` nếu chưa tồn tại.

**Full-stack Mode:**
```
main/xiaozhi-server/data/.config.yaml
```
Tự động copy từ `config_from_api_vi.yaml` và cần cấu hình `server.secret`.

## Quy Trình Khởi Động Full-stack

### 1. Chạy Script
```bash
./run-source.sh
```

Chọn:
- `[2]` - Full-stack Management
- `[y]` hoặc `[n]` cho MySQL/Redis Docker
- `[y]` hoặc `[n]` cho các service tùy chọn
- `[n]` để bỏ qua download SenseVoiceSmall (nếu dùng Whisper ASR)

### 2. Đăng Ký Tài Khoản Admin

Mở trình duyệt: **http://127.0.0.1:8001**

- Đăng ký người dùng **đầu tiên** → Trở thành **Super Admin**
- Người dùng sau → Quyền thông thường

### 3. Lấy Server Secret

1. Đăng nhập với tài khoản admin
2. Menu: **Quản lý tham số**
3. Tìm tham số: **`server.secret`**
4. Copy giá trị secret

### 4. Cập Nhật Cấu Hình

- Script sẽ hỏi `server.secret` khi khởi động
- Paste secret vừa copy
- Hoặc cập nhật thủ công vào `data/.config.yaml`:

```yaml
manager-api:
  url: http://127.0.0.1:8002/xiaozhi
  secret: "<secret-key-từ-web-ui>"
```

### 5. Khởi Động Hoàn Tất

Core `xiaozhi-server` sẽ chạy ở foreground và hiển thị logs.

Nhấn **Ctrl+C** để dừng toàn bộ hệ thống.

## Logs và Debugging

### Vị Trí Logs

```
logs/
├── whisper-asr.log          # Whisper ASR service
├── vieneu-tts.log           # VieNeu TTS service
├── digital-human.log        # Digital Human service
├── manager-api.log          # Manager API stdout
├── manager-web.log          # Vue dev server
└── xiaozhi-esp32-api.log    # Manager API application log
```

**Manager API chi tiết:**
```
main/manager-api/logs/
├── xiaozhi-esp32-api.log    # Main application log
└── error.log                # Error-only log
```

### Kiểm Tra Trạng Thái

```bash
# Kiểm tra các cổng đang lắng nghe
lsof -i :8001 -i :8002 -i :8004 -i :8005 -i :8006 -i :8010 -i :8013

# Xem logs real-time
tail -f logs/whisper-asr.log
tail -f main/manager-api/logs/xiaozhi-esp32-api.log

# Kiểm tra tiến trình
ps aux | grep java
ps aux | grep python
ps aux | grep node
```

## Tối Ưu Hóa

### 1. Tái Sử Dụng Virtual Environment

Script tự động phát hiện và sử dụng lại `venv` ở thư mục root cho:
- Whisper ASR Server
- Digital Human

Điều này tiết kiệm:
- **Thời gian**: Không cần cài lại dependencies
- **Dung lượng**: Không duplicate packages
- **Băng thông**: Không download lại PyTorch, Transformers

### 2. Dừng Docker Containers Tự Động

Script tự động dừng các Docker containers sau nếu đang chạy:
- `whisper-asr-server`
- `vieneu-tts-server`
- `xiaozhi-esp32-server-web`
- `xiaozhi-esp32-server`

Để giải phóng cổng trước khi chạy từ source.

### 3. GPU Acceleration

**VieNeu TTS** tự động phát hiện CUDA:
```bash
# Kiểm tra GPU
python3 -c "import torch; print(torch.cuda.is_available())"
```

Nếu có GPU, script sẽ tự động:
- Set `VIENEU_DEVICE=cuda`
- Set `VIENEU_N_GPU_LAYERS=99`

## Troubleshooting

### Lỗi: "Port already in use"

**Nguyên nhân:** Cổng bị chiếm bởi tiến trình khác.

**Giải pháp:**
```bash
# Tìm tiến trình đang chiếm cổng (ví dụ: 8002)
lsof -i :8002

# Dừng tiến trình
kill -9 <PID>

# Hoặc để script tự động xử lý
# Script có hàm kill_port tích hợp
```

### Lỗi: "Exception: cấu hìnhmanager-apisecret"

**Nguyên nhân:** Chạy Full-stack mode nhưng chưa cấu hình `server.secret`.

**Giải pháp:**
1. Mở http://127.0.0.1:8001
2. Đăng ký/đăng nhập admin
3. Lấy `server.secret` từ **Quản lý tham số**
4. Chạy lại script và nhập secret

### Lỗi: "No module named 'xxx'"

**Nguyên nhân:** Thiếu Python dependencies.

**Giải pháp:**
```bash
source venv/bin/activate
pip install -r main/xiaozhi-server/requirements.txt
```

### Lỗi: Maven build failed

**Nguyên nhân:** Chưa cài Maven hoặc không có Java 21.

**Giải pháp:**
```bash
# Kiểm tra Java version
java -version  # Phải là 21+

# Cài Maven (Ubuntu)
sudo apt install maven

# Script có Maven embedded tại tmp/maven/bin/mvn
```

### Lỗi: MySQL connection refused

**Nguyên nhân:** MySQL chưa chạy hoặc chưa expose port 3306.

**Giải pháp:**
```bash
# Kiểm tra MySQL container
docker ps | grep mysql

# Khởi động MySQL
docker start xiaozhi-esp32-server-db

# Hoặc tạo mới
docker run -d --name xiaozhi-db \
  -e MYSQL_ROOT_PASSWORD=123456 \
  -e MYSQL_DATABASE=xiaozhi_esp32_server \
  -p 3306:3306 mysql:latest
```

### Whisper ASR/VieNeu TTS không start

**Nguyên nhân:** Model chưa download hoặc virtualenv lỗi.

**Giải pháp:**
```bash
# Kiểm tra logs
tail -f logs/whisper-asr.log
tail -f logs/vieneu-tts.log

# Download model thủ công
cd main/whisper-asr-server
source .venv/bin/activate
python -c "from faster_whisper import WhisperModel; WhisperModel('quocphu/PhoWhisper-ct2-FasterWhisper/PhoWhisper-small-ct2-fasterWhisper')"
```

## Dừng Hệ Thống

### Dừng Tất Cả

Nhấn **Ctrl+C** trong terminal đang chạy `xiaozhi-server` (foreground).

Script sẽ tự động:
- Bắt tín hiệu SIGINT
- Dừng các background services (manager-api, manager-web, whisper-asr, vieneu-tts, digital-human)
- Exit clean

### Dừng Riêng Lẻ

```bash
# Dừng bằng port
lsof -t -i:8002 | xargs kill -9  # Manager API
lsof -t -i:8001 | xargs kill -9  # Manager Web
lsof -t -i:8005 | xargs kill -9  # Whisper ASR
lsof -t -i:8004 | xargs kill -9  # VieNeu TTS
lsof -t -i:8006 | xargs kill -9  # Digital Human
lsof -t -i:8010 | xargs kill -9  # Xiaozhi Server
```

## So Sánh Docker vs Source

| Tiêu Chí | Docker | Source |
|----------|--------|--------|
| **Setup** | Đơn giản, 1 lệnh | Cần cài dependencies |
| **Tốc độ khởi động** | Nhanh (images có sẵn) | Lâu hơn (build lần đầu) |
| **Phát triển** | Rebuild image mỗi lần | Hot reload (Vue), restart nhanh |
| **Debugging** | Phức tạp (vào container) | Dễ (logs trực tiếp, IDE attach) |
| **Tài nguyên** | Overhead container | Native performance |
| **Production** | ✅ Khuyến nghị | Không khuyến nghị |
| **Development** | ⚠️ Khả dụng | ✅ Khuyến nghị |

## Ghi Chú Quan Trọng

### Port Conflicts

- **Port 8001**: Mặc định dành cho **manager-web** (Vue dev server)
- **Whisper ASR** đã được đổi từ 8001 → **8005** để tránh xung đột
- File config đã được cập nhật: `main/xiaozhi-server/config_vi_whisper.yaml`

### Docker Compatibility

- Script có thể chạy song song với Docker containers khác
- Tự động stop các containers của chính nó trước khi start from source
- MySQL và Redis có thể dùng Docker (khuyến nghị) hoặc native

### Background Services

Các service chạy background (manager-api, whisper-asr, etc.) sử dụng `nohup` và ghi logs vào `logs/`.

Nếu script exit unexpected, các background processes có thể vẫn chạy. Dừng thủ công bằng `kill`.

## Tham Khảo

- **README chính**: [README.md](README.md)
- **Docker setup**: [docker-setup.sh](docker-setup.sh)
- **Deployment guide**: [docs/Deployment_all.md](docs/Deployment_all.md)

## Liên Hệ & Hỗ Trợ

- **Issues**: [GitHub Issues](https://github.com/your-repo/xiaozhi-esp32-server/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-repo/xiaozhi-esp32-server/discussions)

---

**Phiên bản:** 1.0  
**Cập nhật:** 2026-06-23
