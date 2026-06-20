package xiaozhi.modules.device.vo;

import java.util.Date;

import com.fasterxml.jackson.annotation.JsonFormat;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

@Data
@Schema(description = "Người dùng hiển thị danh sách thiết bịVO")
public class UserShowDeviceListVO {

    @Schema(description = "appphiên bản")
    private String appVersion;

    @Schema(description = "Ràng buộc tên người dùng")
    private String bindUserName;

    @Schema(description = "Mẫu thiết bị")
    private String deviceType;

    @Schema(description = "Mẫu thiết bị(board)")
    private String board;

    @Schema(description = "mã định danh duy nhất của thiết bị")
    private String id;

    @Schema(description = "macđịa chỉ")
    private String macAddress;

    @Schema(description = "Bí danh thiết bị")
    private String alias;

    @Schema(description = "bật lênOTA")
    private Integer otaUpgrade;

    @Schema(description = "Lần trò chuyện cuối cùng")
    private String recentChatTime;

    @Schema(description = "Lần kết nối cuối cùng(UTCmili giây)")
    private Long lastConnectedAtTimestamp;

    @Schema(description = "thời gian ràng buộc")
    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "yyyy-MM-dd HH:mm:ss", timezone = "UTC")
    private Date createDate;

}