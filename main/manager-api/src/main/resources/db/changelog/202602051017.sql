-- Đã thêm nhà cung cấp mô hình bộ nhớ powermem
INSERT INTO `ai_model_provider` (`id`, `model_type`, `provider_code`, `name`, `fields`, `sort`, `creator`, `create_date`, `updater`, `update_date`)
VALUES ('SYSTEM_Memory_powermem', 'Memory', 'powermem', 'PowerMemký ức', '[
  {"key":"enable_user_profile","label":"Bật chân dung người dùng","type":"boolean"},
  {"key":"llm_provider","label":"LLMnhà cung cấp","type":"string"},
  {"key":"llm_api_key","label":"LLM APIchìa khóa","type":"string"},
  {"key":"llm_model","label":"LLMngười mẫu","type":"string"},
  {"key":"openai_base_url","label":"OpenAIKhái niệm cơ bảnURL","type":"string"},
  {"key":"embedding_provider","label":"Embeddingnhà cung cấp","type":"string"},
  {"key":"embedding_api_key","label":"Embedding APIchìa khóa","type":"string"},
  {"key":"embedding_model","label":"Embeddingngười mẫu","type":"string"},
  {"key":"embedding_openai_base_url","label":"Embedding OpenAIKhái niệm cơ bảnURL","type":"string"},
  {"key":"embedding_dims","label":"EmbeddingKích thước","type":"integer"},
  {"key":"vector_store","label":"Cấu hình lưu trữ vectơ(JSON)","type":"dict"}
]', 4, 1, NOW(), 1, NOW());

-- Đã thêm cấu hình mô hình bộ nhớ PowerMem
INSERT INTO `ai_model_config` VALUES (
  'Memory_powermem',
  'Memory',
  'powermem',
  'PowerMemký ức',
  0,
  1,
  '{\"type\": \"powermem\", \"enable_user_profile\": true, \"llm_provider\": \"openai\", \"llm_api_key\": \"của bạnLLM APIchìa khóa\", \"llm_model\": \"qwen-plus\", \"openai_base_url\": \"\", \"embedding_provider\": \"openai\", \"embedding_api_key\": \"mô hình nhúng của bạnAPIchìa khóa\", \"embedding_model\": \"text-embedding-v4\", \"embedding_openai_base_url\": \"https://api.openai.com/v1\", \"embedding_dims\": \"\", \"vector_store\": {\"provider\": \"sqlite\", \"config\": {}}}',
  NULL,
  NULL,
  4,
  NULL,
  NULL,
  NULL,
  NULL
);


-- Hướng dẫn cấu hình bộ nhớ PowerMem
UPDATE `ai_model_config` SET
`doc_link` = 'https://github.com/oceanbase/powermem',
`remark` = 'PowerMemCóOceanBasenguồn mởagentthành phần bộ nhớ，qua địa phươngLLMThực hiện một bản tóm tắt bộ nhớ
GitHub: https://github.com/oceanbase/powermem
Trang web chính thức: https://www.powermem.ai/
Ví dụ sử dụng: https://github.com/oceanbase/powermem/tree/main/examples

【Mô tả phí】
PowerMembản thân nó miễn phí，Chi phí thực tế phụ thuộc vào lựa chọnLLMvà cơ sở dữ liệu：
- sử dụngsqlite + miễn phíLLM(Chẳng hạn nhưglm-4-flash) = hoàn toàn miễn phí
- Sử dụng đám mâyLLMhoặc cơ sở dữ liệu đám mây = Tính phí theo dịch vụ tương ứng

【enable_user_profile】Chức năng chân dung người dùng
- false: Sử dụng chế độ bộ nhớ bình thường(AsyncMemory)
- true: Sử dụng chế độ chân dung người dùng(UserMemory)，Tự động trích xuất thông tin người dùng
- Hỗ trợ chức năng chân dung người dùng: oceanbase、seekdb、sqlite (powermem 0.3.0+)

【llm】LLMCấu hình - Được sử dụng để tóm tắt bộ nhớ và trích xuất chân dung người dùng
  provider: LLMnhà cung cấp，Giá trị tùy chọn：
    - qwen: Tongyi Qianwen (https://bailian.console.aliyun.com/?apiKey=1#/api-key)
    - openai: OpenAIGiao diện tương thích
    - zhipu: Phổ trí tuệAI (https://bigmodel.cn/usercenter/proj-mgmt/apikeys) - Nên sử dụng miễn phíglm-4-flash
  config: LLMThông số cấu hình
    - api_key: APIchìa khóa (Bắt buộc)
    - model: Tên mẫu，Chẳng hạn như qwen-plus、glm-4-flash Đợi đã
    - openai_base_url: Địa chỉ dịch vụ tùy chỉnh (Tùy chọn)，Chẳng hạn như https://api.openai.com/v1
  Ví dụ：
    {"provider": "zhipu", "config": {"api_key": "your_key", "model": "glm-4-flash"}}
    {"provider": "qwen", "config": {"api_key": "your_key", "model": "qwen-plus"}}

【embedder】EmbeddingCấu hình - Được sử dụng để vector hóa nội dung bộ nhớ
  provider: Nhà cung cấp mô hình nhúng，Giá trị tùy chọn：
    - qwen: Tongyi Qianwen
    - openai: OpenAIGiao diện tương thích
  config: EmbeddingThông số cấu hình
    - api_key: APIchìa khóa (Bắt buộc)
    - model: Tên mẫu，Chẳng hạn như text-embedding-v4、text-embedding-3-small Đợi đã
    - openai_base_url: Địa chỉ dịch vụ tùy chỉnh (Tùy chọn)
    - embedding_dims: kích thước vector (Tùy chọn)，Không1536Yêu cầu cấu hình
  Ví dụ：
    {"provider": "openai", "config": {"api_key": "your_key", "model": "text-embedding-v4", "openai_base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1"}}

【vector_store】Cấu hình lưu trữ cơ sở dữ liệu - Bộ nhớ được sử dụng để lưu trữ vector hóa
  provider: Loại cơ sở dữ liệu，Giá trị tùy chọn：
    - sqlite: Cơ sở dữ liệu cục bộ nhẹ (Đề xuất cho người mới bắt đầu，Không cần cấu hình bổ sung)
    - oceanbase: OceanBasecơ sở dữ liệu (Khuyến nghị sử dụng cho sản xuất，Hiệu suất tốt nhất)
    - seekdb: SeekDB (Được đề xuất，AILưu trữ ứng dụng tích hợp)
    - postgres: PostgreSQLcơ sở dữ liệu

  SQLiteCấu hình (Không cần cấu hình bổ sung):
    {"provider": "sqlite", "config": {}}

  OceanBaseVí dụ cấu hình:
    {"provider": "oceanbase", "config": {
      "host": "127.0.0.1",
      "port": 2881,
      "user": "root@test",
      "password": "your_password",
      "db_name": "powermem",
      "collection_name": "memories",
      "embedding_model_dims": 1024
    }}
  Lưu ý：
    - collection_name: Tên bảng mặc định，Nếu có lỗi khi tạo thứ nguyên, vui lòng xóa bảng hoặc đổi tên.
    - embedding_model_dims: nhúng kích thước vector，cần phảiembedderKích thước mô hình phù hợp
      Ví dụ, phổ trí tuệ：embedding-2Kích thước là1024，embedding-3Kích thước là2048

【Kết hợp cấu hình đề xuất】
1. Gói hoàn toàn miễn phí：
   - LLM: zhipu + glm-4-flash (miễn phí)
   - Embedder: Tongyi Qianwen text-embedding-v4
   - Database: sqlite

2. Kế hoạch môi trường sản xuất：
   - LLM: qwen-plus hoặc các mô hình kinh doanh khác
   - Embedder: text-embedding-v4
   - Database: oceanbase hoặc seekdb
'
WHERE `id` = 'Memory_powermem';
