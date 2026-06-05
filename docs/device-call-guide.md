# Hướng dẫn sử dụng plug-in gọi nhau giữa các thiết bị

## Tổng quan

Tính năng gọi điện của thiết bị cho phép liên lạc hai chiều giữa hai thiết bị được định cấu hình qua kênh thoại/dữ liệu. Khi thiết bị A gọi thiết bị B, hệ thống sẽ thực hiện quy trình sau:

```
设备A → 授权校验 → MQTT网关 → 设备B远程唤醒 → 建立连接 → 通话建立
```
## Điều kiện tiên quyết để sử dụng chức năng này
1. Bạn phải có ít nhất hai thiết bị và mỗi kiểu thiết bị phải là `ESP32-S3`, vì chỉ `ESP32-S3` hỗ trợ chức năng đánh thức từ xa.
2. Thiết bị của bạn phải có `两个麦克风`. Nhưng nếu thiết bị của bạn chỉ có `单个麦克风` và bạn chỉ muốn trải nghiệm chức năng này thì không sao, tuy nhiên sẽ có cảm giác lag rất mạnh.
3. Bạn phải sử dụng [Triển khai mô-đun đầy đủ](Deployment_all.md) cho dự án này vì bạn cần `智控台` để quản lý quyền và liên lạc của thiết bị.
4. Bạn phải cài đặt và định cấu hình [dịch vụ cổng MQTT](mqtt-gateway-integration.md) sau `2026年5月27日`. Nếu bạn đã triển khai dịch vụ cổng MQTT, vui lòng xác nhận rằng phiên bản mã nằm sau `2026年5月27日`.

Trên đây là những điều kiện khó khăn để sử dụng chức năng này, sẽ được giới thiệu chi tiết ở phần tiếp theo.

## Các bước cấu hình

### Bước 1: Bật chức năng sổ địa chỉ

1. Xác nhận rằng phiên bản bảng điều khiển thông minh của bạn là `0.9.4` trở lên.
2. Đăng nhập vào phần phụ trợ của bảng điều khiển thông minh
3. Nhập **Cấu hình chức năng hệ thống**
4. Kiểm tra **Sổ địa chỉ** trong danh sách chức năng bên trái
5. Nhấp vào **Lưu cấu hình** để xác nhận

### Bước 2: Định cấu hình quyền gọi giữa các thiết bị

1. Nhấp vào **Sổ liên hệ** trên menu trên cùng của bảng điều khiển thông minh
2. Trong tác nhân bên trái, chọn thiết bị A của bạn trong danh sách thiết bị (hỗ trợ tìm kiếm theo địa chỉ MAC hoặc tên nhận xét)
3. Trong bảng chi tiết ở bên phải, tìm cài đặt tiêu đề của thiết bị mục tiêu B, ví dụ **"小王"**
4. Chọn hộp kiểm **Quyền gọi** của thiết bị B
5. Nhấp vào **Lưu**

**Hướng dẫn ủy quyền hai chiều:** Nếu thiết bị A và thiết bị B cần liên lạc với nhau thì quyền của nhau phải được định cấu hình trên cả hai mặt của bảng điều khiển thông minh. Ví dụ:

- Kiểm tra thiết bị B trong cấu hình của thiết bị A → Thiết bị A có thể giao tiếp với thiết bị B
- Kiểm tra thiết bị A trong cấu hình của thiết bị B → Thiết bị B có thể giao tiếp với thiết bị A

### Bước 3: Thêm công cụ gọi điện vào cấu hình tổng đài viên

1. Nhấp vào **Quản lý đại lý** trên menu trên cùng của bảng điều khiển thông minh
2. Nhấp vào **Chỉnh sửa vai trò** trong tác nhân liên quan mà liên hệ thiết bị vừa được định cấu hình.
3. Trong bảng chi tiết ở bên phải, nhấp vào **Chỉnh sửa chức năng**
4. Kiểm tra công cụ **Device Call Device**
5. Nhấp vào **Lưu cấu hình** để xác nhận
6. Nhấp vào **Save Configuration** lần nữa ở bên ngoài, sau đó khởi động lại thiết bị

### Bước 4: Thêm công cụ đánh thức từ xa vào phía firmware

1. Thêm công cụ đánh thức từ xa MCP dựa trên mã [xiaozhi-esp32](https://github.com/78/xiaozhi-esp32), phiên bản hỗ trợ là 2.1.0 đến 2.2.6 (phiên bản ngày 29 tháng 5 năm 2026)
2. Thêm khai báo hàm đánh thức từ xa trong tệp application.h
    ```cpp
    void RemoteWakeup(const std::string& reason);
    ```
3. Thêm chức năng đánh thức từ xa trong file application.cc
    ```cpp
    void Application::RemoteWakeup(const std::string& Reason){
        nếu (!protocol_) {
            trở lại;
        }

        auto state = GetDeviceState();
        
        if (state == kDeviceStateIdle) {
            audio_service_.EncodeWakeWord();

if (!protocol_->IsAudioChannelOpened()) {
                SetDeviceState(kDeviceStateConnecting);
                if (!protocol_->OpenAudioChanel()) {
                    audio_service_.EnableWakeWordDetection(true);
                    trở lại;
                }
            }
            std::string Wake_word = lý do;
    #if CONFIG_USE_AFE_WAKE_WORD || CONFIG_USE_CUSTOM_WAKE_WORD
            // Mã hóa và gửi dữ liệu từ đánh thức đến máy chủ
            while (gói tự động = audio_service_.PopWakeWordPacket()) {
                giao thức_->SendAudio(std::move(packet));
            }
            // Đặt trạng thái trò chuyện để đánh thức từ được phát hiện
            giao thức_->SendWakeWordDetected(wake_word);
            SetListeningMode(aec_mode_ == kAecOff ? kListeningModeAutoStop : kListeningModeRealtime);
    #khác
            // Đặt cờ để phát âm thanh bật lên sau khi thay đổi trạng thái sang nghe
            // (PlaySound ở đây sẽ bị xóa bởi ResetDecode trong EnableVoiceProcessing)
            play_popup_on_listening_ = đúng;
            SetListeningMode(aec_mode_ == kAecOff ? kListeningModeAutoStop : kListeningModeRealtime);
    #endif
        } else if (state == kDeviceStateSpeaking) {
            AbortSpeaking(kAbortReasonWakeWordDetected);
            SetDeviceState(kDeviceStateIdle);
        } else if (state == kDeviceStateActivating) {
            SetDeviceState(kDeviceStateIdle);
        }
    }
    ```
4. 在mcp_server.cc文件中添加远程唤醒工具
    ```cpp
    AddUserOnlyTool("self.remote_wakeup", "Chức năng đánh thức từ xa với các tham số có thể định cấu hình",
        Danh sách thuộc tính({
            Thuộc tính("lý do", kPropertyTypeString, "Lý do đánh thức"),
        }),
        [cái này](const PropertyList& properties) -> ReturnValue {
            std::string Reason = Properties["reason"].value<std::string>();
            ESP_LOGI(TAG, "Lý do đánh thức=%s", Reason.c_str());
            auto& app = Ứng dụng::GetInstance();
            app.RemoteWakeup(lý do);
            trả về sự thật;
    ```
5. Làm theo [Hướng dẫn biên dịch và ghi chương trình cơ sở](firmware-build.md) để hoàn tất quá trình ghi chương trình cơ sở
6. Cho dù thiết bị của bạn là micrô đơn hay micrô kép, vui lòng kiểm tra để bật chức năng AEC trong quá trình biên dịch!
7. Cho dù thiết bị của bạn là micrô đơn hay micrô kép, vui lòng kiểm tra để bật chức năng AEC trong quá trình biên dịch!
8. Cho dù thiết bị của bạn là micrô đơn hay micrô kép, vui lòng kiểm tra để bật chức năng AEC trong quá trình biên dịch!

### Bước 5: Cấu hình dịch vụ cổng MQTT

1. Triển khai dịch vụ cổng MQTT, tham khảo [Tài liệu tích hợp cổng MQTT](mqtt-gateway-integration.md)
2. Nếu đã triển khai vui lòng xác nhận phiên bản của mã là phiên bản ngày 27/05/2026

## Mô tả luồng cuộc gọi

Chuẩn bị hai thiết bị, định cấu hình quyền liên lạc trên bảng điều khiển thông minh và thêm công cụ gọi điện vào tổng đài viên. Trong một trong những cuộc đối thoại của Xiaozhi, hãy nói với anh ấy: "Gọi XXX" và quan sát xem thiết bị B có phản hồi hay không.

## Câu hỏi thường gặp

### Hỏi: Máy B không phản hồi cuộc gọi?

- Kiểm tra xem thiết bị B có trực tuyến hay không (trạng thái thiết bị bảng điều khiển thông minh)
- Xác nhận firmware của thiết bị B đã tích hợp chính xác công cụ đánh thức từ xa
- Kiểm tra kết nối cổng MQTT có bình thường không
- Xác minh xem cấu hình quyền hai chiều đã hoàn tất chưa

### Hỏi: Nhắc "Không được phép gọi"?

- Xác nhận thiết bị A đã kiểm tra quyền gọi của thiết bị B trên bảng điều khiển thông minh
- Xác nhận cấu hình đã được lưu (không chỉ sửa đổi mà còn chưa lưu)

### Hỏi: Làm thế nào để xác nhận rằng chức năng sổ địa chỉ đã được bật?

- Nếu mục "Sổ địa chỉ" hiển thị trên menu trên cùng của bảng điều khiển thông minh, điều đó có nghĩa là nó đã được bật.

### Hỏi: Tôi bảo anh ấy gọi là "Trương Sơn", nhưng anh ấy luôn nhận ra là "Trương San", tôi phải làm sao?
- Bạn có thể kiểm tra tài liệu của dịch vụ asr bạn đang sử dụng để xác nhận xem nó có hỗ trợ nhận dạng từ nóng hay không.
- Nếu bạn đang sử dụng `FunASRServer`, bạn có thể thêm "Zhang Shan" vào `热词文件` trong vùng chứa, sau đó khởi động lại vùng chứa.
- Nếu bạn đang sử dụng dịch vụ của `火山引擎`, bạn có thể thêm `热词文件` vào `火山引擎的控制台`, sau đó quay lại `模型配置页面` của bảng điều khiển thông minh và định cấu hình `热词文件名称` trên `火山引擎的tts`.

