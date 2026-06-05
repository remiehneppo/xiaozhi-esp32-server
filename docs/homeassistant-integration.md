# Xiaozhi ESP32-Hướng dẫn tích hợp máy chủ mã nguồn mở và HomeAssistant

[TOC]

-----

## Giới thiệu

Tài liệu này sẽ hướng dẫn bạn cách tích hợp thiết bị ESP32 với HomeAssistant.

## Điều kiện tiên quyết

- `HomeAssistant` đã được cài đặt và cấu hình
- Model tôi chọn lần này là: ChatGLM miễn phí, hỗ trợ gọi hàm functioncall

## Các thao tác trước khi bắt đầu (cần thiết)

### 1. Lấy thông tin địa chỉ mạng của HA

Vui lòng truy cập địa chỉ mạng của Trợ lý gia đình của bạn. Ví dụ: địa chỉ HA của tôi là 192.168.4.7 và cổng mặc định là 8123. Sau đó mở nó lên trên trình duyệt

```
http://192.168.4.7:8123
```

> Truy vấn thủ công địa chỉ IP của HA** (chỉ khi Xiaozhi ESP32-server và HA được triển khai trên cùng một thiết bị mạng [chẳng hạn như cùng một wifi])**:
>
> 1. Nhập Trợ lý gia đình (giao diện người dùng).
>
> 2. Nhấp vào **Cài đặt** → **Hệ thống** → **Mạng** ở góc dưới bên trái.
>
> 3. Trượt xuống vùng `Home Assistant 网址(Home Assistant website)` phía dưới. Trong `本地网络(local network)`, nhấp vào nút `眼睛` để xem địa chỉ IP hiện được sử dụng (chẳng hạn như `192.168.1.10`) và giao diện mạng. Bấm vào `复制连接(copy link)` để sao chép trực tiếp.
>
> ![image-20250504051716417](images/image-ha-integration-01.png)

Hoặc bạn đã thiết lập địa chỉ OAuth của Home Assistant để có thể truy cập trực tiếp. Bạn cũng có thể truy cập nó trực tiếp trong trình duyệt.

```
http://homeassistant.local:8123
```

### 2. Đăng nhập vào `Home Assistant` để lấy key phát triển

Đăng nhập vào `HomeAssistant`, nhấp vào `左下角头像 -> 个人`, chuyển sang thanh điều hướng `安全`, vuốt xuống dưới cùng `长期访问令牌` để tạo api_key, sau đó sao chép và lưu nó. Các phương pháp tiếp theo cần sử dụng khóa api này và nó chỉ xuất hiện một lần (mẹo nhỏ: Bạn có thể lưu images mã QR đã tạo và có thể quét mã QR và trích xuất khóa api sau).

## Cách 1: Chức năng gọi HA do cộng đồng Xiaozhi chung tay xây dựng

### Mô tả chức năng

- Nếu sau này bạn cần thêm thiết bị mới, phương pháp này yêu cầu bạn khởi động lại thủ công `xiaozhi-esp32-server服务端` để cập nhật thông tin thiết bị** (Quan trọng**).

- Bạn cần đảm bảo rằng bạn đã tích hợp `Xiaomi Home` trong HomeAssistant và nhập thiết bị Mijia vào `HomeAssistant`.

- Bạn cần đảm bảo rằng `xiaozhi-esp32-server智控台` có thể sử dụng bình thường.

- `xiaozhi-esp32-server智控台` và `HomeAssistant` của tôi được triển khai trên một cổng khác trên cùng một máy, phiên bản là `0.3.10`

  ```
  http://192.168.4.7:8002
  ```


###Các bước cấu hình

#### 1. Đăng nhập vào `HomeAssistant` để sắp xếp danh sách các thiết bị cần điều khiển.

Đăng nhập vào `HomeAssistant`, nhấp vào `左下角的设置`, sau đó nhập `设备与服务`, sau đó nhấp vào `实体` ở trên cùng.

Sau đó tìm kiếm công tắc điều khiển liên quan của bạn trong thực thể. Sau khi có kết quả, bạn nhấn vào một trong các kết quả trong danh sách sẽ xuất hiện giao diện chuyển đổi.

Trong giao diện chuyển đổi, chúng ta thử nhấn vào công tắc để xem quá trình phát triển có bật/tắt khi nhấn vào hay không. Nếu nó hoạt động, có nghĩa là mạng được kết nối bình thường.

Sau đó tìm nút cài đặt trên bảng công tắc. Sau khi nhấp vào nó, bạn có thể xem `实体标识符` của nút chuyển này.

Chúng tôi mở một sổ ghi chú và sắp xếp một phần dữ liệu theo định dạng sau:

Vị trí + dấu phẩy + tên thiết bị + dấu phẩy + `实体标识符` + dấu chấm phẩy

Ví dụ mình đang ở công ty, mình có một chiếc đèn đồ chơi, mã định danh của nó là switch.cuco_cn_460494544_cp1_on_p_2_1 thì viết đoạn dữ liệu này

```
公司,玩具灯,switch.cuco_cn_460494544_cp1_on_p_2_1;
```

Tất nhiên, cuối cùng tôi có thể phải vận hành hai đèn. Kết quả cuối cùng của tôi là:

```
公司,玩具灯,switch.cuco_cn_460494544_cp1_on_p_2_1;
公司,台灯,switch.iot_cn_831898993_socn1_on_p_2_1;
```

Ký tự này, mà chúng tôi gọi là "ký tự danh sách thiết bị", cần được lưu lại và sẽ hữu ích sau này.

#### 2. Đăng nhập `智控台`

![image-20250504051716417](images/image-ha-integration-06.png)

Sử dụng tài khoản quản trị viên để đăng nhập vào `智控台`. Trong `智能体管理`, tìm đại lý của bạn và nhấp vào `配置角色`.

Đặt nhận dạng ý định thành `外挂的大模型意图识别` hoặc `大模型自主函数调用`. Lúc này bạn sẽ thấy `编辑功能` ở bên phải. Nhấp vào nút `编辑功能` và hộp `功能管理` sẽ bật lên.

Trong ô `功能管理`, bạn cần đánh dấu vào `HomeAssistant设备状态查询` và `HomeAssistant设备状态修改`.

Sau khi kiểm tra, hãy nhấp vào `HomeAssistant设备状态查询` trong `已选功能`, sau đó định cấu hình các ký tự địa chỉ, khóa và danh sách thiết bị `HomeAssistant` của bạn trong `参数配置`.

Sau khi chỉnh sửa xong nhấn vào `保存配置`. Lúc này ô `功能管理` sẽ bị ẩn đi. Sau đó, bạn có thể nhấp để lưu cấu hình tác nhân.

Sau khi lưu thành công, hoạt động của thiết bị có thể được đánh thức.

#### 3. Đánh thức máy để điều khiển

Hãy thử nói với ESP32, "Bật đèn XXX"

## Cách 2: Xiaozhi sử dụng trợ lý giọng nói của Home Assistant làm công cụ LLM

### Mô tả chức năng

- Phương pháp này có một thiếu sót nghiêm trọng - **Phương pháp này không thể sử dụng chức năng plug-in function_call của hệ sinh thái nguồn mở của Xiaozhi**, vì việc sử dụng Home Assistant làm công cụ LLM của Xiaozhi sẽ chuyển khả năng nhận dạng ý định sang Home Assistant. Nhưng **phương pháp này cho phép bạn trải nghiệm các chức năng vận hành Home Assistant gốc và khả năng trò chuyện của Xiaozhi vẫn không thay đổi**. Nếu thực sự quan tâm, bạn có thể sử dụng [Phương pháp 3](##方法3：使用Home Assistant的MCP服务（推荐）), cũng được Home Assistant hỗ trợ, để trải nghiệm tối đa các chức năng của Home Assistant.

###Các bước cấu hình:

#### 1. Cấu hình trợ lý giọng nói mô hình lớn của Home Assistant.

**Bạn cần định cấu hình trước trợ lý giọng nói Home Assistant hoặc công cụ mô hình lớn. **

#### 2. Lấy Agent ID của trợ lý ngôn ngữ Home Assistant.

1. Vào trang Home Assistant. Nhấp vào `开发者助手` ở bên trái.
2. Trong `开发者助手` đã mở, hãy nhấp vào tab `动作` (như minh họa trong thao tác 1). Trong thanh tùy chọn `动作` trên trang, tìm hoặc nhập `conversation.process（对话-处理）` và chọn `对话（conversation）: 处理` (như minh họa trong thao tác 2).

![image-20250504043539343](images/image-ha-integration-02.png)

3. Chọn tùy chọn `代理(agent)` trên trang và chọn tên của trợ lý giọng nói mà bạn đã định cấu hình ở bước 1 trong `对话代理(conversation agent)` sẽ chuyển sang đèn sáng liên tục. Như trong hình, cái tôi cấu hình ở đây là `ZhipuAi` và chọn nó.

![image-20250504043854760](images/image-ha-integration-03.png)

4. Sau khi chọn, nhấp vào `进入YAML模式` ở phía dưới bên trái của biểu mẫu.

![image-20250504043951126](images/image-ha-integration-04.png)

5. Sao chép giá trị của id tác nhân. Ví dụ: của tôi là `01JP2DYMBDF7F4ZA2DMCF2AGX2` trong hình (chỉ mang tính chất tham khảo).

![image-20250504044046466](images/image-ha-integration-05.png)

6. Chuyển sang tệp `config.yaml` của máy chủ nguồn mở Xiaozhi `xiaozhi-esp32-server`, tìm Home Assistant trong cấu hình LLM và đặt địa chỉ mạng, khóa API và Agent_id của Home Assistant mà bạn vừa truy vấn.
7. Sửa đổi thuộc tính `selected_module` trong tệp `config.yaml` từ `LLM` thành `HomeAssistant` và `Intent` thành `nointent`.
8. Khởi động lại máy chủ nguồn mở Xiaozhi `xiaozhi-esp32-server` để sử dụng bình thường.

## Cách 3: Sử dụng dịch vụ MCP của Home Assistant (khuyến nghị)

### Mô tả chức năng

- Bạn cần tích hợp và cài đặt trước tính năng tích hợp HA trong Home Assistant - [Model Context Protocol Server](https://www.home-assistant.io/integrations/mcp_server/).

- Phương pháp này và phương pháp 2 đều là giải pháp do HA chính thức cung cấp. Khác với phương pháp 2, thông thường bạn có thể sử dụng plug-in đồng xây dựng nguồn mở của máy chủ nguồn mở Xiaozhi `xiaozhi-esp32-server` và bạn được phép sử dụng bất kỳ mô hình LLM lớn nào hỗ trợ chức năng function_call theo ý muốn.

###Các bước cấu hình

#### 1. Cài đặt tích hợp dịch vụ MCP của Home Assistant.

Tích hợp trang web chính thức——[Máy chủ Giao thức Ngữ cảnh Mô hình](https://www.home-assistant.io/integrations/mcp_server/). .

Hoặc làm theo các bước hướng dẫn dưới đây.

> - Đi tới **[Cài đặt > Thiết bị & Dịch vụ.](https://my.home-assistant.io/redirect/integrations)** trên trang Trợ lý chính.
>
> - Ở góc dưới bên phải, chọn nút **[Thêm tích hợp](https://my.home-assistant.io/redirect/config_flow_start?domain=mcp_server)**.
>
> - Chọn Máy chủ Giao thức Ngữ cảnh Mô hình từ danh sách.
>
> - Làm theo hướng dẫn trên màn hình để hoàn tất thiết lập.

#### 2. Cấu hình thông tin cấu hình MCP máy chủ mã nguồn mở Xiaozhi


Nhập thư mục `data` và tìm tệp `.mcp_server_settings.json`.

Nếu không có tệp `.mcp_server_settings.json` trong thư mục `data` của bạn,
- Hãy copy file `mcp_server_settings.json` trong thư mục gốc của thư mục `xiaozhi-server` vào thư mục `data` và đổi tên thành `.mcp_server_settings.json`
- Hoặc [Tải file này](https://github.com/xinnan-tech/xiaozhi-esp32-server/blob/main/main/xiaozhi-server/mcp_server_settings.json), tải về thư mục `data` rồi đổi tên thành `.mcp_server_settings.json`


Sửa đổi nội dung phần này trong `"mcpServers"`:

```json
"Home Assistant": {
      "command": "mcp-proxy",
      "args": [
        "http://YOUR_HA_HOST/mcp_server/sse"
      ],
      "env": {
        "API_ACCESS_TOKEN": "YOUR_API_ACCESS_TOKEN"
      }
},
```

Để ý:

1. **Cấu hình thay thế:**
   - Thay thế `YOUR_HA_HOST` trong `args` bằng địa chỉ dịch vụ HA của bạn. Nếu địa chỉ dịch vụ của bạn đã chứa từ https/http (chẳng hạn như `http://192.168.1.101:8123`), bạn chỉ cần điền `192.168.1.101:8123`.
   - Thay thế `YOUR_API_ACCESS_TOKEN` trong `API_ACCESS_TOKEN` trong `env` bằng khóa api khóa phát triển mà bạn đã lấy được trước đó.
2. **Nếu bạn thêm cấu hình trong dấu ngoặc của `"mcpServers"` và không có cấu hình `mcpServers` mới, bạn cần xóa dấu phẩy cuối cùng `,`**, nếu không quá trình phân tích cú pháp có thể không thành công.

**Hiệu quả cuối cùng như sau (tham khảo như sau)**:

```json
 "mcpServers": {
    "Home Assistant": {
      "command": "mcp-proxy",
      "args": [
        "http://192.168.1.101:8123/mcp_server/sse"
      ],
      "env": {
        "API_ACCESS_TOKEN": "abcd.efghi.jkl"
      }
    }
  }
```

#### 3. Cấu hình cấu hình hệ thống máy chủ mã nguồn mở Xiaozhi

1. **Chọn bất kỳ mô hình LLM lớn nào hỗ trợ function_call làm trợ lý trò chuyện LLM của Xiaozhi (nhưng không chọn Home Assistant làm công cụ LLM)**. Mô hình tôi chọn lần này là: ChatGLM miễn phí, hỗ trợ gọi hàm, gọi hàm nhưng đôi khi gọi không ổn định. Nếu bạn đang theo đuổi sự ổn định, bạn nên đặt LLM thành: DoubaoLLM và model_name cụ thể được sử dụng là: doubao-1-5-pro-32k-250115.

2. Chuyển sang tệp `config.yaml` của máy chủ nguồn mở Xiaozhi `xiaozhi-esp32-server`, đặt cấu hình mô hình lớn LLM của bạn và điều chỉnh `Intent` của cấu hình `selected_module` thành `function_call`.

3. Khởi động lại máy chủ mã nguồn mở Xiaozhi `xiaozhi-esp32-server` để sử dụng bình thường.