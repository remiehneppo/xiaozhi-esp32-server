package xiaozhi.modules.model.entity;

import java.util.Date;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

@Data
@TableName("ai_model_provider")
@Schema(description = "bảng nhà cung cấp mô hình")
public class ModelProviderEntity {

    @TableId(type = IdType.ASSIGN_UUID)
    @Schema(description = "khóa chính")
    private String id;

    @Schema(description = "Loại mô hình(Memory/ASR/VAD/LLM/TTS)")
    private String modelType;

    @Schema(description = "loại nhà cung cấp，Chẳng hạn như openai、")
    private String providerCode;

    @Schema(description = "tên nhà cung cấp")
    private String name;

    @Schema(description = "Danh sách trường nhà cung cấp(JSONđịnh dạng)")
    private String fields;

    @Schema(description = "sắp xếp")
    private Integer sort;

    @Schema(description = "Người sáng tạo")
    private Long creator;

    @Schema(description = "thời gian sáng tạo")
    private Date createDate;

    @Schema(description = "Trình cập nhật")
    private Long updater;

    @Schema(description = "Thời gian cập nhật")
    private Date updateDate;
}
