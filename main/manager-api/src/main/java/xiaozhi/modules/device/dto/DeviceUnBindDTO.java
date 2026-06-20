package xiaozhi.modules.device.dto;

import java.io.Serializable;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;
import lombok.Data;

/**
 * Biểu mẫu hủy liên kết thiết bị
 */
@Data
@Schema(description = "Biểu mẫu hủy liên kết thiết bị")
public class DeviceUnBindDTO implements Serializable {

    @Schema(description = "Thiết bịID")
    @NotBlank(message = "Thiết bịIDkhông thể trống")
    private String deviceId;

}