package xiaozhi.modules.agent.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.Data;

/**
 * Yêu cầu báo cáo trò chuyện trên thiết bị Xiaozhi
 *
 * @author Haotian
 * @version 1.0, 2025/5/8
 */
@Data
@Schema(description = "Yêu cầu báo cáo trò chuyện trên thiết bị Xiaozhi")
public class AgentChatHistoryReportDTO {
    @Schema(description = "MACđịa chỉ", example = "00:11:22:33:44:55")
    @NotBlank
    private String macAddress;
    @Schema(description = "phiênID", example = "79578c31-f1fb-426a-900e-1e934215f05a")
    @NotBlank
    private String sessionId;
    @Schema(description = "Loại tin nhắn: 1-người dùng, 2-đại lý", example = "1")
    @NotNull
    private Byte chatType;
    @Schema(description = "Nội dung trò chuyện", example = "xin chào")
    @NotBlank
    private String content;
    @Schema(description = "base64được mã hóaopusdữ liệu âm thanh", example = "")
    private String audioBase64;
    @Schema(description = "Thời gian báo cáo，dấu thời gian mười chữ số，Nếu trống, thời gian hiện tại sẽ được sử dụng theo mặc định.", example = "1745657732")
    private Long reportTime;
}
