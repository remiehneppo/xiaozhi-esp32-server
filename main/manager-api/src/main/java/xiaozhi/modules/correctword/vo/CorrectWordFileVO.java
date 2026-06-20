package xiaozhi.modules.correctword.vo;

import java.util.Date;
import java.util.List;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

@Data
@Schema(description = "Danh sách file word thay thếVO")
public class CorrectWordFileVO {

    @Schema(description = "tập tin từ thay thếID")
    private String id;

    @Schema(description = "tên tập tin gốc")
    private String fileName;

    @Schema(description = "Số từ thay thế")
    private Integer wordCount;

    @Schema(description = "Thay thế nội dung từ，mỗi dòng một cái")
    private List<String> content;

    @Schema(description = "thời gian sáng tạo")
    private Date createdAt;

    @Schema(description = "Thời gian cập nhật")
    private Date updatedAt;
}
