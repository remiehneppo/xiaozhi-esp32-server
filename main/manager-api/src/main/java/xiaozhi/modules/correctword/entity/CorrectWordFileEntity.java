package xiaozhi.modules.correctword.entity;

import java.util.Date;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

@Data
@TableName("ai_agent_correct_word_file")
@Schema(description = "Tập tin từ thay thế đại lý")
public class CorrectWordFileEntity {

    @TableId(type = IdType.ASSIGN_UUID)
    @Schema(description = "tập tin từ thay thếID")
    private String id;

    @Schema(description = "tên tập tin gốc")
    private String fileName;

    @Schema(description = "Số từ thay thế")
    private Integer wordCount;

    @Schema(description = "Nội dung gốc của tập tin（để tải xuống）")
    private String content;

    @Schema(description = "Người sáng tạo")
    private Long creator;

    @Schema(description = "thời gian sáng tạo")
    private Date createdAt;

    @Schema(description = "Trình cập nhật")
    private Long updater;

    @Schema(description = "Thời gian cập nhật")
    private Date updatedAt;
}
