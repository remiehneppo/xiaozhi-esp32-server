package xiaozhi.modules.security.dto;

import java.io.Serializable;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;
import lombok.Data;

/**
 * Yêu cầu mã xác minh qua SMS DTO
 */
@Data
@Schema(description = "Yêu cầu mã xác minh qua SMS")
public class SmsVerificationDTO implements Serializable {
    private static final long serialVersionUID = 1L;

    @Schema(description = "Số điện thoại di động")
    @NotBlank(message = "{sysuser.username.require}")
    private String phone;

    @Schema(description = "Mã xác minh")
    @NotBlank(message = "{sysuser.captcha.require}")
    private String captcha;

    @Schema(description = "mã định danh duy nhất")
    @NotBlank(message = "{sysuser.uuid.require}")
    private String captchaId;
}