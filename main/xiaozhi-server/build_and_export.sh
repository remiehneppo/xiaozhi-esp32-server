#!/bin/bash
# Hướng dẫn chạy: ./build_and_export.sh <tên_username_docker_hub>
# Ví dụ: ./build_and_export.sh remiehneppo

set -e

# Đặt registry/username mặc định là remiehneppo
REGISTRY="${1:-remiehneppo}"
EXPORT_DIR="exports"

echo "=========================================================="
echo "Bắt đầu build và export các Docker image ra file tar"
echo "Registry/Username sử dụng: $REGISTRY"
echo "Thư mục xuất file tar: $EXPORT_DIR"
echo "=========================================================="

# Lấy đường dẫn gốc của dự án
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$ROOT_DIR"

# Tạo thư mục exports ở thư mục chạy script
mkdir -p "$SCRIPT_DIR/$EXPORT_DIR"

# 1. Build xiaozhi-esp32-server
echo ">> 1. Đang build: xiaozhi-esp32-server..."
docker build -t "$REGISTRY/xiaozhi-esp32-server:latest" -f Dockerfile-server .
echo ">> Đang export: xiaozhi-esp32-server:latest..."
docker save -o "$SCRIPT_DIR/$EXPORT_DIR/xiaozhi-esp32-server.tar" "$REGISTRY/xiaozhi-esp32-server:latest"

# 2. Build xiaozhi-esp32-server-web
echo ">> 2. Đang build: xiaozhi-esp32-server-web..."
docker build -t "$REGISTRY/xiaozhi-esp32-server-web:latest" -f Dockerfile-web .
echo ">> Đang export: xiaozhi-esp32-server-web:latest..."
docker save -o "$SCRIPT_DIR/$EXPORT_DIR/xiaozhi-esp32-server-web.tar" "$REGISTRY/xiaozhi-esp32-server-web:latest"

# 3. Build vieneu-tts-server (CPU)
echo ">> 3. Đang build: vieneu-tts-server (CPU)..."
docker build -t "$REGISTRY/vieneu-tts-server:cpu-latest" -f main/vieneu-tts-server/Dockerfile main/vieneu-tts-server
echo ">> Đang export: vieneu-tts-server:cpu-latest..."
docker save -o "$SCRIPT_DIR/$EXPORT_DIR/vieneu-tts-server-cpu.tar" "$REGISTRY/vieneu-tts-server:cpu-latest"

# 4. Build whisper-asr-server (CPU)
echo ">> 4. Đang build: whisper-asr-server (CPU)..."
docker build -t "$REGISTRY/whisper-asr-server:cpu-latest" -f main/whisper-asr-server/Dockerfile main/whisper-asr-server
echo ">> Đang export: whisper-asr-server:cpu-latest..."
docker save -o "$SCRIPT_DIR/$EXPORT_DIR/whisper-asr-server-cpu.tar" "$REGISTRY/whisper-asr-server:cpu-latest"

echo "=========================================================="
echo "Hoàn thành xuất 4 file tar thành công!"
echo "Danh sách các file trong thư mục $SCRIPT_DIR/$EXPORT_DIR:"
ls -lh "$SCRIPT_DIR/$EXPORT_DIR"
echo "----------------------------------------------------------"
echo "Để load các file này ở máy chủ khác, hãy dùng lệnh:"
echo "  docker load -i <tên_file>.tar"
echo "=========================================================="
