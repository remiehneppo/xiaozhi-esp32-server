package xiaozhi.modules.sys.dto;

import java.io.Serializable;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;
import lombok.Data;

/**
 * Thay đổi mật khẩu
 */
@Data
@Schema(description = "Thay đổi mật khẩu")
public class PasswordDTO implements Serializable {

    @Schema(description = "Mật khẩu gốc")
    @NotBlank(message = "{sysuser.password.require}")
    private String password;

    @Schema(description = "mật khẩu mới")
    @NotBlank(message = "{sysuser.password.require}")
    private String newPassword;

}