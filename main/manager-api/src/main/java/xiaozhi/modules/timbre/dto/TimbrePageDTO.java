package xiaozhi.modules.timbre.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;
import lombok.Data;

/**
 * Tham số phân trang giai điệu DTO
 *
 * @author zjy
 * @since 2025-3-21
 */
@Data
@Schema(description = "Thông số phân trang giai điệu")
public class TimbrePageDTO {

    @Schema(description = "tương ứng TTS Khóa chính của mô hình")
    @NotBlank(message = "{timbre.ttsModelId.require}")
    private String ttsModelId;

    @Schema(description = "Tên giọng nói")
    private String name;

    @Schema(description = "Số trang")
    private String page;

    @Schema(description = "Hiển thị số cột")
    private String limit;
}
