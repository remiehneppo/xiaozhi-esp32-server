package xiaozhi.modules.sys.vo;

import java.util.Date;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

/**
 * Quản trị viên hiển thị VO của người dùng trong trang
 * @ zjy
 *
 * @since 2025-3-25
 */
@Data
public class AdminPageUserVO {

    @Schema(description = "Số lượng thiết bị")
    private String deviceCount;

    @Schema(description = "Số điện thoại di động")
    private String mobile;

    @Schema(description = "Trạng thái")
    private Integer status;

    @Schema(description = "người dùngid")
    private String userid;

    @Schema(description = "Thời gian đăng ký")
    private Date createDate;
}
