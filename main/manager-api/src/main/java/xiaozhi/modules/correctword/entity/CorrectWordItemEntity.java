package xiaozhi.modules.correctword.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

@Data
@TableName("ai_agent_correct_word_item")
@Schema(description = "Mục nhập từ thay thế")
public class CorrectWordItemEntity {

    @TableId(type = IdType.ASSIGN_UUID)
    @Schema(description = "lối vàoID")
    private String id;

    @Schema(description = "Tập tin thuộc vềID")
    private String fileId;

    @Schema(description = "từ gốc")
    private String sourceWord;

    @Schema(description = "từ thay thế")
    private String targetWord;
}
