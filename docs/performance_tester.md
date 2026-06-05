# Hướng dẫn sử dụng các công cụ kiểm tra hiệu suất để nhận dạng giọng nói, mô hình ngôn ngữ lớn, tổng hợp giọng nói không phát trực tuyến, tổng hợp giọng nói phát trực tuyến và mô hình trực quan

1. Tạo thư mục dữ liệu trong thư mục main/xiaozhi-server
2. Tạo file .config.yaml trong thư mục data
3. Trong .data/config.yaml, viết các tham số nhận dạng giọng nói, mô hình ngôn ngữ lớn, tổng hợp giọng nói trực tuyến và mô hình trực quan
Ví dụ:
```
LLM:
  Trò chuyệnGLMLLM:
    # Xác định loại API LLM
    Kiểu: openai
    # glm-4-flash miễn phí nhưng bạn vẫn cần đăng ký và điền api_key
    # Bạn có thể tìm thấy khóa api của mình tại đây https://bigmodel.cn/usercenter/proj-mgmt/apikeys
    model_name: glm-4-flash
    url: https://open.bigmodel.cn/api/paas/v4/
    api_key: khóa web chat-glm của bạn

TTS:

VLLM:

ASR:
```
4.在main/xiaozhi-server目录下运行performance_tester.py: 
```
python performance_tester.py
```