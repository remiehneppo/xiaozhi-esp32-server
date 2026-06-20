package xiaozhi.modules.agent.entity;

import java.io.Serializable;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

/**
 * Bảng ánh xạ duy nhất giữa Tác nhân và trình cắm
 *
 * @TableName ai_agent_plugin_mapping
 */
@Data
@TableName(value = "ai_agent_plugin_mapping")
@Schema(description = "AgentBảng ánh xạ duy nhất tới các plugin")
public class AgentPluginMapping implements Serializable {
    /**
     * khóa chính
     */
    @TableId(type = IdType.ASSIGN_ID)
    @Schema(description = "Khóa chính thông tin ánh xạID")
    private Long id;

    /**
     * ID đại lý
     */
    @Schema(description = "đại lýID")
    private String agentId;

    /**
     * Mã plugin
     */
    @Schema(description = "trình cắm thêmID")
    private String pluginId;

    /**
     * Định dạng tham số trình cắm (Json)
     */
    @Schema(description = "Thông số trình cắm(Json)định dạng")
    private String paramInfo;

    // Trường dự phòng, được sử dụng để tạo điều kiện thuận lợi cho việc kiểm tra Provider_code của trình cắm khi truy vấn trình cắm dựa trên ID. Để biết chi tiết, hãy xem tệp xml lớp dao.
    @TableField(exist = false)
    @Schema(description = "trình cắm thêmprovider_code, Bảng tương ứngai_model_provider")
    private String providerCode;

    @TableField(exist = false)
    private static final long serialVersionUID = 1L;
}