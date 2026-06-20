package xiaozhi.modules.model.dto;

import java.io.Serializable;
import java.util.Date;

import com.baomidou.mybatisplus.annotation.FieldFill;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.extension.handlers.JacksonTypeHandler;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.Data;
import xiaozhi.common.validator.group.UpdateGroup;

@Data
@Schema(description = "nhà cung cấp mô hình/Kinh doanh")
public class ModelProviderDTO implements Serializable {
    @Schema(description = "khóa chính")
    @NotBlank(message = "idkhông thể trống", groups = UpdateGroup.class)
    private String id;

    @Schema(description = "Loại mô hình(Memory/ASR/VAD/LLM/TTS)")
    @NotBlank(message = "modelTypekhông thể trống")
    private String modelType;

    @Schema(description = "loại nhà cung cấp")
    @NotBlank(message = "providerCodekhông thể trống")
    private String providerCode;

    @Schema(description = "tên nhà cung cấp")
    @NotBlank(message = "namekhông thể trống")
    private String name;

    @Schema(description = "Danh sách trường nhà cung cấp(JSONđịnh dạng)")
    @TableField(typeHandler = JacksonTypeHandler.class)
    @NotBlank(message = "fields(JSONđịnh dạng)không thể trống")
    private String fields;

    @Schema(description = "sắp xếp")
    @NotNull(message = "sortkhông thể trống")
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
