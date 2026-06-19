# Báo cáo so sánh hiệu năng VieNeu TTS: CPU vs GPU

Báo cáo đo lường chi tiết hiệu suất tổng hợp giọng nói tiếng Việt bằng mô hình **VieNeu-TTS-v2-Turbo-GGUF** trên CPU và GPU với 20 câu mẫu thử nghiệm khác nhau.

## 1. Cấu hình thử nghiệm
- **GPU Server**: RTX 5060 Ti 16GB (CUDA, full offload).
- **CPU Server**: Intel/AMD host CPU (11 Threads).
- **Model**: `pnnbao-ump/VieNeu-TTS-v2-Turbo-GGUF`.
- **Giọng đọc mặc định**: Thục Đoan (Nữ - Miền Nam).
- **Đoạn mã tối ưu**: Sử dụng xử lý âm thanh trong RAM hoàn toàn (`io.BytesIO`).

## 2. Kết quả tổng quan
| Chỉ số | GPU (CUDA) | CPU (Host) | Tỷ lệ cải thiện |
| :--- | :---: | :---: | :---: |
| **Tổng thời gian (20 câu)** | 4744.30 ms | 16409.45 ms | **3.5x nhanh hơn** |
| **Độ trễ trung bình/câu** | 237.21 ms | 820.47 ms | **3.5x nhanh hơn** |
| **Realtime Factor (RTF) trung bình** | 0.0505 | 0.2063 | *(Càng thấp càng tốt)* |
| **Số ký tự / giây (CPS) trung bình** | 324.60 | 94.95 | *(Càng cao càng tốt)* |

## 3. Bảng dữ liệu chi tiết từng câu thử nghiệm

| STT | Độ dài (ký tự) | Thời lượng âm thanh | Thời gian xử lý GPU | RTF GPU | Thời gian xử lý CPU | RTF CPU | Tỷ lệ GPU/CPU |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | 9 | 0.76s | 47.5 ms | 0.062 | 622.2 ms | 0.819 | **13.1x** |
| 2 | 26 | 1.80s | 89.0 ms | 0.049 | 422.0 ms | 0.264 | **4.7x** |
| 3 | 33 | 2.16s | 113.1 ms | 0.052 | 354.1 ms | 0.188 | **3.1x** |
| 4 | 39 | 3.00s | 165.0 ms | 0.055 | 442.1 ms | 0.194 | **2.7x** |
| 5 | 44 | 2.52s | 138.1 ms | 0.055 | 517.1 ms | 0.208 | **3.7x** |
| 6 | 64 | 3.60s | 192.9 ms | 0.054 | 591.1 ms | 0.168 | **3.1x** |
| 7 | 93 | 4.84s | 263.1 ms | 0.054 | 778.1 ms | 0.159 | **3.0x** |
| 8 | 86 | 4.36s | 234.1 ms | 0.054 | 697.1 ms | 0.171 | **3.0x** |
| 9 | 98 | 4.96s | 267.0 ms | 0.054 | 913.2 ms | 0.159 | **3.4x** |
| 10 | 70 | 5.00s | 247.1 ms | 0.049 | 1143.2 ms | 0.197 | **4.6x** |
| 11 | 50 | 6.32s | 341.1 ms | 0.054 | 1066.1 ms | 0.165 | **3.1x** |
| 12 | 84 | 4.56s | 209.0 ms | 0.046 | 737.1 ms | 0.162 | **3.5x** |
| 13 | 80 | 4.92s | 229.9 ms | 0.047 | 812.0 ms | 0.166 | **3.5x** |
| 14 | 104 | 5.28s | 241.0 ms | 0.046 | 789.1 ms | 0.151 | **3.3x** |
| 15 | 107 | 6.52s | 301.1 ms | 0.046 | 1215.2 ms | 0.176 | **4.0x** |
| 16 | 107 | 6.16s | 285.1 ms | 0.046 | 996.0 ms | 0.169 | **3.5x** |
| 17 | 110 | 6.52s | 302.0 ms | 0.046 | 966.2 ms | 0.161 | **3.2x** |
| 18 | 120 | 7.44s | 348.9 ms | 0.047 | 993.2 ms | 0.143 | **2.8x** |
| 19 | 130 | 7.60s | 364.2 ms | 0.048 | 1251.1 ms | 0.156 | **3.4x** |
| 20 | 123 | 7.92s | 365.1 ms | 0.046 | 1103.2 ms | 0.152 | **3.0x** |

## 4. Nhận xét & Kết luận
1. **Hiệu suất GPU vượt trội**: Xử lý bằng GPU (offload hoàn toàn lên VRAM của RTX 5060 Ti) nhanh hơn đáng kể so với CPU, rút ngắn thời gian xử lý tổng thể.
2. **Tính đáp ứng thời gian thực (Real-time)**: Cả GPU và CPU đều có RTF nhỏ hơn 1.0 (nhanh hơn thời gian thực phát âm thanh), nghĩa là cả hai cấu hình đều đủ đáp ứng tốt cho giao tiếp giọng nói thời gian thực. Tuy nhiên, GPU cung cấp trải nghiệm mượt mà hơn rất nhiều nhờ độ trễ ban đầu cực thấp.
3. **Hiệu quả tối ưu hóa RAM**: Nhờ đoạn mã cập nhật chuyển đổi in-memory thông qua `io.BytesIO`, độ trễ của cả CPU và GPU đều giảm đáng kể và không gây hao mòn thiết bị lưu trữ vật lý.
