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
@TableName("ai_device")
@Schema(description = "Thông tin thiết bị")
public class DeviceEntity {

    @TableId(type = IdType.ASSIGN_UUID)
    @Schema(description = "ID")
    private String id;

    @Schema(description = "Người dùng được liên kếtID")
    private Long userId;

    @Schema(description = "MACđịa chỉ")
    private String macAddress;

    @Schema(description = "Lần kết nối cuối cùng")
    private Date lastConnectedAt;

    @Schema(description = "Công tắc cập nhật tự động(0Đóng/1bật lên)")
    private Integer autoUpdate;

    @Schema(description = "Mô hình phần cứng thiết bị")
    private String board;

    @Schema(description = "Bí danh thiết bị")
    private String alias;

    @Schema(description = "đại lýID")
    private String agentId;

    @Schema(description = "Số phiên bản phần sụn")
    private String appVersion;

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