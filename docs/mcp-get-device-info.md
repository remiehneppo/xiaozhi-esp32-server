#Phương pháp MCP lấy thông tin thiết bị như thế nào?

Hướng dẫn này sẽ hướng dẫn bạn cách lấy thông tin thiết bị bằng phương pháp MCP.

Bước 1: Tùy chỉnh tệp `agent-base-prompt.txt` của bạn

Sao chép nội dung của tệp `agent-base-prompt.txt` trong thư mục xiaozhi-server vào thư mục `data` của bạn và đổi tên thành `.agent-base-prompt.txt`.

Bước 2: Sửa đổi tệp `data/.agent-base-prompt.txt`, tìm thẻ `<context>` và thêm nội dung mã sau vào nội dung thẻ:
```
- **设备ID：** {{device_id}}
```

Sau khi việc bổ sung hoàn tất, nội dung của thẻ `<context>` trong tệp `data/.agent-base-prompt.txt` của bạn đại khái như sau:
```
<context>
【重要！以下信息已实时提供，无需调用工具查询，请直接使用：】
- **设备ID：** {{device_id}}
- **当前时间：** {{current_time}}
- **今天日期：** {{today_date}} ({{today_weekday}})
- **今天农历：** {{lunar_date}}
- **用户所在城市：** {{local_address}}
- **当地未来7天天气：** {{weather_info}}
</context>
```

Bước 3: Sửa đổi tệp `data/.config.yaml` và tìm cấu hình `agent-base-prompt`. Nội dung trước khi sửa đổi như sau:
```
prompt_template: agent-base-prompt.txt
```
Sửa đổi thành
```
prompt_template: data/.agent-base-prompt.txt
```

Bước 4: Khởi động lại dịch vụ máy chủ xiaozhi của bạn.

Bước 5: Thêm tham số có tên `device_id`, nhập `string` và mô tả `设备ID` vào phương thức mcp của bạn.

Bước 6: Đánh thức lại Xiaozhi và để anh ấy gọi phương thức mcp để xem liệu phương thức mcp của bạn có thể nhận được `设备ID` hay không.