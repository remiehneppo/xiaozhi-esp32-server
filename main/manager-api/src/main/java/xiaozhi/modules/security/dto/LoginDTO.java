package xiaozhi.modules.security.dto;

import java.io.Serializable;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;
import lombok.Data;

/**
 * Mẫu đăng nhập
 */
@Data
@Schema(description = "Mẫu đăng nhập")
public class LoginDTO implements Serializable {

    @Schema(description = "Số điện thoại di động")
    @NotBlank(message = "{sysuser.username.require}")
    private String username;

    @Schema(description = "Mật khẩu")
    @NotBlank(message = "{sysuser.password.require}")
    private String password;

    @Schema(description = "Mã xác minh điện thoại di động")
    private String mobileCaptcha;

    @Schema(description = "mã định danh duy nhất")
    @NotBlank(message = "{sysuser.uuid.require}")
    private String captchaId;

}