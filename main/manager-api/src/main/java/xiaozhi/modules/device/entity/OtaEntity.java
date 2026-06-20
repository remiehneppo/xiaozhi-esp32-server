package xiaozhi.modules.device.entity;

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
@TableName("ai_ota")
@Schema(description = "Thông tin phần mềm")
public class OtaEntity {

    @TableId(type = IdType.ASSIGN_UUID)
    @Schema(description = "ID")
    private String id;

    @Schema(description = "Tên chương trình cơ sở")
    private String firmwareName;

    @Schema(description = "Loại phần mềm")
    private String type;

    @Schema(description = "số phiên bản")
    private String version;

    @Schema(description = "kích thước tập tin(Byte)")
    private Long size;

    @Schema(description = "Bình luận/Mô tả")
    private String remark;

    @Schema(description = "Đường dẫn phần sụn")
    private String firmwarePath;

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