# Hướng dẫn tích hợp thành phần bộ nhớ PowerMem

## Giới thiệu

[PowerMem](https://www.powermem.ai/) là thành phần bộ nhớ Tác nhân có nguồn mở bởi OceanBase. Nó thực hiện tóm tắt bộ nhớ và truy xuất thông minh thông qua LLM cục bộ, cung cấp các chức năng quản lý bộ nhớ hiệu quả cho các tác nhân AI.

Mô tả chi phí: Bản thân PowerMem là nguồn mở và miễn phí, chi phí thực tế phụ thuộc vào LLM và cơ sở dữ liệu bạn chọn:
- Sử dụng SQLite + LLM miễn phí (chẳng hạn như glm-4-flash) = **hoàn toàn miễn phí**
- Sử dụng LLM đám mây hoặc cơ sở dữ liệu đám mây = tính phí theo dịch vụ tương ứng

> 💡 **Mẹo về hiệu suất tốt nhất**: PowerMem có thể được sử dụng với OceanBase để đạt được hiệu suất tối đa. SQLite chỉ được khuyến nghị sử dụng khi tài nguyên không đủ.

- **GitHub**: https://github.com/oceanbase/powermem
- **Trang web chính thức**: https://www.powermem.ai/
- **Ví dụ sử dụng**: https://github.com/oceanbase/powermem/tree/main/examples

## Đặc trưng

- **Tóm tắt cục bộ**: Tóm tắt và trích xuất bộ nhớ cục bộ thông qua LLM
- **Chân dung người dùng**: Tự động trích xuất thông tin người dùng (tên, nghề nghiệp, sở thích, v.v.) thông qua `UserMemory` và cập nhật liên tục chân dung người dùng
- **Quên thông minh**: Dựa trên đường cong quên Ebbinghaus, tự động "quên" thông tin tiếng ồn lỗi thời
- **Nhiều phụ trợ lưu trữ**: Hỗ trợ OceanBase (được khuyến nghị, hiệu suất tốt nhất), SeekDB (được khuyến nghị, lưu trữ ứng dụng AI tích hợp), PostgreSQL, SQLite (thay thế nhẹ)
- **Hỗ trợ nhiều LLM**: Tongyi Qianwen, Zhipu (glm-4-flash free), OpenAI, v.v.
- **Truy xuất thông minh**: Khả năng truy xuất ngữ nghĩa dựa trên tìm kiếm vectơ
- **Triển khai riêng tư**: Hỗ trợ đầy đủ việc triển khai tư nhân hóa tại địa phương
- **Hoạt động không đồng bộ**: Quản lý bộ nhớ không đồng bộ hiệu quả

## Cài đặt

PowerMem đã được thêm vào phần phụ thuộc của dự án, nếu bạn cần cài đặt thủ công:

```bash
pip install powermem
```

## Hướng dẫn cấu hình

###Cấu hình cơ bản

Định cấu hình PowerMem trong `config.yaml`:

```yaml
selected_module:
  Memory: powermem

Bộ nhớ:
  quyền lực:
    Kiểu: powermem
    # Có bật chức năng chân dung người dùng hay không
    # Hỗ trợ chân dung người dùng: Oceanbase, seekdb, sqlite (powermem 0.3.0+)
    Enable_user_profile: đúng
    
    # ========== Cấu hình LLM ===========
    ừm:
      nhà cung cấp: openai # Tùy chọn: qwen, openai, zhipu, v.v.
      cấu hình:
        api_key: khóa API LLM của bạn
        mô hình: qwen-plus
        # openai_base_url: https://api.openai.com/v1 # Tùy chọn, địa chỉ dịch vụ tùy chỉnh
    
    # ========== Cấu hình nhúng ===========
    trình nhúng:
      nhà cung cấp: openai # Tùy chọn: qwen, openai, v.v.
      cấu hình:
        api_key: Khóa API mô hình được nhúng của bạn
        mô hình: nhúng văn bản-v4
        openai_base_url: https://dashscope.aliyuncs.com/compix-mode/v1
        # embedding_dims: 1024 # Kích thước vectơ, cần được cấu hình nếu không phải là 1536
    
    # ========== Cấu hình cơ sở dữ liệu ==========
    vector_store:
      nhà cung cấp: sqlite # Tùy chọn: Oceanbase (được khuyến nghị), seekdb (được khuyến nghị), postgres, sqlite (nhẹ)
      config: {} # SQLite không yêu cầu cấu hình bổ sung
```

###Giải thích chi tiết các thông số cấu hình

#### Cấu hình LLM

| Thông số | Mô tả | Giá trị tùy chọn |
|------|------|--------|
| `llm.provider` | Nhà cung cấp LLM | `qwen`, `openai`, `zhipu`, v.v. |
| `llm.config.api_key` | Khóa API | - |
| `llm.config.model` | Tên mẫu | Dựa trên lựa chọn nhà cung cấp |
| `llm.config.openai_base_url` | Địa chỉ dịch vụ tùy chỉnh (tùy chọn) | - |

#### Cấu hình nhúng

| Thông số | Mô tả | Giá trị tùy chọn |
|------|------|--------|
| `embedder.provider` | Nhà cung cấp mô hình nhúng | `qwen`, `openai`, v.v. |
| `embedder.config.api_key` | Khóa API | - |
| `embedder.config.model` | Tên mẫu | Dựa trên lựa chọn nhà cung cấp |
| `embedder.config.openai_base_url` | Địa chỉ dịch vụ tùy chỉnh (tùy chọn) | - |

#### Cấu hình cơ sở dữ liệu

| Thông số | Mô tả | Giá trị tùy chọn |
|------|------|--------|
| `vector_store.provider` | Loại phụ trợ lưu trữ | `oceanbase`(khuyên dùng), `seekdb`(khuyên dùng), `postgres`, `sqlite`(nhẹ) |
| `vector_store.config` | Cấu hình kết nối cơ sở dữ liệu | Đặt theo nhà cung cấp |

### Mô tả chế độ bộ nhớ

PowerMem hỗ trợ hai chế độ bộ nhớ:

| Chế độ | Cấu hình | Tính năng | Yêu cầu lưu trữ |
|------|------|------|----------|
| **Bộ nhớ bình thường** | `enable_user_profile: false` | Lưu trữ và truy xuất bộ nhớ hộp thoại | Hỗ trợ tất cả cơ sở dữ liệu |
| **Chân dung người dùng** | `enable_user_profile: true` | Bộ nhớ + tự động trích xuất chân dung người dùng | Oceanbase, seekdb, sqlite |

> ** **Ghi chú phiên bản**: PowerMem phiên bản 0.3.0+, chức năng chân dung người dùng hỗ trợ ba chương trình phụ trợ lưu trữ: OceanBase, SeekDB và SQLite.

### Sử dụng Tongyi Qianwen (được khuyến nghị)

1. Truy cập [Nền tảng Bailian đám mây của Alibaba](https://bailian.console.aliyun.com/) để đăng ký tài khoản
2. Lấy khóa API trên trang [Quản lý khóa API](https://bailian.console.aliyun.com/?apiKey=1#/api-key)
3. Cấu hình như sau:

```yaml
Memory:
  powermem:
    type: powermem
    enable_user_profile: true
    llm:
      provider: qwen
      config:
        api_key: sk-xxxxxxxxxxxxxxxx
        model: qwen-plus
    embedder:
      provider: openai
      config:
        api_key: sk-xxxxxxxxxxxxxxxx
        model: text-embedding-v4
        openai_base_url: https://dashscope.aliyuncs.com/compatible-mode/v1
    vector_store:
      provider: sqlite
      config: {}
```

### Sử dụng Zhipu LLM miễn phí (gói hoàn toàn miễn phí)

Zhipu cung cấp mô hình glm-4-flash miễn phí, có thể được sử dụng hoàn toàn miễn phí với SQLite:

1. Truy cập [Nền tảng mở Zhipu AI](https://bigmodel.cn/) để đăng ký tài khoản
2. Lấy khóa API trên trang [Khóa API](https://bigmodel.cn/usercenter/proj-mgmt/apikeys)
3. Cấu hình như sau:

```yaml
Memory:
  powermem:
    type: powermem
    enable_user_profile: true
    llm:
      provider: openai  # 使用 openai 兼容模式
      config:
        api_key: xxxxxxxxxxxxxxxx.xxxxxxxxxxxxxxxx
        model: glm-4-flash
        openai_base_url: https://open.bigmodel.cn/api/paas/v4/
    embedder:
      provider: openai
      config:
        api_key: xxxxxxxxxxxxxxxx.xxxxxxxxxxxxxxxx
        model: embedding-3
        openai_base_url: https://open.bigmodel.cn/api/paas/v4/
    vector_store:
      provider: sqlite
      config: {}
```

### Sử dụng OpenAI

```yaml
Memory:
  powermem:
    type: powermem
    enable_user_profile: true
    llm:
      provider: openai
      config:
        api_key: sk-xxxxxxxxxxxxxxxx
        model: gpt-4o-mini
        openai_base_url: https://api.openai.com/v1
    embedder:
      provider: openai
      config:
        api_key: sk-xxxxxxxxxxxxxxxx
        model: text-embedding-3-small
        openai_base_url: https://api.openai.com/v1
    vector_store:
      provider: sqlite
      config: {}
```

### Sử dụng OceanBase (giải pháp hiệu suất tốt nhất)

OceanBase là đối tác tốt nhất của PowerMem để đạt được hiệu suất tối đa:

1. Triển khai cơ sở dữ liệu OceanBase (hỗ trợ triển khai cục bộ nguồn mở hoặc sử dụng dịch vụ đám mây)
   - Triển khai mã nguồn mở: https://github.com/oceanbase/oceanbase
   - Dịch vụ đám mây: https://www.oceanbase.com/
2. Cấu hình như sau:

```yaml
Memory:
  powermem:
    type: powermem
    enable_user_profile: true
    llm:
      provider: qwen
      config:
        api_key: sk-xxxxxxxxxxxxxxxx
        model: qwen-plus
    embedder:
      provider: openai
      config:
        api_key: sk-xxxxxxxxxxxxxxxx
        model: text-embedding-v4
        openai_base_url: https://dashscope.aliyuncs.com/compatible-mode/v1
    vector_store:
      provider: oceanbase
      config:
        host: 127.0.0.1
        port: 2881
        user: root@test
        password: your_password
        db_name: powermem
        collection_name: memories  # 默认值
        embedding_model_dims: 1536  # 嵌入向量维度，必需参数
```

## Cách ly bộ nhớ thiết bị

PowerMem sẽ tự động sử dụng ID thiết bị (`device_id`) làm `user_id` để cách ly bộ nhớ. Điều này có nghĩa là:

-Mỗi thiết bị có không gian bộ nhớ độc lập riêng
- Cách ly bộ nhớ hoàn toàn giữa các thiết bị khác nhau
- Nhiều cuộc hội thoại trên cùng một thiết bị có thể chia sẻ bối cảnh bộ nhớ

## Chân dung người dùng (UserMemory)

PowerMem cung cấp lớp `UserMemory`, lớp này có thể tự động trích xuất thông tin hồ sơ người dùng từ các cuộc hội thoại.

> ** **Ghi chú phiên bản**: PowerMem phiên bản 0.3.0+, chức năng chân dung người dùng hỗ trợ ba chương trình phụ trợ lưu trữ: OceanBase, SeekDB và SQLite.

### Bật chân dung người dùng

Kích hoạt nó bằng cách cài đặt `enable_user_profile: true` trong cấu hình:

```yaml
Memory:
  powermem:
    type: powermem
    enable_user_profile: true  # 启用用户画像
    llm:
      provider: qwen
      config:
        api_key: sk-xxxxxxxxxxxxxxxx
        model: qwen-plus
    embedder:
      provider: openai
      config:
        api_key: sk-xxxxxxxxxxxxxxxx
        model: text-embedding-v4
        openai_base_url: https://dashscope.aliyuncs.com/compatible-mode/v1
    vector_store:
      provider: sqlite  # 用户画像支持: oceanbase、seekdb、sqlite
      config: {}
```

### Khả năng chụp chân dung người dùng

| Khả năng | Mô tả |
|------|------|
| **Khai thác thông tin** | Tự động trích xuất tên, tuổi, nghề nghiệp, sở thích, v.v. từ các cuộc hội thoại |
| **Cập nhật liên tục** | Liên tục cải thiện chân dung người dùng khi cuộc trò chuyện diễn ra |
| **Truy xuất chân dung** | Kết hợp chân dung người dùng với tìm kiếm bộ nhớ để cải thiện mức độ liên quan của việc truy xuất |
| **Quên thông minh** | Dựa trên đường cong quên Ebbinghaus, hạ thấp thông tin lỗi thời |

### Nguyên tắc làm việc

Sau khi kích hoạt chân dung người dùng, Xiaozhi sẽ tự động quay lại:
1. **Chân dung người dùng**: thông tin cơ bản, sở thích và sở thích của người dùng, v.v.
2. **Ký ức liên quan**: Ký ức lịch sử liên quan đến cuộc trò chuyện hiện tại

> ✅ **Ghi chú phiên bản**: PowerMem phiên bản 0.3.0+, chức năng chân dung người dùng hỗ trợ ba chương trình phụ trợ lưu trữ: OceanBase, SeekDB và SQLite.

## So sánh với các thành phần bộ nhớ khác

| Tính năng | PowerMem | mem0ai | mem_local_short |
|------|----------|--------|-------------------|
| Phương pháp làm việc | Tóm tắt địa phương | Giao diện đám mây | Tóm tắt địa phương |
| Vị trí lưu trữ | DB cục bộ/đám mây | Đám mây | YAML địa phương |
| Chi phí | Phụ thuộc vào LLM và DB | 1000 lần/tháng miễn phí | Hoàn toàn miễn phí |
| Tìm kiếm thông minh | ✅ Tìm kiếm vectơ | ✅ Tìm kiếm vectơ | ❌ Hoàn trả đầy đủ |
| Chân dung người dùng | ✅ Bộ nhớ người dùng | ❌ | ❌ |
| Quên thông minh | ✅ Đường cong quên lãng | ❌ | ❌ |
| Triển khai riêng tư | ✅ Hỗ trợ | ❌ Chỉ trên đám mây | ✅ Hỗ trợ |
| Hỗ trợ cơ sở dữ liệu | OceanBase(được khuyến nghị)/SeekDB/PostgreSQL/SQLite | - | Tệp YAML |

## Câu hỏi thường gặp

### 1. Lỗi khóa API

Nếu bạn gặp lỗi `API key is required`, hãy kiểm tra:
- `llm_api_key` và `embedding_api_key` được điền đúng chưa?
- Khóa API có hợp lệ không

### 2. Model không tồn tại

Nếu bạn gặp lỗi mô hình không tồn tại, vui lòng xác nhận:
- Tên `llm_model` và `embedding_model` có đúng không?
- Dịch vụ mẫu tương ứng đã được kích hoạt chưa

### 3. Hết thời gian kết nối

Nếu xảy ra thời gian chờ kết nối, bạn có thể thử:
- Kiểm tra kết nối mạng
- Nếu sử dụng proxy, hãy định cấu hình `llm_base_url` và `embedding_base_url`

## Kiểm tra xác minh

Bạn có thể kiểm tra xem PowerMem có hoạt động bình thường trong môi trường ảo hay không:

``` bash
# Kích hoạt môi trường ảo
nguồn .venv/bin/kích hoạt

# Kiểm tra nhập PowerMem
python -c "from powermem import AsyncMemory; print('PowerMem đã nhập thành công')"

# Kiểm tra nhập UserMemory (chức năng chân dung người dùng)
python -c "from powermem import UserMemory; print('UserMemory đã nhập thành công')"
```

## Nhiều tài nguyên hơn

- [Tài liệu chính thức của PowerMem](https://www.powermem.ai/)
- [Kho lưu trữ PowerMem GitHub](https://github.com/oceanbase/powermem)
- [Ví dụ về cách sử dụng PowerMem](https://github.com/oceanbase/powermem/tree/main/examples)
- [Trang web chính thức của OceanBase](https://www.oceanbase.com/)
- [OceanBase GitHub](https://github.com/oceanbase/oceanbase)
- [SeekDB GitHub](https://github.com/oceanbase/seekdb) (cơ sở dữ liệu tìm kiếm gốc AI)
- [Nền tảng Bailian đám mây của Alibaba](https://bailian.console.aliyun.com/)

