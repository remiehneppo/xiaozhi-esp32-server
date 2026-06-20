package xiaozhi.modules.device.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Data;

/**
 * DTO ràng buộc thiết bị
 *
 * @author zjy
 * @since 2025-3-28
 */
@Data
@AllArgsConstructor
@Schema(description = "Thông tin đầu nối thiết bị")
public class DeviceBindDTO {

    @Schema(description = "macđịa chỉ")
    private String macAddress;

    @Schema(description = "người dùngid")
    private Long userId;

    @Schema(description = "đại lýid")
    private String agentId;

}