package xiaozhi.modules.sys.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.Min;
import lombok.Data;

/**
 * Tham số DTO cho người dùng phân trang quản trị viên
 *
 * @author zjy
 * @since 2025-3-21
 */
@Data
@Schema(description = "Thông số người dùng phân trang quản trịDTO")
public class AdminPageUserDTO {

    @Schema(description = "Số điện thoại di động")
    private String mobile;

    @Schema(description = "Số trang")
    @Min(value = 0, message = "{sort.number}")
    private String page;

    @Schema(description = "Hiển thị số cột")
    @Min(value = 0, message = "{sort.number}")
    private String limit;
}
