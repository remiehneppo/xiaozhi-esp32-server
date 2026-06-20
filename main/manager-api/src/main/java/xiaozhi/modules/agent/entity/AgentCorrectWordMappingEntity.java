package xiaozhi.modules.agent.entity;

import java.util.Date;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

@Data
@TableName("ai_agent_correct_word_mapping")
@Schema(description = "Liên kết tập tin từ thay thế đại lý")
public class AgentCorrectWordMappingEntity {

    @TableId(type = IdType.ASSIGN_UUID)
    @Schema(description = "khóa chính")
    private String id;

    @Schema(description = "đại lýID")
    private String agentId;

    @Schema(description = "tập tin từ thay thếID")
    private String fileId;

    @Schema(description = "Người sáng tạo")
    private Long creator;

    @Schema(description = "thời gian sáng tạo")
    private Date createdAt;

    @Schema(description = "Trình cập nhật")
    private Long updater;

    @Schema(description = "Thời gian cập nhật")
    private Date updatedAt;
}
