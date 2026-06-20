package xiaozhi.modules.agent.entity;

import java.util.Date;
import java.util.List;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import com.baomidou.mybatisplus.extension.handlers.JacksonTypeHandler;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;
import xiaozhi.modules.agent.dto.ContextProviderDTO;

@Data
@TableName(value = "ai_agent_context_provider", autoResultMap = true)
@Schema(description = "Cấu hình nguồn ngữ cảnh của tác nhân")
public class AgentContextProviderEntity {

    @TableId(type = IdType.ASSIGN_UUID)
    @Schema(description = "khóa chính")
    private String id;

    @Schema(description = "đại lýID")
    private String agentId;

    @Schema(description = "Cấu hình nguồn ngữ cảnh")
    @TableField(typeHandler = JacksonTypeHandler.class)
    private List<ContextProviderDTO> contextProviders;

    @Schema(description = "Người sáng tạo")
    private Long creator;

    @Schema(description = "thời gian sáng tạo")
    private Date createdAt;

    @Schema(description = "Trình cập nhật")
    private Long updater;

    @Schema(description = "Thời gian cập nhật")
    private Date updatedAt;
}
