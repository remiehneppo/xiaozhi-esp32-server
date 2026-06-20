package xiaozhi.modules.agent.vo;

import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.extension.handlers.JacksonTypeHandler;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;
import lombok.EqualsAndHashCode;
import xiaozhi.modules.agent.dto.ContextProviderDTO;
import xiaozhi.modules.agent.entity.AgentEntity;
import xiaozhi.modules.agent.entity.AgentPluginMapping;

import java.util.List;

/**
 * Cơ quan trả lời thông tin đại lý VO
 * Lớp thực thể Tác nhân AgentEntity được mở rộng trực tiếp ở đây. Nếu sau này bạn cần chuẩn hóa các trường trả về, bạn có thể sao chép các trường đó ra.
 */
@EqualsAndHashCode(callSuper = true)
@Data
public class AgentInfoVO extends AgentEntity
{
    @Schema(description = "Danh sách pluginId")
    @TableField(typeHandler = JacksonTypeHandler.class)
    private List<AgentPluginMapping> functions;

    @Schema(description = "Cấu hình nguồn ngữ cảnh")
    private List<ContextProviderDTO> contextProviders;

    @Schema(description = "tập tin từ thay thếIDdanh sách")
    private List<String> correctWordFileIds;
}
