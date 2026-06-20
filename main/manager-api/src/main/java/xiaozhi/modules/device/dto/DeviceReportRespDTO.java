package xiaozhi.modules.device.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;
import lombok.Getter;
import lombok.Setter;

@Data
@Schema(description = "Thiết bịOTAPhát hiện nội dung trả về phiên bản，Chứa các yêu cầu về mã kích hoạt")
public class DeviceReportRespDTO {
    @Schema(description = "giờ máy chủ")
    private ServerTime server_time;

    @Schema(description = "mã kích hoạt")
    private Activation activation;

    @Schema(description = "thông báo lỗi")
    private String error;

    @Schema(description = "Thông tin phiên bản phần mềm")
    private Firmware firmware;

    @Schema(description = "WebSocketCấu hình")
    private Websocket websocket;

    @Schema(description = "MQTT GatewayCấu hình")
    private MQTT mqtt;

    @Getter
    @Setter
    public static class Firmware {
        @Schema(description = "số phiên bản")
        private String version;
        @Schema(description = "Địa chỉ tải xuống")
        private String url;
    }

    public static DeviceReportRespDTO createError(String message) {
        DeviceReportRespDTO resp = new DeviceReportRespDTO();
        resp.setError(message);
        return resp;
    }

    @Setter
    @Getter
    public static class Activation {
        @Schema(description = "mã kích hoạt")
        private String code;

        @Schema(description = "Thông tin mã kích hoạt: địa chỉ kích hoạt")
        private String message;

        @Schema(description = "Mã thách thức")
        private String challenge;
    }

    @Getter
    @Setter
    public static class ServerTime {
        @Schema(description = "Dấu thời gian")
        private Long timestamp;

        @Schema(description = "múi giờ")
        private String timeZone;

        @Schema(description = "bù múi giờ，Đơn vị là phút")
        private Integer timezone_offset;
    }

    @Getter
    @Setter
    public static class Websocket {
        @Schema(description = "WebSocketĐịa chỉ máy chủ")
        private String url;
        @Schema(description = "WebSocket Chứng nhận token")
        private String token;
    }

    @Getter
    @Setter
    public static class MQTT {
        @Schema(description = "MQTT Định cấu hình URL")
        private String endpoint;
        @Schema(description = "MQTT mã định danh duy nhất của khách hàng")
        private String client_id;
        @Schema(description = "MQTT Tên người dùng xác thực")
        private String username;
        @Schema(description = "MQTT Mật khẩu xác thực")
        private String password;
        @Schema(description = "ESP32 Đăng chủ đề tin nhắn")
        private String publish_topic;
        @Schema(description = "ESP32 Chủ đề đã đăng ký")
        private String subscribe_topic;
    }
}