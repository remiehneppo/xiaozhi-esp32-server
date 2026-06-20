-- Sửa đổi định nghĩa yêu cầu giao diện TTS tùy chỉnh
update `ai_model_provider` set `fields` =
'[{"key":"url","label":"Địa chỉ dịch vụ","type":"string"},{"key":"method","label":"Phương thức yêu cầu","type":"string"},{"key":"params","label":"Tham số yêu cầu","type":"dict","dict_name":"params"},{"key":"headers","label":"Tiêu đề yêu cầu","type":"dict","dict_name":"headers"},{"key":"format","label":"Định dạng âm thanh","type":"string"},{"key":"output_dir","label":"Thư mục đầu ra","type":"string"}]'
where `id` = 'SYSTEM_TTS_custom';

-- Sửa đổi mô tả cấu hình TTS tùy chỉnh
UPDATE `ai_model_config` SET
`doc_link` = NULL,
`remark` = 'Mô tả cấu hình TTS tùy chỉnh:
1. tùy chỉnhTTSDịch vụ giao diện，Tham số yêu cầuCó thể tùy chỉnh，Có thể truy cập nhiềuTTSdịch vụ
2. Lấy ví dụ về KokoroTTS triển khai cục bộ
3. Nếu chỉ chạy trên cpu:docker run -p 8880:8880 ghcr.io/remsky/kokoro-fastapi-cpu:latest
4. Nếu chỉ chạy trên gpu:docker run --gpus all -p 8880:8880 ghcr.io/remsky/kokoro-fastapi-gpu:latest
Mô tả cấu hình:
1. trongparamsCấu hình trung bìnhTham số yêu cầu,sử dụngJSONđịnh dạng
   Ví dụ KokoroTTS:{ "input": "{prompt_text}", "speed": 1, "voice": "zm_yunxi", "stream": true, "download_format": "mp3", "response_format": "mp3", "return_download_link": true }
2. trongheadersCấu hình trung bìnhTiêu đề yêu cầu
3. Đặt lợi nhuậnĐịnh dạng âm thanh' WHERE `id` = 'TTS_CustomTTS';