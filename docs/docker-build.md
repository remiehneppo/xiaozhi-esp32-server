# Cách biên dịch images docker cục bộ

Bây giờ dự án này đã sử dụng chức năng biên dịch docker tự động của github. Tài liệu này được cung cấp cho những người bạn cần biên dịch images docker cục bộ.

1. Cài đặt docker
```
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```
2. Biên dịch images docker
```
#Nhập thư mục gốc của dự án
#Máy chủ biên dịch
docker build -t xiaozhi-esp32-server:server_latest -f ./Dockerfile-server .
#Biên dịch web
docker build -t xiaozhi-esp32-server:web_latest -f ./Dockerfile-web .

# Sau khi biên dịch xong, bạn có thể sử dụng docker-compose để bắt đầu dự án
# docker-compose.yml Bạn cần sửa nó thành phiên bản image do chính bạn biên dịch
cd chính/máy chủ xiaozhi
docker soạn thảo -d
```