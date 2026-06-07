[![Banners](docs/images/banner1.png)](https://github.com/xinnan-tech/xiaozhi-esp32-server)

<h1 align="center"> Dịch vụ phụ trợ Xiaozhi xiaozhi-esp32-server</h1>

<p align="center">
Dự án này dựa trên lý thuyết và công nghệ về sự cộng sinh trí tuệ giữa con người và máy móc để phát triển hệ thống phần cứng và phần mềm đầu cuối thông minh <br/> là một dự án phần cứng thông minh nguồn mở
<a href="https://github.com/78/xiaozhi-esp32">xiaozhi-esp32</a> cung cấp dịch vụ phụ trợ <br/>
Theo <a href="https://ccnphfhqs21z.feishu.cn/wiki/M0XiwldO9iJwHikpXD5cEx71nKh"> Giao thức truyền thông Xiaozhi </a> sử dụng Python, Java và Vue để triển khai <br/>
Hỗ trợ giao thức MQTT+UDP, giao thức WebSocket, điểm truy cập MCP, nhận dạng giọng nói, cơ sở kiến ​​thức
</p>

<p align="center">
<a href="./docs/FAQ.md">Câu hỏi thường gặp</a>
· <a href="https://github.com/xinnan-tech/xiaozhi-esp32-server/issues">Câu hỏi phản hồi</a>
· <a href="./docs/Deployment.md">Tài liệu triển khai</a>
· <a href="https://github.com/xinnan-tech/xiaozhi-esp32-server/releases">Nhật ký cập nhật</a>
</p>

<p align="center">
<a href="./README.md"><img alt="Bản giới thiệu tiếng Trung giản thể" src="https://img.shields.io/badge/zh--CN-DBEDFA"></a>
  <a href="./docs/readme/README_en.md"><img alt="README in English" src="https://img.shields.io/badge/English-DFE0E5"></a>
  <a href="./docs/readme/README_vi.md"><img alt="Tiếng Việt" src="https://img.shields.io/badge/Tiếng Việt-DFE0E5"></a>
  <a href="./docs/readme/README_de.md"><img alt="Deutsch" src="https://img.shields.io/badge/Deutsch-DFE0E5"></a>
  <a href="./docs/readme/README_pt_BR.md"><img alt="Português (Brasil)" src="https://img.shields.io/badge/Português (Brasil)-DFE0E5"></a>
  <a href="https://github.com/xinnan-tech/xiaozhi-esp32-server/releases">
    <img alt="GitHub Contributors" src="https://img.shields.io/github/v/release/xinnan-tech/xiaozhi-esp32-server?logo=docker" />
  </a>
  <a href="https://github.com/xinnan-tech/xiaozhi-esp32-server/blob/main/LICENSE">
    <img alt="GitHub pull requests" src="https://img.shields.io/badge/license-MIT-white?labelColor=black" />
  </a>
  <a href="https://github.com/xinnan-tech/xiaozhi-esp32-server">
    <img alt="stars" src="https://img.shields.io/github/stars/xinnan-tech/xiaozhi-esp32-server?color=ffcb47&labelColor=black" />
  </a>
</p>

<p align="center">
Spearheaded by Professor Siyuan Liu's Team (South China University of Technology)
</br>
Nghiên cứu và phát triển do nhóm của Giáo sư Liu Siyuan (Đại học Công nghệ Nam Trung Quốc) dẫn đầu
</br>
<img src="./docs/images/hnlg.jpg" alt="Đại học Công nghệ Nam Trung Quốc" width="50%">
</p>

---

## Người áp dụng 👥

Dự án này cần được sử dụng với thiết bị phần cứng ESP32. Nếu bạn đã mua phần cứng liên quan đến ESP32 và kết nối thành công dịch vụ phụ trợ do Xiage triển khai và muốn tự xây dựng phần cứng của riêng mình
`xiaozhi-esp32` dịch vụ phụ trợ thì dự án này là sự lựa chọn hoàn hảo cho bạn.

Bạn muốn xem hiệu quả? Hãy click vào video 🎥

<table>
  <tr>
    <td>
      <a href="https://www.bilibili.com/video/BV1FMFyejExX" target="_blank">
        <picture>
<img alt="Cảm nhận tốc độ phản hồi" src="docs/images/demo9.png" />
      </a>
    </td>
    <td>
      <a href="https://www.bilibili.com/video/BV1vchQzaEse" target="_blank">
        <picture>
<img alt="Mẹo tối ưu tốc độ" src="docs/images/demo6.png" />
      </a>
    </td>
    <td>
      <a href="https://www.bilibili.com/video/BV1WEcxzFEAT" target="_blank">
        <picture>
<img alt="Xiaozhi digital human hỗ trợ đánh thức bằng giọng nói" src="docs/images/demo8.png" />
      </a>
    </td>
    <td>
      <a href="https://www.bilibili.com/video/BV1CKVz6UEuB" target="_blank">
        <picture>
<img alt="Thiết bị gọi thiết bị, gọi điện" src="docs/images/demo0.png" />
      </a>
    </td>
    <td>
      <a href="https://www.bilibili.com/video/BV1C1tCzUEZh" target="_blank">
        <picture>
<img alt="Kịch bản y tế phức tạp" src="docs/images/demo1.png" />
      </a>
    </td>
  </tr>
  <tr>
    <td>
      <a href="https://www.bilibili.com/video/BV1VC96Y5EMH" target="_blank">
        <picture>
<img alt="Phát nhạc, tra thời tiết, đọc tin tức" src="docs/images/demo7.png" />
      </a>
    </td>
    <td>
      <a href="https://www.bilibili.com/video/BV12J7WzBEaH" target="_blank">
        <picture>
<img alt="Ngắt lời theo thời gian thực" src="docs/images/demo10.png" />
      </a>
    </td>
    <td>
      <a href="https://www.bilibili.com/video/BV1Co76z7EvK" target="_blank">
        <picture>
<img alt="Chụp ảnh nhận diện vật thể" src="docs/images/demo12.png" />
      </a>
    </td>
    <td>
      <a href="https://www.bilibili.com/video/BV1pNXWYGEx1" target="_blank">
        <picture>
<img alt="Điều khiển bật tắt thiết bị gia dụng" src="docs/images/demo5.png" />
      </a>
    </td>
    <td>
      <a href="https://www.bilibili.com/video/BV1TJ7WzzEo6" target="_blank">
        <picture>
<img alt="Tác vụ đa lệnh" src="docs/images/demo11.png" />
      </a>
    </td>
  </tr>
  <tr>
    <td>
      <a href="https://www.bilibili.com/video/BV1ZQKUzYExM" target="_blank">
        <picture>
<img alt="Điểm truy cập MCP" src="docs/images/demo13.png" />
      </a>
    </td>
    <td>
      <a href="https://www.bilibili.com/video/BV1zUW5zJEkq" target="_blank">
        <picture>
<img alt="Phát lệnh MQTT" src="docs/images/demo4.png" />
      </a>
    </td>
    <td>
      <a href="https://www.bilibili.com/video/BV1Exu3zqEDe" target="_blank">
        <picture>
<img alt="Nhận dạng giọng nói" src="docs/images/demo14.png" />
      </a>
    </td>
    <td>
      <a href="https://www.bilibili.com/video/BV1CDKWemEU6" target="_blank">
        <picture>
<img alt="Tùy chỉnh giọng nói" src="docs/images/demo2.png" />
      </a>
    </td>
    <td>
      <a href="https://www.bilibili.com/video/BV12yA2egEaC" target="_blank">
        <picture>
<img alt="Giao tiếp bằng tiếng Quảng Đông" src="docs/images/demo3.png" />
      </a>
    </td>
  </tr>
</table>

---

## CẢNH BÁO ⚠️

1. Dự án này là phần mềm nguồn mở. Không có quan hệ đối tác thương mại giữa phần mềm này và bất kỳ nhà cung cấp dịch vụ API bên thứ ba nào (bao gồm nhưng không giới hạn ở nhận dạng giọng nói, mô hình lớn, tổng hợp giọng nói và các nền tảng khác) và không có bất kỳ hình thức đảm bảo nào được cung cấp cho chất lượng dịch vụ hoặc bảo mật tài chính.
Người dùng nên ưu tiên cho các nhà cung cấp dịch vụ có giấy phép kinh doanh có liên quan và đọc kỹ các thỏa thuận dịch vụ cũng như chính sách quyền riêng tư của họ. Phần mềm này không lưu trữ bất kỳ khóa tài khoản nào, không tham gia vào dòng vốn và không chịu rủi ro mất tiền nạp.

2. Các chức năng của dự án này chưa hoàn hảo và chưa vượt qua đánh giá an ninh mạng. Vui lòng không sử dụng nó trong môi trường sản xuất. Nếu bạn triển khai và nghiên cứu dự án này trong môi trường mạng công cộng, hãy đảm bảo thực hiện các biện pháp bảo vệ cần thiết.

---

## Tài liệu triển khai

![Banners](docs/images/banner2.png)

Dự án này cung cấp hai phương pháp triển khai, vui lòng chọn theo nhu cầu cụ thể của bạn:

#### 🚀 Lựa chọn phương thức triển khai
| Phương pháp triển khai | Tính năng | Các tình huống áp dụng | Tài liệu triển khai | Yêu cầu cấu hình | Video hướng dẫn |
|---------|------|---------|---------|---------|---------|
| **Cài đặt đơn giản** | Đối thoại thông minh, quản lý một tác nhân | Môi trường cấu hình thấp, dữ liệu được lưu trữ trong file cấu hình, không cần cơ sở dữ liệu | [①Phiên bản Docker](./docs/Deployment.md#%E6%96%B9%E5%BC%8F%E4%B8%80docker%E5%8F%AA%E8%BF%90%E8%A1%8Cserver) / [②Triển khai mã nguồn](./docs/Deployment.md#%E6%96%B9%E5%BC%8F%E4%BA%8C%E6%9C%AC%E5%9C%B0%E6%BA%90%E7%A0%81%E5%8F%AA%E8%BF%90%E8%A1%8Cserver)| Dùng `FunASR` thì cần 2 nhân 4G, dùng full API thì cần 2 nhân 2G | - |
| **Cài đặt mô-đun đầy đủ** | Đối thoại thông minh, quản lý nhiều người dùng, quản lý nhiều tác nhân, vận hành giao diện bảng điều khiển thông minh | Trải nghiệm chức năng hoàn chỉnh, dữ liệu được lưu trữ trong cơ sở dữ liệu |[①Phiên bản Docker](./docs/Deployment_all.md#%E6%96%B9%E5%BC%8F%E4%B8%80docker%E8%BF%90%E8%A1%8C%E5%85%A8%E6%A8%A1%E5%9D%97) / [②Triển khai mã nguồn](./docs/Deployment_all.md#%E6%96%B9%E5%BC%8F%E4%BA%8C%E6%9C%AC%E5%9C%B0%E6%BA%90%E7%A0%81%E8%BF%90%E8%A1%8C%E5%85%A8%E6%A8%A1%E5%9D%97) / [③Hướng dẫn cập nhật tự động triển khai mã nguồn](./docs/dev-ops-integration.md) | Nếu bạn sử dụng `FunASR` thì cần 4 lõi 8G, nếu sử dụng API đầy đủ thì cần 2 lõi 4G| [Video hướng dẫn khởi động mã nguồn cục bộ](https://www.bilibili.com/video/BV1wBJhz4Ewe) |

Để biết các câu hỏi thường gặp và hướng dẫn liên quan, vui lòng tham khảo [liên kết này](./docs/FAQ.md)

> 💡 Mẹo: Sau đây là nền tảng thử nghiệm sau khi triển khai theo code mới nhất. Nếu cần, bạn có thể ghi bài kiểm tra. Đồng thời là 6. Dữ liệu sẽ bị xóa mỗi ngày.

```
Địa chỉ bảng điều khiển thông minh: https://2662r3426b.vicp.fun
Bảng điều khiển thông minh (bản h5): https://2662r3426b.vicp.fun/h5/index.html

Công cụ kiểm tra dịch vụ: https://2662r3426b.vicp.fun/test/
Địa chỉ giao diện OTA: https://2662r3426b.vicp.fun/xiaozhi/ota/
Địa chỉ giao diện WebSocket: wss://2662r3426b.vicp.fun/xiaozhi/v1/
```

#### 🚩 Hướng dẫn cấu hình và khuyến nghị
> [!Note]
> Dự án này cung cấp hai tùy chọn cấu hình:
> 
> 1. Cấu hình `nhập môn miễn phí`: phù hợp cho nhu cầu sử dụng cá nhân tại nhà, tất cả các thành phần đều là gói miễn phí, không cần thanh toán thêm.
> 
> 2. `cấu hình phát trực tuyến`: Thích hợp cho các buổi trình diễn, đào tạo, nhiều kịch bản đồng thời, v.v., sử dụng công nghệ xử lý streaming, phản hồi nhanh hơn và trải nghiệm tốt hơn.
> 
> Bắt đầu từ phiên bản `0.5.2`, dự án hỗ trợ cấu hình phát trực tuyến. So với các phiên bản trước, tốc độ phản hồi tăng lên khoảng `2.5 giây`, cải thiện đáng kể trải nghiệm người dùng.

| Tên mô-đun | Thiết lập cấp đầu vào miễn phí | Cấu hình phát trực tuyến |
|:---:|:---:|:---:|
| ASR (Nhận dạng giọng nói) | FunASR (Địa phương) | 👍XunfeiStreamASR (Truyền phát iFlytek) |
| LLM (Mô hình lớn) | glm-4-flash (Zhipu) | 👍qwen-flash (Alibaba Bailian) |
| VLLM (Mô hình trực quan lớn) | glm-4v-flash (Phổ trí tuệ) | 👍qwen3.5-flash (Alibaba Bailian) |
| TTS (tổng hợp giọng nói) | EdgeTTS (Microsoft) | 👍HuoshanDoubleStreamTTS (dòng núi lửa) |
| Ý định (nhận dạng ý định) | function_call (gọi hàm) | function_call (gọi hàm) |
| Bộ nhớ (chức năng bộ nhớ) | mem_local_short (bộ nhớ ngắn hạn cục bộ) | mem_local_short (bộ nhớ ngắn hạn cục bộ) |

Nếu bạn lo ngại về mức tiêu thụ thời gian của từng thành phần, vui lòng kiểm tra [báo cáo kiểm tra hiệu suất thành phần của Xiaozhi](https://github.com/xinnan-tech/xiaozhi-performance-research) và bạn thực sự có thể kiểm tra nó trong môi trường của mình theo các phương pháp kiểm tra trong báo cáo.

#### 🔧 Công cụ kiểm tra
Dự án này cung cấp các công cụ kiểm tra sau để giúp bạn xác minh hệ thống của mình và chọn mô hình phù hợp:

| Tên công cụ | Vị trí | Cách sử dụng | Mô tả chức năng |
|:---:|:---|:---:|:---:|
| Công cụ kiểm tra tương tác âm thanh | `main/digital-human/index.html` | Truy cập `http://127.0.0.1:8006/index.html` sau khi thực thi `python start.py` trong `main/digital-human` | Kiểm tra chức năng phát và nhận âm thanh cũng như xác minh xem quá trình xử lý âm thanh ở phía Python có bình thường hay không |
| Công cụ kiểm tra phản hồi mô hình | `main/xiaozhi-server/performance_tester.py` | Thực thi `python performance_tester.py` | Kiểm tra tốc độ phản hồi của ba mô-đun cốt lõi là ASR (nhận dạng giọng nói), LLM (mô hình lớn), VLLM (mô hình trực quan) và TTS (tổng hợp giọng nói) |

> 💡 Mẹo: Khi kiểm tra tốc độ của model, chỉ những model được cấu hình bằng phím mới được kiểm tra.

---
## Danh sách tính năng ✨
### Đã thực hiện ✅
![Vui lòng tham khảo sơ đồ kiến ​​trúc cài đặt mô-đun đầy đủ](docs/images/deploy2.png)
| Mô-đun chức năng | Mô tả |
|:---:|:---|
| Kiến trúc cốt lõi | Dựa trên [Cổng MQTT+UDP](https://github.com/xinnan-tech/xiaozhi-esp32-server/blob/main/docs/mqtt-gateway-integration.md), WebSocket, máy chủ HTTP, cung cấp hệ thống xác thực và quản lý bảng điều khiển hoàn chỉnh |
| Tương tác bằng giọng nói | Hỗ trợ truyền phát ASR (nhận dạng giọng nói), truyền phát TTS (tổng hợp giọng nói), VAD (phát hiện hoạt động giọng nói) và hỗ trợ nhận dạng và xử lý giọng nói đa ngôn ngữ |
| Nhận dạng giọng nói | Hỗ trợ đăng ký, quản lý và nhận dạng giọng nói của nhiều người dùng, xử lý song song với ASR, xác định danh tính của người nói trong thời gian thực và chuyển nó đến LLM để phản hồi được cá nhân hóa |
| Đối thoại thông minh | Hỗ trợ nhiều LLM (mô hình ngôn ngữ lớn) để đạt được cuộc đối thoại thông minh |
| Nhận thức trực quan | Hỗ trợ nhiều VLLM (mô hình trực quan lớn) để đạt được tương tác đa phương thức |
| Công nhận ý định | Hỗ trợ nhận dạng ý định mô hình lớn của plug-in, gọi hàm tự động mô hình lớn và cung cấp cơ chế xử lý ý định của plug-in |
| Hệ thống bộ nhớ | Hỗ trợ bộ nhớ ngắn hạn cục bộ, bộ nhớ giao diện mem0ai, bộ nhớ thông minh PowerMem và có chức năng tóm tắt bộ nhớ |
| Cơ sở kiến ​​thức | Hỗ trợ cơ sở tri thức RAGFlow, cho phép các mô hình lớn xác định nhu cầu lập lịch cơ sở tri thức trước khi trả lời |
| Cuộc gọi công cụ | Hỗ trợ giao thức IOT máy khách, giao thức MCP máy khách, giao thức MCP máy chủ, giao thức điểm truy cập MCP và các chức năng công cụ tùy chỉnh |
| Giao lệnh | Dựa vào giao thức MQTT, nó hỗ trợ phát lệnh MCP từ bảng điều khiển thông minh đến thiết bị ESP32 |
| Quản lý phụ trợ | Cung cấp giao diện quản lý Web hỗ trợ quản lý người dùng, cấu hình hệ thống và quản lý thiết bị; giao diện hỗ trợ hiển thị tiếng Trung giản thể, tiếng Trung phồn thể và tiếng Anh |
| Công cụ kiểm tra | Cung cấp các công cụ kiểm tra hiệu suất, công cụ kiểm tra mô hình trực quan và công cụ kiểm tra tương tác âm thanh |
| Hỗ trợ triển khai | Hỗ trợ triển khai Docker và triển khai cục bộ, cung cấp khả năng quản lý tệp cấu hình hoàn chỉnh |
| Hệ thống plug-in | Hỗ trợ chức năng mở rộng plug-in, phát triển plug-in tùy chỉnh và tải nóng plug-in |

### Đang được phát triển 🚧

Để tìm hiểu về tiến độ kế hoạch phát triển cụ thể, [vui lòng nhấp vào đây](https://github.com/users/xinnan-tech/projects/3). Để biết các câu hỏi thường gặp và hướng dẫn liên quan, vui lòng tham khảo [liên kết này](./docs/FAQ.md)

Nếu bạn là nhà phát triển phần mềm, đây là ["Thư ngỏ gửi nhà phát triển"](docs/contributor_open_letter.md), chào mừng bạn tham gia!

---

## Sinh thái sản phẩm 👬
Xiaozhi là một hệ sinh thái. Khi bạn sử dụng sản phẩm này, bạn cũng có thể xem các [dự án xuất sắc khác trong hệ sinh thái này](https://github.com/78/xiaozhi-esp32/blob/main/README_zh.md#%E7%9B%B8%E5%85%B3%E5%BC%80%E6%BA%90%E9%A1%B9%E7%9B%AE)

---

## Danh sách các nền tảng/thành phần được dự án này hỗ trợ 📋
### Mô hình ngôn ngữ LLM

| Cách sử dụng | Nền tảng được hỗ trợ | Nền tảng miễn phí |
|:---:|:---:|:---:|
| cuộc gọi giao diện openai | Alibaba Bailian, Động cơ núi lửa, DeepSeek, Zhipu, Gemini, iFlytek | Chí Phổ, Song Tử |
| cuộc gọi giao diện ollama | Olama | - |
| cuộc gọi giao diện dify | Làm mờ | - |
| cuộc gọi giao diện fastgpt | Nhanhgpt | - |
| cuộc gọi giao diện coze | Coze | - |
| cuộc gọi giao diện xinference | Xin suy luận | - |
| cuộc gọi giao diện trợ lý gia đình | Trang chủTrợ lý | - |

Trên thực tế, bất kỳ LLM nào hỗ trợ cuộc gọi giao diện openai đều có thể được truy cập và sử dụng.

---

### Mô hình tầm nhìn VLLM

| Cách sử dụng | Nền tảng được hỗ trợ | Nền tảng miễn phí |
|:---:|:---:|:---:|
| cuộc gọi giao diện openai | Alibaba Bailian, Zhipu ChatGLMVLLM | Trò chuyện ZhipuGLMVLLM |

Trên thực tế, bất kỳ VLLM nào hỗ trợ cuộc gọi giao diện openai đều có thể được truy cập và sử dụng.

---

### Tổng hợp giọng nói TTS

| Cách sử dụng | Nền tảng được hỗ trợ | Nền tảng miễn phí |
|:---:|:---:|:---:|
| Cuộc gọi giao diện | EdgeTTS, iFlytek, Huoshan Engine, Tencent Cloud, Alibaba Cloud và Bailian, CosyVoiceSiliconflow, TTS302AI, CozeCnTTS, GizwitsTTS, ACGNTTS, OpenAITTS, Coincidence TTS, MinimaxTTS | CosyVoiceSiliconflow (phần) |
| Dịch vụ địa phương | FishSpeech, GPT_SOVITS_V2, GPT_SOVITS_V3, Index-TTS, PaddleSpeech | Index-TTS, PaddleSpeech, FishSpeech, GPT_SOVITS_V2, GPT_SOVITS_V3 |

---

### Phát hiện hoạt động giọng nói VAD

| Loại | Tên nền tảng | Cách sử dụng | Mô hình sạc | Bình luận |
|:---:|:---------:|:----:|:----:|:--:|
| VAD | SileroVAD | Sử dụng địa phương | Miễn phí | |

---

### Nhận dạng giọng nói ASR

| Cách sử dụng | Nền tảng được hỗ trợ | Nền tảng miễn phí |
|:---:|:---:|:---:|
| Sử dụng địa phương | FunASR, SherpaASR | FunASR, SherpaASR |
| Cuộc gọi giao diện | FunASRServer, Volcano Engine, iFlytek, Tencent Cloud, Alibaba Cloud, Baidu Cloud, OpenAI ASR | Máy chủ FunASR |

---

### Nhận dạng giọng nói bằng giọng nói

| Cách sử dụng | Nền tảng được hỗ trợ | Nền tảng miễn phí |
|:---:|:---:|:---:|
| Sử dụng địa phương | Loa 3D | Loa 3D |

---

### Bộ nhớ lưu trữ

| Loại | Tên nền tảng | Cách sử dụng | Mô hình sạc | Bình luận |
|:------:|:---------------:|:----:|:---------:|:--:|
| Ký ức | mem0ai | Cuộc gọi giao diện | Hạn ngạch 1000 lần/tháng | |
| Ký ức | [powermem](./docs/powermem-integration.md) | Tóm tắt địa phương | Phụ thuộc vào LLM và DB | OceanBase là nguồn mở và hỗ trợ truy xuất thông minh |
| Ký ức | mem_local_short | Tóm tắt địa phương | Miễn phí | |
| Ký ức | tên | Không có chế độ bộ nhớ | Miễn phí | |

---

### Nhận dạng ý định

| Loại | Tên nền tảng | Cách sử dụng | Mô hình sạc | Bình luận |
|:------:|:-------------:|:----:|:-------:|:---------------------:|
| Ý định | ý định_llm | Cuộc gọi giao diện | Tính phí dựa trên LLM | Xác định ý định thông qua mô hình lớn, tính linh hoạt mạnh mẽ |
| Ý định | hàm_gọi | Cuộc gọi giao diện | Tính phí theo LLM | Hoàn thành ý định thông qua lệnh gọi hàm mô hình lớn, hiệu quả nhanh và tốt |
| Ý định | nhẹ nhàng | Không có chế độ có ý định | Miễn phí | Không có nhận dạng ý định nào được thực hiện và kết quả hội thoại được trả về trực tiếp |

---

### Tạo sinh tăng cường truy xuất Rag

| Loại | Tên nền tảng | Cách sử dụng | Mô hình sạc | Bình luận |
|:------:|:-------------:|:----:|:-------:|:---------------------:|
| Rag | dòng chảy hỗn loạn | Cuộc gọi giao diện | Các khoản phí dựa trên số token được sử dụng bằng cách cắt và phân đoạn từ | Sử dụng chức năng tạo nâng cao tìm kiếm của RagFlow để cung cấp phản hồi đối thoại chính xác hơn |

---

## Lời cảm ơn 🙏

| Logo | Dự án/Công ty | Mô tả |
|:---:|:---:|:---|
| <img src="./docs/images/logo_bailing.png" width="160"> | [Robot trò chuyện bằng giọng nói Bailing](https://github.com/wwbin2017/bailing) | Dự án này được lấy cảm hứng từ [Robot hội thoại bằng giọng nói Bailing](https://github.com/wwbin2017/bailing) và được triển khai trên cơ sở nó |
| <img src="./docs/images/logo_tenclass.png" width="160"> | [Shifangronghai](https://www.tenclass.com/) | Cảm ơn [Shifangronghai](https://www.tenclass.com/) đã xây dựng các giao thức truyền thông tiêu chuẩn, giải pháp tương thích đa thiết bị và trình diễn thực hành kịch bản đồng thời cao cho Hệ sinh thái Xiaozhi; cung cấp hỗ trợ tài liệu kỹ thuật liên kết đầy đủ cho dự án này |
| <img src="./docs/images/logo_xuanfeng.png" width="160"> | [Công nghệ Huyền Phong](https://github.com/Eric0308) | Cảm ơn [Xuanfeng Technology](https://github.com/Eric0308) đã đóng góp mã triển khai của khung gọi hàm, giao thức truyền thông MCP và cơ chế gọi plug-in. Thông qua hệ thống lập kế hoạch hướng dẫn được tiêu chuẩn hóa và khả năng mở rộng động, nó đã cải thiện đáng kể hiệu quả tương tác và khả năng mở rộng chức năng của thiết bị đầu cuối (IoT) |
| <img src="./docs/images/logo_junsen.png" width="160"> | [huangjunsen](https://github.com/huangjunsen0406) | Cảm ơn [huangjunsen](https://github.com/huangjunsen0406) đã đóng góp mô-đun `bản di động của bảng điều khiển thông minh`, cho phép kiểm soát hiệu quả và tương tác theo thời gian thực của các thiết bị di động đa nền tảng, cải thiện đáng kể sự thuận tiện trong vận hành và hiệu quả quản lý của hệ thống trong các tình huống di động |
| <img src="./docs/images/logo_huiyuan.png" width="160"> | [Thiết kế Huiyuan](http://ui.kwd988.net/) | Cảm ơn [Huiyuan Design](http://ui.kwd988.net/) đã cung cấp các giải pháp trực quan chuyên nghiệp cho dự án này, sử dụng kinh nghiệm thiết kế thực tế của mình để phục vụ hơn một nghìn công ty nhằm nâng cao trải nghiệm người dùng đối với các sản phẩm của dự án này |
| <img src="./docs/images/logo_qinren.png" width="160"> | [Công nghệ thông tin Qinren Tây An](https://www.029app.com/) | Cảm ơn [Xi'an Qinren Information Technology](https://www.029app.com/) đã đào sâu hệ thống trực quan của dự án này và đảm bảo tính nhất quán cũng như khả năng mở rộng của phong cách thiết kế tổng thể trong các ứng dụng đa kịch bản |
| <img src="./docs/images/logo_contributors.png" width="160"> | [Người đóng góp mã](https://github.com/xinnan-tech/xiaozhi-esp32-server/graphs/contributors) | Nhờ những người đóng góp [Tất cả người đóng góp mã](https://github.com/xinnan-tech/xiaozhi-esp32-server/graphs/contributors), những nỗ lực của bạn đã làm cho dự án trở nên mạnh mẽ và hiệu quả hơn. |


<a href="https://star-history.com/#xinnan-tech/xiaozhi-esp32-server&Date">

 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=xinnan-tech/xiaozhi-esp32-server&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=xinnan-tech/xiaozhi-esp32-server&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=xinnan-tech/xiaozhi-esp32-server&type=Date" />
 </picture>
</a>
