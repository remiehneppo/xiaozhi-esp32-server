package xiaozhi.modules.voiceclone.dto;

import java.util.List;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

@Data
@Schema(description = "nhân bản âm thanhDTO")
public class VoiceCloneDTO {

    @Schema(description = "người mẫuID")
    private String modelId;

    @Schema(description = "âm sắcIDdanh sách")
    private List<String> voiceIds;

    @Schema(description = "người dùngID")
    private Long userId;

    @Schema(description = "Ngôn ngữ")
    private String languages;
}
