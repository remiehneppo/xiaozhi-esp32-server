## Phiên bản di động bảng điều khiển thông minh (manager-mobile)
Thiết bị đầu cuối quản lý thiết bị di động đa năng dựa trên uni-app v3 + Vue 3 + Vite, hỗ trợ các chương trình nhỏ Ứng dụng (Android & iOS) và WeChat.

### Khả năng tương thích nền tảng

| H5 | iOS | Android | Chương trình nhỏ WeChat |
| -- | --- | ------- | ---------- |
| √ | √ | √ | √ |

Mẹo: Khả năng thích ứng của các thành phần UI khác nhau trên các nền tảng khác nhau hơi khác nhau, vui lòng tham khảo tài liệu thư viện thành phần tương ứng.

### Yêu cầu về môi trường phát triển
- Nút >= 18
- pnpm >= 7.30 (nên sử dụng `pnpm@10.x` khai báo trong project)
- Tùy chọn: HBuilderX (Gỡ lỗi/đóng gói ứng dụng), Công cụ dành cho nhà phát triển WeChat (applet WeChat)

### Bắt đầu nhanh
1) Cấu hình các biến môi trường
   - Sao chép `env/.env.example` vào `env/.env.development`
   - Sửa đổi các mục cấu hình theo điều kiện thực tế (đặc biệt `VITE_SERVER_BASEURL`, `VITE_UNI_APPID`, `VITE_WX_APPID`)

2) Cài đặt phụ thuộc

```bash
pnpm i
```

3) Phát triển địa phương (cập nhật nóng)
- h5: `pnpm dev:h5`, sau đó quan sát số cổng ip hiển thị trong nhật ký khởi động
- Chương trình WeChat mini: `pnpm dev:mp` hoặc `pnpm dev:mp-weixin`, sau đó sử dụng công cụ dành cho nhà phát triển WeChat để nhập `dist/dev/mp-weixin`
- Ứng dụng: Sử dụng HBuilderX để nhập `manager-mobile`, sau đó tham khảo hướng dẫn bên dưới để chạy nó

### Biến môi trường và cấu hình
Dự án sử dụng thư mục `env` tùy chỉnh để lưu trữ các tệp môi trường, được đặt tên theo thông số kỹ thuật của Vite: `.env.development`, `.env.production`, v.v.

Các biến chính (một phần):
- VITE_APP_TITLE: Tên ứng dụng (ghi `manifest.config.ts`)
- VITE_UNI_APPID: appid ứng dụng uni-app (App)
- VITE_WX_APPID: Ứng dụng ứng dụng WeChat (mp-weixin)
- VITE_FALLBACK_LOCALE: ngôn ngữ mặc định, chẳng hạn như `zh-Hans`
- VITE_SERVER_BASEURL: Địa chỉ cơ sở máy chủ (URL cơ sở yêu cầu HTTP)
- VITE_DELETE_CONSOLE: Có nên tháo console khi build hay không (`true`/`false`)
- VITE_SHOW_SOURCEMAP: có tạo sơ đồ nguồn hay không (mặc định tắt)
- VITE_LOGIN_URL: Đường dẫn trang đăng nhập cho bước nhảy không đăng nhập (được sử dụng bởi bộ chặn định tuyến)

Ví dụ (`env/.env.development`):
```env
VITE_APP_TITLE=Xiao Zhi
VITE_FALLBACK_LOCALE=zh-Hans
VITE_UNI_APPID=
VITE_WX_APPID=

VITE_SERVER_BASEURL=http://localhost:8080

VITE_DELETE_CONSOLE=false
VITE_SHOW_SOURCEMAP=false
VITE_LOGIN_URL=/pages/login/index
```

Mô tả:
- `manifest.config.ts` sẽ đọc tiêu đề, ứng dụng, ngôn ngữ và các cấu hình khác từ `env`.

### Lưu ý quan trọng
⚠️ **Các mục cấu hình phải được sửa đổi trước khi triển khai:**

1. **Cấu hình ID ứng dụng**
   - `VITE_UNI_APPID`: Bạn cần tạo một ứng dụng và lấy AppID trong [Trung tâm nhà phát triển DCloud](https://dev.dcloud.net.cn/)
   - `VITE_WX_APPID`: Bạn cần đăng ký chương trình mini trên [Nền tảng công cộng WeChat](https://mp.weixin.qq.com/) và lấy AppID

2. **Địa chỉ máy chủ**
   - `VITE_SERVER_BASEURL`: Thay đổi địa chỉ máy chủ thực của bạn

3. **Thông tin ứng tuyển**
   - `VITE_APP_TITLE`: Thay đổi tên ứng dụng của bạn
   - Cập nhật tài nguyên biểu tượng như `src/static/logo.png`

4. **Cấu hình khác**
   - Kiểm tra thông tin cấu hình ứng dụng trong `manifest.config.ts`
   - Sửa đổi cấu hình thanh tab trong `src/layouts/fg-tabbar/tabbarList.ts` nếu cần

###Hướng dẫn thao tác chi tiết

#### 1. Nhận AppID đơn ứng dụng
![Tạo ID ứng dụng](../../docs/images/manager-mobile/生成appid.png)
- Sao chép AppID đã tạo vào biến môi trường `VITE_UNI_APPID`

#### 2. Các bước chạy cục bộ
![Chạy cục bộ](../../docs/images/manager-mobile/本地运行.png)

**Gỡ lỗi cục bộ ứng dụng:**
1. Sử dụng HBuilderX để nhập thư mục `manager-mobile`
2. Xác định lại dự án
3. Kết nối với điện thoại di động hoặc sử dụng trình giả lập để gỡ lỗi thiết bị thực

**Giải quyết vấn đề xác định dự án:**
![Xác định lại các mục](../../docs/images/manager-mobile/重新识别项目.png)

Nếu HBuilderX không nhận dạng chính xác loại dự án:
- Nhấp chuột phải vào thư mục gốc của dự án và chọn "Xác định lại loại dự án"
- Đảm bảo dự án được công nhận là dự án "uni-app"

### Định tuyến và xác thực
- Plug-in chặn tuyến đường `routeInterceptor` được đăng ký trong `src/main.ts`.
- Chặn danh sách đen: Chỉ xác minh các trang được định cấu hình để yêu cầu đăng nhập (nguồn `getNeedLoginPages` của `@/utils`).
- Phán quyết đăng nhập: Dựa trên thông tin người dùng (`pinia` đến `useUserStore`), nếu bạn chưa đăng nhập, bạn sẽ được chuyển hướng đến `VITE_LOGIN_URL` với các thông số để chuyển hướng trở lại trang gốc.

### Yêu cầu mạng
- Dựa trên `alova` + `@alova/adapter-uniapp`, tạo các thể hiện trong `src/http/request/alova.ts`.
- `baseURL` đọc cấu hình môi trường (`getEnvBaseUrl`) và có thể tự động chuyển đổi tên miền thông qua `method.config.meta.domain`.
- Xác thực: Theo mặc định, tiêu đề `Authorization` được chèn từ `token` (`uni.getStorageSync('token')`) cục bộ. Nếu thiếu, thông tin đăng nhập sẽ được chuyển hướng.
- Phản hồi: Xử lý thống nhất các lỗi HTTP `statusCode !== 200` và lỗi `code !== 0` nghiệp vụ; `401` sẽ xóa mã thông báo và chuyển sang đăng nhập.

### Xây dựng và phát hành

**Chương trình nhỏ WeChat:**
1. Đảm bảo `VITE_WX_APPID` được định cấu hình đúng
2. Chạy `pnpm build:mp`, sản phẩm nằm trong `dist/build/mp-weixin`
3. Sử dụng công cụ dành cho nhà phát triển WeChat để nhập thư mục dự án và tải mã lên
4. Gửi để xem xét trên nền tảng công cộng WeChat

**Android & iOS App：**

#### 3. Các bước đóng gói và phân phối ứng dụng

**Bước 1: Chuẩn bị đóng gói**
![Bước đóng gói và phân phối 1](../../docs/images/manager-mobile/打包发行步骤1.png)

1. Đảm bảo `VITE_UNI_APPID` được định cấu hình đúng
2. Chạy `pnpm build:app`, sản phẩm nằm trong `dist/build/app`
3. Sử dụng HBuilderX để nhập thư mục dự án
4. Nhấp vào "Phát hành" → "Bao bì đám mây ứng dụng gốc" trong HBuilderX

**Bước 2: Cấu hình các thông số đóng gói**
![Bước đóng gói và phân phối 2](../../docs/images/manager-mobile/打包发行步骤2.png)

1. **Biểu tượng ứng dụng và images khởi động**: Tải lên biểu tượng ứng dụng và images trang khởi động
2. **Số phiên bản ứng dụng**: Đặt số phiên bản và tên phiên bản
3. **Chứng nhận chữ ký**:
   - Android: Tải lên tệp chứng chỉ kho khóa
   - iOS: Định cấu hình chứng chỉ và hồ sơ nhà phát triển
4. **Cấu hình tên gói**: Đặt tên gói ứng dụng (ID gói)
5. **Loại bao bì**: Chọn gói thử nghiệm hoặc gói chính thức
6. Nhấp vào "Gói" để bắt đầu quá trình đóng gói trên đám mây

**Xuất bản lên App Store:**
- **Android**: Tải tệp APK đã tạo lên các thị trường ứng dụng Android lớn
- **iOS**: Tải tệp IPA đã tạo lên App Store thông qua App Store Connect (yêu cầu tài khoản nhà phát triển Apple)

### Quy ước và Kỹ thuật
- Trang và hợp đồng phụ: được tạo thống nhất bởi `@uni-helper/vite-plugin-uni-pages` và `pages.config.ts`; thanh tab được định cấu hình trong `src/layouts/fg-tabbar/tabbarList.ts`.
- Tự động nhập linh kiện và hook: xem `unplugin-auto-import` và `@uni-helper/vite-plugin-uni-components` trong `vite.config.ts`.
- Tạo kiểu: sử dụng UnoCSS với `src/style/index.scss`.
- Quản lý trạng thái: `pinia` + `pinia-plugin-persistedstate`.
- Thông số mã: tích hợp sẵn `eslint`, `husky`, `lint-staged`, được định dạng tự động trước khi gửi (`lint-staged`).

### Các tập lệnh thường dùng
``` bash
# phát triển
pnpm dev:mp # Tương đương với dev:mp-weixin

# xây dựng
pnpm build:mp # Tương đương với build:mp-weixin

# Khác
kiểm tra kiểu pnpm
pnpm lint && pnpm lint:sửa
```

### License
MIT
