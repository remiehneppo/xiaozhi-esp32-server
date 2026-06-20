package xiaozhi.modules.device.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.Min;
import lombok.Data;

/**
 * Truy vấn DTO của tất cả các thiết bị
 *
 * @author zjy
 * @since 2025-3-21
 */
@Data
@Schema(description = "Truy vấn tất cả các thiết bịDTO")
public class DevicePageUserDTO {

    @Schema(description = "Từ khóa thiết bị")
    private String keywords;

    @Schema(description = "Số trang")
    @Min(value = 0, message = "{page.number}")
    private String page;

    @Schema(description = "Hiển thị số cột")
    @Min(value = 0, message = "{limit.number}")
    private String limit;
}
