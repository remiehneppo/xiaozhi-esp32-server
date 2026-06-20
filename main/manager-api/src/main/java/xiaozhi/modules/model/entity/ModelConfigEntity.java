package xiaozhi.modules.model.entity;

import java.util.Date;

import com.baomidou.mybatisplus.annotation.FieldFill;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableName;
import com.baomidou.mybatisplus.extension.handlers.JacksonTypeHandler;

import cn.hutool.json.JSONObject;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

@Data
@TableName(value = "ai_model_config", autoResultMap = true)
@Schema(description = "Bảng cấu hình mô hình")
public class ModelConfigEntity {

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

    @TableField(typeHandler = JacksonTypeHandler.class)
    @Schema(description = "Cấu hình mô hình(JSONđịnh dạng)")
    private JSONObject configJson;

    @Schema(description = "Liên kết tài liệu chính thức")
    private String docLink;

    @Schema(description = "Bình luận")
    private String remark;

    @Schema(description = "sắp xếp")
    private Integer sort;

    @Schema(description = "Trình cập nhật")
    @TableField(fill = FieldFill.UPDATE)
    private Long updater;

    @Schema(description = "Thời gian cập nhật")
    @TableField(fill = FieldFill.UPDATE)
    private Date updateDate;

    @Schema(description = "Người sáng tạo")
    @TableField(fill = FieldFill.INSERT)
    private Long creator;

    @Schema(description = "thời gian sáng tạo")
    @TableField(fill = FieldFill.INSERT)
    private Date createDate;
}
