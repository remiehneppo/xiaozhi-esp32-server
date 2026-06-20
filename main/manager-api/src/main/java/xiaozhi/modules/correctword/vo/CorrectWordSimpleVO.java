package xiaozhi.modules.correctword.vo;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

@Data
@Schema(description = "Đơn giản hóa từ thay thếVO（Sử dụng bên thiết bị）")
public class CorrectWordSimpleVO {

    @Schema(description = "từ gốc")
    private String sourceWord;

    @Schema(description = "từ thay thế")
    private String targetWord;
}
