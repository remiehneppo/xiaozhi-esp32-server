package xiaozhi.modules.config.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;
import lombok.Data;

@Data
@Schema(description = "Nhận từ thay thế đại lýDTO")
public class CorrectWordsDTO {

    @NotBlank(message = "Thiết bịMACĐịa chỉ không thể trống")
    @Schema(description = "Thiết bịMACđịa chỉ")
    private String macAddress;
}
