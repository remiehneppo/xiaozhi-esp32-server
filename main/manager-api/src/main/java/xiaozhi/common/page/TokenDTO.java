package xiaozhi.common.page;

import java.io.Serializable;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

/**
 * Thông tin mã thông báo
 *
 * @author Jack
 */
@Data
@Schema(description = "Thông tin mã thông báo")
public class TokenDTO implements Serializable {

    @Schema(description = "Mật khẩu")
    private String token;

    @Schema(description = "Thời gian hết hạn")
    private int expire;

    @Schema(description = "Dấu vân tay của khách hàng")
    private String clientHash;
}
