package xiaozhi.modules.model.dto;

import java.io.Serial;
import java.io.Serializable;

import cn.hutool.json.JSONObject;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

@Data
@Schema(description = "nhà cung cấp mô hình/Kinh doanh")
public class ModelConfigDTO implements Serializable {

    @Serial
    private static final long serialVersionUID = 1L;

    @Schema(description = "khóa chính")
    private String id;

    @Schema(description = "Loại mô hình(Memory/ASR/VAD/LLM/TTS)")
    private String modelType;

    @Schema(description = "mã hóa mô hình(Chẳng hạn nhưAliLLM、DoubaoTTS)")
    private String modelCode;

    @Schema(description = "Tên mẫu")
    private String modelName;

    @Schema(description = "Nó có được cấu hình theo mặc định không?(0Không 1Có)")
    private Integer isDefault;

    @Schema(description = "Có bật hay không")
    private Integer isEnabled;

    @Schema(description = "Cấu hình mô hình(JSONđịnh dạng)")
    private JSONObject configJson;

    @Schema(description = "Liên kết tài liệu chính thức")
    private String docLink;

    @Schema(description = "Bình luận")
    private String remark;

    @Schema(description = "sắp xếp")
    private Integer sort;
}
