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
@TableName("ai_device_address_book")
@Schema(description = "Sổ địa chỉ thiết bị")
public class DeviceAddressBookEntity {

    @TableId(type = IdType.INPUT)
    @Schema(description = "Thiết bị nàyMACđịa chỉ")
    private String macAddress;

    @Schema(description = "Thiết bị khácMACđịa chỉ")
    private String targetMac;

    @Schema(description = "Tôi gọi người khác là gì")
    private String alias;

    @Schema(description = "Bạn có được phép gọi không")
    private Boolean hasPermission;

    @TableField(fill = FieldFill.INSERT)
    @Schema(description = "Người sáng tạo")
    private Long creator;

    @TableField(fill = FieldFill.INSERT)
    @Schema(description = "thời gian sáng tạo")
    private Date createDate;

    @TableField(fill = FieldFill.INSERT_UPDATE)
    @Schema(description = "Trình cập nhật")
    private Long updater;

    @TableField(fill = FieldFill.INSERT_UPDATE)
    @Schema(description = "Thời gian cập nhật")
    private Date updateDate;
}