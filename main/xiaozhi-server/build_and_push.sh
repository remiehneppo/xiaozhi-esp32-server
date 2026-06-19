#!/bin/bash
# Hướng dẫn chạy: ./build_and_push.sh <tên_username_docker_hub>
# Ví dụ: ./build_and_push.sh tieubaoca

set -e

# Đặt registry/username mặc định là remiehneppo
REGISTRY="${1:-remiehneppo}"

echo "=========================================================="
echo "Bắt đầu build và push các Docker image lên Docker Hub"
echo "Registry/Username sử dụng: $REGISTRY"
echo "=========================================================="

# Yêu cầu đăng nhập Docker Hub
echo ">> Kiểm tra đăng nhập Docker Hub..."
docker login

# Lấy đường dẫn gốc của dự án
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$ROOT_DIR"

# 1. Build & Push xiaozhi-esp32-server
echo ">> 1. Đang build: xiaozhi-esp32-server..."
docker build -t "$REGISTRY/xiaozhi-esp32-server:latest" -f Dockerfile-server .
echo ">> Đang push: xiaozhi-esp32-server:latest..."
docker push "$REGISTRY/xiaozhi-esp32-server:latest"

# 2. Build & Push xiaozhi-esp32-server-web
echo ">> 2. Đang build: xiaozhi-esp32-server-web..."
docker build -t "$REGISTRY/xiaozhi-esp32-server-web:latest" -f Dockerfile-web .
echo ">> Đang push: xiaozhi-esp32-server-web:latest..."
docker push "$REGISTRY/xiaozhi-esp32-server-web:latest"

# 3. Build & Push vieneu-tts-server (CPU)
echo ">> 3. Đang build: vieneu-tts-server (CPU)..."
docker build -t "$REGISTRY/vieneu-tts-server:cpu-latest" -f main/vieneu-tts-server/Dockerfile main/vieneu-tts-server
echo ">> Đang push: vieneu-tts-server:cpu-latest..."
docker push "$REGISTRY/vieneu-tts-server:cpu-latest"

# 4. Build & Push whisper-asr-server (CPU)
echo ">> 4. Đang build: whisper-asr-server (CPU)..."
docker build -t "$REGISTRY/whisper-asr-server:cpu-latest" -f main/whisper-asr-server/Dockerfile main/whisper-asr-server
echo ">> Đang push: whisper-asr-server:cpu-latest..."
docker push "$REGISTRY/whisper-asr-server:cpu-latest"

echo "=========================================================="
echo "Hoàn thành build và push toàn bộ 4 image lên Docker Hub!"
echo "=========================================================="
