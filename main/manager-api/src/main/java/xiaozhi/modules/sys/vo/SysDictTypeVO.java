package xiaozhi.modules.sys.vo;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

import java.io.Serializable;
import java.util.Date;

/**
 * Loại từ điển VO
 */
@Data
@Schema(description = "loại từ điểnVO")
public class SysDictTypeVO implements Serializable {
    @Schema(description = "khóa chính")
    private Long id;

    @Schema(description = "loại từ điển")
    private String dictType;

    @Schema(description = "Tên từ điển")
    private String dictName;

    @Schema(description = "Bình luận")
    private String remark;

    @Schema(description = "sắp xếp")
    private Integer sort;

    @Schema(description = "Người sáng tạo")
    private Long creator;

    @Schema(description = "Tên người sáng tạo")
    private String creatorName;

    @Schema(description = "thời gian sáng tạo")
    private Date createDate;

    @Schema(description = "Trình cập nhật")
    private Long updater;

    @Schema(description = "Tên người cập nhật")
    private String updaterName;

    @Schema(description = "Thời gian cập nhật")
    private Date updateDate;
}
