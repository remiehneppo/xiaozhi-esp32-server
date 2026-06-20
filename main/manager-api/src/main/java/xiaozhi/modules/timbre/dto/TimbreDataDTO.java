package xiaozhi.modules.timbre.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import lombok.Data;

/**
 * Dữ liệu bảng giai điệu DTO
 *
 * @author zjy
 * @since 2025-3-21
 */
@Data
@Schema(description = "Thông tin bảng giai điệu")
public class TimbreDataDTO {

    @Schema(description = "Ngôn ngữ")
    @NotBlank(message = "{timbre.languages.require}")
    private String languages;

    @Schema(description = "Tên giọng nói")
    @NotBlank(message = "{timbre.name.require}")
    private String name;

    @Schema(description = "Bình luận")
    private String remark;

    @Schema(description = "Đường dẫn âm thanh tham chiếu")
    private String referenceAudio;

    @Schema(description = "Văn bản tham khảo")
    private String referenceText;

    @Schema(description = "sắp xếp")
    @Min(value = 0, message = "{sort.number}")
    private long sort;

    @Schema(description = "tương ứng TTS Khóa chính của mô hình")
    @NotBlank(message = "{timbre.ttsModelId.require}")
    private String ttsModelId;

    @Schema(description = "mã hóa âm sắc")
    @NotBlank(message = "{timbre.ttsVoice.require}")
    private String ttsVoice;

    @Schema(description = "Địa chỉ phát lại âm thanh")
    private String voiceDemo;
}