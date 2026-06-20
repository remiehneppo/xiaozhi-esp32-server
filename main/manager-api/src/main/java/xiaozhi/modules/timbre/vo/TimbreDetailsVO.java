package xiaozhi.modules.timbre.vo;

import java.io.Serializable;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

/**
 * Hiển thị chi tiết âm thanh VO
 *
 * @author zjy
 * @since 2025-3-21
 */
@Data
public class TimbreDetailsVO implements Serializable {
    @Schema(description = "âm sắcid")
    private String id;

    @Schema(description = "Ngôn ngữ")
    private String languages;

    @Schema(description = "Tên giọng nói")
    private String name;

    @Schema(description = "Bình luận")
    private String remark;

    @Schema(description = "Đường dẫn âm thanh tham chiếu")
    private String referenceAudio;

    @Schema(description = "Văn bản tham khảo")
    private String referenceText;

    @Schema(description = "sắp xếp")
    private long sort;

    @Schema(description = "tương ứng TTS Khóa chính của mô hình")
    private String ttsModelId;

    @Schema(description = "mã hóa âm sắc")
    private String ttsVoice;

    @Schema(description = "Địa chỉ phát lại âm thanh")
    private String voiceDemo;

}
