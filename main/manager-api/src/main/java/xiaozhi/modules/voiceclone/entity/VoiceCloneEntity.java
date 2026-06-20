package xiaozhi.modules.voiceclone.entity;

import java.util.Date;

import com.baomidou.mybatisplus.annotation.FieldFill;
import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = false)
@TableName("ai_voice_clone")
@Schema(description = "nhân bản âm thanh")
public class VoiceCloneEntity {

    @TableId(type = IdType.ASSIGN_UUID)
    @Schema(description = "mã định danh duy nhất")
    private String id;

    @Schema(description = "tên âm thanh")
    private String name;

    @Schema(description = "người mẫuid")
    private String modelId;

    @Schema(description = "âm thanhid")
    private String voiceId;

    @Schema(description = "Ngôn ngữ")
    private String languages;

    @Schema(description = "người dùng ID（Bảng người dùng liên quan）")
    private Long userId;

    @Schema(description = "âm thanh")
    private byte[] voice;

    @Schema(description = "tình trạng đào tạo：0Để được đào tạo 1trong đào tạo 2Đào tạo thành công 3Đào tạo không thành công")
    private Integer trainStatus;

    @Schema(description = "Nguyên nhân dẫn đến sai sót trong đào tạo")
    private String trainError;

    @Schema(description = "Người sáng tạo")
    @TableField(fill = FieldFill.INSERT)
    private Long creator;

    @Schema(description = "thời gian sáng tạo")
    @TableField(fill = FieldFill.INSERT)
    private Date createDate;
}
