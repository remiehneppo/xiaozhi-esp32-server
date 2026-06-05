#Yêu cầu thư viện

Dự án hiện tại sử dụng Alova làm thư viện yêu cầu HTTP duy nhất:

## Cách sử dụng

- **Alova HTTP**: đường dẫn (src/http/request/alova.ts)
- **Mã ví dụ**: src/api/foo-alova.ts và src/api/foo.ts
- **Tài liệu API**: https://alova.js.org/

## Hướng dẫn cấu hình

Phiên bản Alova được cấu hình:
- Xác thực và làm mới mã thông báo tự động
- Thống nhất xử lý lỗi và nhắc nhở
- Hỗ trợ chuyển đổi tên miền động
- Trình chặn yêu cầu/phản hồi tích hợp

## Ví dụ sử dụng

```typescript
import { http } from '@/http/request/alova'

// NHẬN yêu cầu
http.Get<ResponseType>('/api/path', {
  thông số: { id: 1 },
  tiêu đề: { 'Custom-Header': 'value' },
  meta: { toast: false } // Đóng dấu nhắc lỗi
})

// ĐĂNG yêu cầu
http.Post<ResponseType>('/api/path', dữ liệu, {
  thông số: { truy vấn: 'param' },
  tiêu đề: { 'Content-Type': 'application/json' }
})
```