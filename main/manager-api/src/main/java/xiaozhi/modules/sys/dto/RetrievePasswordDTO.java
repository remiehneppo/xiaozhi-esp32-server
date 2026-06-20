package xiaozhi.modules.sys.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;
import lombok.Data;

import java.io.Serializable;

/**
 * Lấy lại mật khẩu DTO
 */
@Data
@Schema(description = "Lấy lại mật khẩu")
public class RetrievePasswordDTO implements Serializable {

    @Schema(description = "Số điện thoại di động")
    @NotBlank(message = "{sysuser.password.require}")
    private String phone;

    @Schema(description = "Mã xác minh")
    @NotBlank(message = "{sysuser.password.require}")
    private String code;

    @Schema(description = "mật khẩu mới")
    @NotBlank(message = "{sysuser.password.require}")
    private String password;

    @Schema(description = "Mã xác minh đồ họaID")
    @NotBlank(message = "{sysuser.uuid.require}")
    private String captchaId;



}