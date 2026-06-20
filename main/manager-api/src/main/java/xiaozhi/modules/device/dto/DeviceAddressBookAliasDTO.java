package xiaozhi.modules.device.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;
import lombok.Data;

@Data
@Schema(description = "Cập nhật bí danh sổ địa chỉ thiết bị")
public class DeviceAddressBookAliasDTO {

    @NotBlank(message = "MACĐịa chỉ không thể trống")
    @Schema(description = "Thiết bị nàyMACđịa chỉ")
    private String macAddress;

    @NotBlank(message = "mục tiêuMACĐịa chỉ không thể trống")
    @Schema(description = "Thiết bị khácMACđịa chỉ")
    private String targetMac;

    @Schema(description = "Tôi gọi người khác là gì")
    private String alias;
}