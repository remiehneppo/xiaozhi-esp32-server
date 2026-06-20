package xiaozhi.modules.device.dto;

import java.io.Serializable;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Getter;
import lombok.Setter;

/**
 * Thông tin tiêu đề đăng ký thiết bị
 *
 * @author zjy
 * @since 2025-3-28
 */
@Setter
@Getter
@Schema(description = "Thông tin tiêu đề đăng ký thiết bị")
public class DeviceRegisterDTO implements Serializable {

    @Schema(description = "macđịa chỉ")
    private String macAddress;

}