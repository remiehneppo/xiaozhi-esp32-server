#!/bin/bash
# Script build và chạy hệ thống xiaozhi-esp32-server từ source (không dùng Docker)
# Hỗ trợ interactive menu lựa chọn các service phụ thuộc để khởi chạy.

set -e

# ANSI colors
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0;5m' # No Color
RESET='\033[0m'

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

# ----------------- BIẾN MÔI TRƯỜNG & ĐỊNH NGHĨA PORT -----------------
# 1. xiaozhi-server: port 8010 (WS), 8013 (HTTP) hoặc config.yaml
# 2. manager-api (Java): port 8002
# 3. manager-web (Vue): port 8001 (proxies /xiaozhi -> 8002)
# 4. whisper-asr-server: port 8005
# 5. vieneu-tts-server: port 8004
# 6. digital-human: port 8006
# 7. mysql (DB): port 3306 (Yêu cầu đang chạy)
# 8. redis (Cache): port 6379 (Yêu cầu đang chạy)

echo -e "${CYAN}=== XIAOZHI-ESP32-SERVER SOURCE RUNNER ===${RESET}"
echo -e "Thư mục gốc: ${GREEN}$ROOT_DIR${RESET}"
echo ""

# HỎI MỤC TIÊU BẮT BUỘC:
# 1. Chạy standalone xiaozhi-server (chỉ cần config.yaml cục bộ)
# 2. Chạy full-stack (gồm manager-api + manager-web + db/redis để quản trị thiết bị)

echo -e "Chọn chế độ chạy bắt buộc:"
echo -e "  [1] Standalone Server (Chỉ chạy core xiaozhi-server, cấu hình bằng file data/.config.yaml)"
echo -e "  [2] Full-stack Management (Chạy cả quản trị web: xiaozhi-server + manager-api + manager-web)"
read -rp "Nhập lựa chọn [1-2] (Mặc định: 1): " CORE_CHOICE
CORE_CHOICE=${CORE_CHOICE:-1}

# LỰA CHỌN CÁC DỊCH VỤ PHỤ THUỘC (INTERACTIVE)
echo ""
echo -e "${YELLOW}--- LỰA CHỌN CÁC DỊCH VỤ PHỤ THUỘC ---${RESET}"

RUN_WHISPER="n"
RUN_VIENEU="n"
RUN_DH="n"

if [ "$CORE_CHOICE" = "2" ]; then
    echo -e "Chế độ Full-stack cần có MySQL (3306) và Redis (6379) đang chạy."
    read -rp "Khởi chạy/Kiểm tra container MySQL & Redis qua Docker? (y/n) (Mặc định: y): " RUN_DB
    RUN_DB=${RUN_DB:-y}
fi

read -rp "Khởi chạy local Whisper ASR Server (Nhận dạng tiếng Việt, port 8005)? (y/n) (Mặc định: n): " RUN_WHISPER
RUN_WHISPER=${RUN_WHISPER:-n}

read -rp "Khởi chạy local VieNeu TTS Server (Tổng hợp giọng nói tiếng Việt, port 8004)? (y/n) (Mặc định: n): " RUN_VIENEU
RUN_VIENEU=${RUN_VIENEU:-n}

read -rp "Khởi chạy local Digital Human (Con người kỹ thuật số để test Web/Wake word, port 8006)? (y/n) (Mặc định: n): " RUN_DH
RUN_DH=${RUN_DH:-n}

# TẢI MODEL CHẤT LƯỢNG CAO SENSEVOICESMALL NẾU CHƯA CÓ
MODEL_DIR="$ROOT_DIR/main/xiaozhi-server/models/SenseVoiceSmall"
if [ ! -f "$MODEL_DIR/model.pt" ]; then
    echo ""
    echo -e "${YELLOW}Không tìm thấy model.pt tại $MODEL_DIR/model.pt${RESET}"
    read -rp "Tải SenseVoiceSmall model.pt từ ModelScope (khoảng 300MB)? (y/n) (Mặc định: y): " DL_MODEL
    DL_MODEL=${DL_MODEL:-y}
    if [ "$DL_MODEL" = "y" ] || [ "$DL_MODEL" = "Y" ]; then
        mkdir -p "$MODEL_DIR"
        echo "Đang tải model.pt..."
        curl -fL --progress-bar "https://modelscope.cn/models/iic/SenseVoiceSmall/resolve/master/model.pt" -o "$MODEL_DIR/model.pt"
        echo -e "${GREEN}Tải xong!${RESET}"
    fi
fi

# TẢI MODEL WAKEWORD CHO DIGITAL HUMAN NẾU CHỌN CHẠY VÀ CHƯA CÓ
if [ "$RUN_DH" = "y" ] || [ "$RUN_DH" = "Y" ]; then
    DH_MODEL_DIR="$ROOT_DIR/main/digital-human/wakeword_runtime/models/sherpa-onnx-kws-zipformer-wenetspeech-3.3M-2024-01-01"
    if [ ! -d "$DH_MODEL_DIR" ]; then
        echo ""
        echo -e "${YELLOW}Không tìm thấy mô hình Wake Word tại $DH_MODEL_DIR${RESET}"
        read -rp "Tải mô hình Wake Word Sherpa-ONNX (khoảng 15MB)? (y/n) (Mặc định: y): " DL_WW
        DL_WW=${DL_WW:-y}
        if [ "$DL_WW" = "y" ] || [ "$DL_WW" = "Y" ]; then
            mkdir -p "$ROOT_DIR/main/digital-human/wakeword_runtime/models"
            echo "Đang tải và giải nén mô hình Wake Word..."
            curl -fL "https://github.com/k2-fsa/sherpa-onnx/releases/download/kws-models/sherpa-onnx-kws-zipformer-wenetspeech-3.3M-2024-01-01.tar.bz2" -o "$ROOT_DIR/main/digital-human/wakeword_runtime/models.tar.bz2"
            tar -xjf "$ROOT_DIR/main/digital-human/wakeword_runtime/models.tar.bz2" -C "$ROOT_DIR/main/digital-human/wakeword_runtime/models"
            rm "$ROOT_DIR/main/digital-human/wakeword_runtime/models.tar.bz2"
            echo -e "${GREEN}Tải xong mô hình Wake Word!${RESET}"
        fi
    fi
fi

# ----------------- KHỞI TẠO CẤU HÌNH VÀ VENV -----------------
# Sử dụng venv ở root hoặc tạo mới
VENV_BIN="$ROOT_DIR/venv/bin"
if [ ! -f "$VENV_BIN/python" ]; then
    echo -e "${YELLOW}Không tìm thấy venv tại root. Đang tạo venv mới...${RESET}"
    python3 -m venv "$ROOT_DIR/venv"
    "$VENV_BIN/pip" install --upgrade pip
    "$VENV_BIN/pip" install -r "$ROOT_DIR/main/xiaozhi-server/requirements.txt"
fi

# Hàm kill tiến trình chạy port
kill_port() {
    local port=$1
    local pid=$(lsof -t -i:"$port" || true)
    if [ -n "$pid" ]; then
        echo "Cổng $port đang bận bởi PID $pid. Đang dừng..."
        kill -9 $pid || true
        sleep 1
    fi
}

stop_docker_container() {
    local container_name=$1
    if docker ps -a --format '{{.Names}}' | grep -q "^${container_name}$"; then
        echo "Dừng container Docker ${container_name} để giải phóng cổng..."
        docker stop "${container_name}" || true
    fi
}

# ----------------- KHỞI CHẠY CÁC THÀNH PHẦN -----------------

# 0. MySQL và Redis qua Docker nếu được chọn
if [ "$RUN_DB" = "y" ] || [ "$RUN_DB" = "Y" ]; then
    echo -e "\n${CYAN}[DB & Redis]${RESET} Đang kiểm tra/Khởi chạy container qua Docker..."
    if ! docker ps -a | grep -q "xiaozhi-esp32-server-db"; then
        echo "Tạo container MySQL..."
        docker run --name xiaozhi-esp32-server-db -e MYSQL_ROOT_PASSWORD=123456 -p 3306:3306 -e MYSQL_DATABASE=xiaozhi_esp32_server -e MYSQL_INITDB_ARGS="--character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci" -e TZ=Asia/Ho_Chi_Minh -d mysql:latest
    else
        docker start xiaozhi-esp32-server-db || true
    fi

    if ! docker ps -a | grep -q "xiaozhi-esp32-server-redis"; then
        echo "Tạo container Redis..."
        docker run --name xiaozhi-esp32-server-redis -d -p 6379:6379 redis:8-alpine
    else
        docker start xiaozhi-esp32-server-redis || true
    fi
fi

# 1. Whisper ASR Server (Port 8005)
if [ "$RUN_WHISPER" = "y" ] || [ "$RUN_WHISPER" = "Y" ]; then
    echo -e "\n${CYAN}[Whisper ASR]${RESET} Đang khởi chạy Whisper ASR Server..."
    stop_docker_container "whisper-asr-server"
    kill_port 8005
    
    # Tạo venv cho whisper nếu chưa có hoặc dùng venv gốc
    ASR_DIR="$ROOT_DIR/main/whisper-asr-server"
    ASR_VENV="$ASR_DIR/.venv"
    if [ ! -d "$ASR_VENV" ]; then
        if [ -f "$ROOT_DIR/venv/bin/python" ]; then
            echo "Phát hiện venv gốc tại $ROOT_DIR/venv. Sử dụng venv gốc để chạy Whisper ASR..."
            ASR_VENV="$ROOT_DIR/venv"
        else
            echo "Tạo venv cho Whisper ASR..."
            python3 -m venv "$ASR_VENV"
            "$ASR_VENV/bin/pip" install --upgrade pip
            "$ASR_VENV/bin/pip" install -r "$ASR_DIR/requirements.txt"
        fi
    fi
    
    # Chạy ngầm và ghi log
    export WHISPER_MODEL="quocphu/PhoWhisper-ct2-FasterWhisper/PhoWhisper-small-ct2-fasterWhisper"
    export WHISPER_DEVICE="cpu"
    export WHISPER_COMPUTE_TYPE="int8"
    export WHISPER_LANGUAGE="vi"
    export WHISPER_MODEL_DIR="$ASR_DIR/models"
    export HF_HOME="$ASR_DIR/models"
    
    nohup "$ASR_VENV/bin/uvicorn" app:app --host 0.0.0.0 --port 8005 --app-dir "$ASR_DIR" > "$ROOT_DIR/logs/whisper-asr.log" 2>&1 &
    echo -e "${GREEN}Whisper ASR đã chạy ngầm (Port 8005). Log: logs/whisper-asr.log${RESET}"
fi

# 2. VieNeu TTS Server (Port 8004)
if [ "$RUN_VIENEU" = "y" ] || [ "$RUN_VIENEU" = "Y" ]; then
    echo -e "\n${CYAN}[VieNeu TTS]${RESET} Đang khởi chạy VieNeu TTS Server..."
    stop_docker_container "vieneu-tts-server"
    kill_port 8004
    
    TTS_DIR="$ROOT_DIR/main/vieneu-tts-server"
    # Dùng venv sẵn hoặc tạo mới
    TTS_VENV="$TTS_DIR/.venv-gpu"
    if [ ! -d "$TTS_VENV" ]; then
        TTS_VENV="$TTS_DIR/.venv"
        if [ ! -d "$TTS_VENV" ]; then
            echo "Tạo venv cho VieNeu TTS..."
            python3 -m venv "$TTS_VENV"
            "$TTS_VENV/bin/pip" install --upgrade pip
            "$TTS_VENV/bin/pip" install -r "$TTS_DIR/requirements.txt"
        fi
    fi
    
    # Cấu hình env
    export VIENEU_MODEL_ID="pnnbao-ump/VieNeu-TTS-v2-Turbo-GGUF"
    export VIENEU_MODEL_FILE="vieneu-tts-v2-turbo.gguf"
    export VIENEU_MODE="turbo"
    export VIENEU_MODEL_DIR="$TTS_DIR/models"
    export HF_HOME="$TTS_DIR/models"
    export HUGGINGFACE_HUB_CACHE="$TTS_DIR/models/hub"
    export VIENEU_DEFAULT_VOICE="Thục Đoan (Nữ - Miền Nam)"
    # Tự động chọn device nếu có GPU cuda
    if "$VENV_BIN/python" -c "import torch; exit(0 if torch.cuda.is_available() else 1)" 2>/dev/null; then
        export VIENEU_DEVICE="cuda"
        export VIENEU_N_GPU_LAYERS="99"
    else
        export VIENEU_DEVICE="cpu"
        export VIENEU_N_GPU_LAYERS="0"
    fi
    
    nohup "$TTS_VENV/bin/uvicorn" app:app --host 0.0.0.0 --port 8004 --app-dir "$TTS_DIR" > "$ROOT_DIR/logs/vieneu-tts.log" 2>&1 &
    echo -e "${GREEN}VieNeu TTS đã chạy ngầm (Port 8004, Device: $VIENEU_DEVICE). Log: logs/vieneu-tts.log${RESET}"
fi

# 3. Manager API & Web (Java / Vue)
if [ "$CORE_CHOICE" = "2" ]; then
    echo -e "\n${CYAN}[Manager API]${RESET} Đang kiểm tra build và khởi chạy Java backend..."
    stop_docker_container "xiaozhi-esp32-server-web"
    kill_port 8002
    
    API_DIR="$ROOT_DIR/main/manager-api"
    # Kiểm tra và build JAR nếu chưa có hoặc yêu cầu rebuild
    if [ ! -f "$API_DIR/target/xiaozhi-esp32-api.jar" ]; then
        echo "Đang build manager-api bằng Maven..."
        "$ROOT_DIR/tmp/maven/bin/mvn" -f "$API_DIR/pom.xml" clean package -Dmaven.test.skip=true
    fi
    
    # Chạy manager-api
    mkdir -p "$ROOT_DIR/logs"
    nohup "$ROOT_DIR/tmp/jdk21/bin/java" -jar "$API_DIR/target/xiaozhi-esp32-api.jar" --spring.profiles.active=dev > "$ROOT_DIR/logs/manager-api.log" 2>&1 &
    echo -e "${GREEN}Manager API đã chạy ngầm (Port 8002). Log: logs/manager-api.log${RESET}"
    
    echo -e "\n${CYAN}[Manager Web]${RESET} Đang khởi chạy Vue frontend..."
    kill_port 8001
    
    WEB_DIR="$ROOT_DIR/main/manager-web"
    # Kiểm tra node_modules
    if [ ! -d "$WEB_DIR/node_modules" ]; then
        echo "Đang cài đặt node dependencies cho manager-web..."
        cd "$WEB_DIR" && npm install && cd "$ROOT_DIR"
    fi
    
    # Chạy Vue dev server (lắng nghe port 8001 và proxy /xiaozhi -> 8002)
    cd "$WEB_DIR"
    nohup npm run serve > "$ROOT_DIR/logs/manager-web.log" 2>&1 &
    cd "$ROOT_DIR"
    echo -e "${GREEN}Manager Web đã chạy ngầm (Port 8001). Log: logs/manager-web.log${RESET}"
fi

# 4. Digital Human (Port 8006)
if [ "$RUN_DH" = "y" ] || [ "$RUN_DH" = "Y" ]; then
    echo -e "\n${CYAN}[Digital Human]${RESET} Đang khởi chạy Digital Human..."
    kill_port 8006
    
    DH_DIR="$ROOT_DIR/main/digital-human"
    DH_VENV="$DH_DIR/.venv"
    if [ ! -d "$DH_VENV" ]; then
        if [ -f "$ROOT_DIR/venv/bin/python" ]; then
            echo "Phát hiện venv gốc tại $ROOT_DIR/venv. Sử dụng venv gốc để chạy Digital Human..."
            DH_VENV="$ROOT_DIR/venv"
        else
            echo "Tạo venv cho Digital Human..."
            python3 -m venv "$DH_VENV"
            "$DH_VENV/bin/pip" install --upgrade pip
            "$DH_VENV/bin/pip" install -r "$DH_DIR/wakeword_runtime/requirements.txt"
        fi
    fi
    
    nohup "$DH_VENV/bin/python" "$DH_DIR/start.py" > "$ROOT_DIR/logs/digital-human.log" 2>&1 &
    echo -e "${GREEN}Digital Human đã chạy ngầm (Port 8006). Log: logs/digital-human.log${RESET}"
fi

# 5. Core xiaozhi-server (Port 8010, HTTP 8013)
echo -e "\n${CYAN}[xiaozhi-server]${RESET} Đang chuẩn bị cấu hình..."
stop_docker_container "xiaozhi-esp32-server"
kill_port 8010
kill_port 8013

SERVER_DIR="$ROOT_DIR/main/xiaozhi-server"
mkdir -p "$SERVER_DIR/data"

# Sao chép file config mẫu nếu chưa có data/.config.yaml
if [ ! -f "$SERVER_DIR/data/.config.yaml" ]; then
    if [ "$CORE_CHOICE" = "2" ]; then
        echo "Sử dụng cấu hình Bootstrap (config_from_api_vi.yaml)..."
        cp "$SERVER_DIR/config_from_api_vi.yaml" "$SERVER_DIR/data/.config.yaml"
    else
        echo "Sử dụng cấu hình Standalone (config_vi_whisper.yaml)..."
        cp "$SERVER_DIR/config_vi_whisper.yaml" "$SERVER_DIR/data/.config.yaml"
    fi
fi

# Nhập server.secret nếu chạy ở chế độ full-stack
if [ "$CORE_CHOICE" = "2" ]; then
    echo -e "${YELLOW}Vui lòng mở trình duyệt truy cập http://127.0.0.1:8001 để đăng ký tài khoản admin.${RESET}"
    echo -e "Sau đó vào menu: Quản lý tham số -> Tìm tham số 'server.secret'."
    read -rp "Nhập khóa server.secret (Để trống để bỏ qua): " SECRET_KEY
    if [ -n "$SECRET_KEY" ]; then
        "$VENV_BIN/python" -c "
import yaml
config_path = '$SERVER_DIR/data/.config.yaml'
with open(config_path, 'r') as f:
    config = yaml.safe_load(f) or {}
config['manager-api'] = {'url': 'http://127.0.0.1:8002/xiaozhi', 'secret': '$SECRET_KEY'}
with open(config_path, 'w') as f:
    yaml.dump(config, f)
"
        echo -e "${GREEN}Cập nhật secret thành công!${RESET}"
    fi
fi

# Chạy core server
echo "Đang khởi chạy core xiaozhi-server..."
cd "$SERVER_DIR"
# Nhấn Ctrl+C để tắt core server và toàn bộ dịch vụ ngầm
trap 'echo -e "\nĐang dừng các dịch vụ ngầm..."; kill $(jobs -p) 2>/dev/null; exit 0' SIGINT SIGTERM

"$VENV_BIN/python" app.py

