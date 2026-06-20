package xiaozhi.modules.sys.vo;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

import java.io.Serializable;
import java.util.Date;

/**
 * Dữ liệu từ điển VO
 */
@Data
@Schema(description = "dữ liệu từ điểnVO")
public class SysDictDataVO implements Serializable {
    @Schema(description = "khóa chính")
    private Long id;

    @Schema(description = "loại từ điểnID")
    private Long dictTypeId;

    @Schema(description = "thẻ từ điển")
    private String dictLabel;

    @Schema(description = "Giá trị từ điển")
    private String dictValue;

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
