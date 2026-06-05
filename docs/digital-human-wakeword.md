#Phương pháp khởi nghiệp số-con người

## Tổng quan

Trang thử nghiệm tích hợp chức năng đánh thức bằng giọng nói có độ chính xác cao dựa trên **Sherpa-ONNX**, hỗ trợ các từ đánh thức tùy chỉnh và phát hiện theo thời gian thực. Sử dụng mô hình phát hiện từ khóa nhẹ để cung cấp tốc độ phản hồi ở mức mili giây.

## Mô hình từ đánh thức

### Tải xuống mô hình (bắt buộc)

**Lưu ý quan trọng**: Dự án không chứa tệp mô hình và cần phải tải xuống cấu hình trước.

### Địa chỉ tải mẫu chính thức

- **Danh sách người mẫu chính thức**: <https://csukuangfj.github.io/sherpa/onnx/kws/pretrain_models/index.html>
- **Mẫu máy đề xuất**: `sherpa-onnx-kws-zipformer-wenetspeech-3.3M-2024-01-01`

### Các bước tải xuống và cấu hình

#### 1. Tải gói mô hình

``` bash
#Phương pháp 1: Tải xuống trực tiếp (khuyến nghị)
cd main/digital-human/wakeword_runtime/
wget https://github.com/k2-fsa/sherpa-onnx/releases/download/kws-models/sherpa-onnx-kws-zipformer-wenetspeech-3.3M-2024-01-01.tar.bz2

# Giải nén
tar xvf sherpa-onnx-kws-zipformer-wenetspeech-3.3M-2024-01-01.tar.bz2

#Phương pháp 2: Sử dụng ModelScope
cài đặt pip mô hình
trăn -c"
từ nhập modelscope snapshot_download
snapshot_download('pkufool/sherpa-onnx-kws-zipformer-wenetspeech-3.3M-2024-01-01', cache_dir='./models')
"
```

#### 2. Cấu hình file model

Gói mô hình chứa các tệp sau sau khi tải xuống:

```
sherpa-onnx-kws-zipformer-wenetspeech-3.3M-2024-01-01/
├── encoder-epoch-12-avg-2-chunk-16-left-64.int8.onnx    # 速度优先
├── encoder-epoch-12-avg-2-chunk-16-left-64.onnx
├── encoder-epoch-99-avg-1-chunk-16-left-64.int8.onnx    # 速度优先
├── encoder-epoch-99-avg-1-chunk-16-left-64.onnx         # 精度优先
├── decoder-epoch-12-avg-2-chunk-16-left-64.onnx
├── decoder-epoch-99-avg-1-chunk-16-left-64.onnx         # 精度优先
├── joiner-epoch-12-avg-2-chunk-16-left-64.int8.onnx     # 速度优先
├── joiner-epoch-12-avg-2-chunk-16-left-64.onnx
├── joiner-epoch-99-avg-1-chunk-16-left-64.int8.onnx     # 速度优先
├── joiner-epoch-99-avg-1-chunk-16-left-64.onnx          # 精度优先
├── tokens.txt                    # Token映射表（必需）
├── keywords_raw.txt              # 模型包里可能附带（可选，runtime 不依赖）
├── keywords.txt                  # 现成的
├── test_wavs/                    # 测试音频（可选）
├── configuration.json            # 模型元信息（可选）
└── README.md                     # 说明文档（可选）
```

#### 3. Chọn phương án cấu hình

**Tùy chọn 1: Độ chính xác là trên hết (được khuyến nghị)**

```bash
cd sherpa-onnx-kws-zipformer-wenetspeech-3.3M-2024-01-01

#Tạo thư mục mô hình
mkdir -p ../model

# Sao chép bộ ba mảnh ưu tiên độ chính xác epoch-99 fp32
cp bộ mã hóa-epoch-99-avg-1-chunk-16-left-64.onnx ../models/encoding.onnx
bộ giải mã cp-epoch-99-avg-1-chunk-16-left-64.onnx ../models/decoding.onnx
cp joiner-epoch-99-avg-1-chunk-16-left-64.onnx ../models/joiner.onnx

# Sao chép các tập tin hỗ trợ
cp token.txt ../models/tokens.txt
# keywords_raw.txt Nếu nó đi kèm với gói mô hình, bạn có thể tự giữ nó; thời gian chạy không phụ thuộc vào nó
```

**Phương án 2: Ưu tiên tốc độ**

```bash
cd sherpa-onnx-kws-zipformer-wenetspeech-3.3M-2024-01-01

#Tạo thư mục mô hình
mkdir -p ../model

# Bộ ba mảnh ưu tiên tốc độ sao chép epoch-99 int8
cp bộ mã hóa-epoch-99-avg-1-chunk-16-left-64.int8.onnx ../models/encoding.onnx
bộ giải mã cp-epoch-99-avg-1-chunk-16-left-64.onnx ../models/decoding.onnx
cp joiner-epoch-99-avg-1-chunk-16-left-64.int8.onnx ../models/joiner.onnx

# Sao chép các tập tin hỗ trợ
cp token.txt ../models/tokens.txt
```

**Ghi chú**:

- **Không trộn lẫn fp32 và int8**: ba tệp mô hình phải duy trì độ chính xác nhất quán
- **Ưu tiên epoch-99**: đào tạo đầy đủ hơn và độ chính xác cao hơn epoch-12
- **Hồ sơ cần thiết**: `encoder.onnx` + `decoder.onnx` + `joiner.onnx` + `tokens.txt` + `keywords.txt`

### Cấu trúc file mô hình cuối cùng

Sau khi cấu hình hoàn tất, tệp mô hình phải được đặt trong thư mục `wakeword_runtime/models/` và đường dẫn đầy đủ là `main/digital-human/wakeword_runtime/models/`:

```
wakeword_runtime/models/
├── encoder.onnx      # 编码器模型（重命名后）
├── decoder.onnx      # 解码器模型（重命名后）
├── joiner.onnx       # 连接器模型（重命名后）
├── tokens.txt        # 拼音 Token 映射表（228行版本）
├── keywords.txt      # 关键词配置文件（首次启动自动生成）
└── keywords_raw.txt  # 可选，runtime 不依赖
```

## Phương thức khởi động

Thực thi trong thư mục `main/digital-human`:

```bash
pip install -r wakeword_runtime/requirements.txt
python start.py
```

Địa chỉ mặc định sau khi khởi động:

- Địa chỉ trang: `http://127.0.0.1:8006/index.html`
- Địa chỉ cầu nối sự kiện: `ws://127.0.0.1:8006/wakeword-ws`
- Khám sức khỏe: `http://127.0.0.1:8006/health`

Phương pháp dừng:

- Nhấn `Ctrl+C` trong terminal đang chạy
- Dịch vụ trang tĩnh, cầu sự kiện và quá trình phát hiện từ đánh thức sẽ bị dừng cùng lúc

## Mô tả tệp cấu hình

Tệp cấu hình được đặt tại [main/digit-human/wakeword_runtime/config.json](../main/digital-human/wakeword_runtime/config.json).

Các mục cấu hình chính hiện tại:

```json
{
  "wakeword": {
    "enabled": true
  },
  "model_dir": "models",
  "audio": {
    "input_device": null,
    "sample_rate": 16000,
    "channels": 1
  },
  "detector": {
    "num_threads": 4,
    "provider": "cpu",
    "max_active_paths": 2,
    "keywords_score": 1.8,
    "keywords_threshold": 0.1,
    "num_trailing_blanks": 1,
    "cooldown_seconds": 1.5
  },
  "logging": {
    "level": "INFO",
    "dir": "logs",
    "file": "wakeword-runtime.log"
  }
}
```

Ý nghĩa của từng trường:

| Thông số | Mô tả |
| --- | --- |
| `wakeword.enabled` | Có bật tính năng phát hiện từ đánh thức cục bộ hay không |
| `model_dir` | Thư mục chứa mô hình và từ vựng |
| `audio.input_device` | Thiết bị đầu vào micrô, thiết bị mặc định của hệ thống được sử dụng theo mặc định |
| `audio.sample_rate` | Tốc độ lấy mẫu, mặc định `16000` |
| `audio.channels` | Số kênh, mặc định `1` |
| `detector.num_threads` | Số lượng chủ đề máy dò |
| `detector.provider` | Nhà cung cấp suy luận, hiện nay thường `cpu` |
| `detector.max_active_paths` | Số đường dẫn tìm kiếm |
| `detector.keywords_score` | Điểm nâng cao từ khóa |
| `detector.keywords_threshold` | Ngưỡng phát hiện |
| `detector.num_trailing_blanks` | Số lượng khoảng trống ở cuối |
| `detector.cooldown_seconds` | Thời gian làm mát kích hoạt liên tục |
| `logging.level` | Cấp độ nhật ký |
| `logging.dir` | Thư mục nhật ký |
| `logging.file` | Tên tệp nhật ký |

## Quy trình sử dụng được đề xuất

### Lần đầu sử dụng

1. Chuẩn bị file mô hình và `tokens.txt` trong thư mục `models/`
2. Xác nhận rằng `models/keywords.txt` tồn tại
3. Chạy `python start.py` trong thư mục `digital-human`
4. Mở trình duyệt `http://127.0.0.1:8006/index.html`
5. Vào trang cài đặt để kiểm tra cấu hình "Wake Word"

### Sửa đổi từ đánh thức

1. Mở cài đặt trang Digital Man
2. Chuyển sang tab “Wake Word”
3. Sửa đổi trạng thái kích hoạt hoặc danh sách từ đánh thức
4. Nhấp vào "Áp dụng Wake Word"
5. Quyết định có khởi động lại ngay lập tức theo lời nhắc hay không

### Tắt từ đánh thức

1. Thay đổi "Bật từ đánh thức cục bộ" thành tắt
2. Nhấp vào "Áp dụng Wake Word"
3. Nên khởi động lại ngay

Sau khi vô hiệu hóa:

- Cầu trang và sự kiện vẫn có sẵn
- Phát hiện từ đánh thức sẽ không tiếp tục chạy