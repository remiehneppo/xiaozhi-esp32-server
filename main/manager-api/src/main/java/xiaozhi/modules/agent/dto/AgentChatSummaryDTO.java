package xiaozhi.modules.agent.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

/**
 * Tóm tắt bản ghi trò chuyện của tổng đài viên DTO
 */
@Data
@Schema(description = "Đối tượng tóm tắt bản ghi cuộc trò chuyện của tổng đài viên")
public class AgentChatSummaryDTO {

    @Schema(description = "phiênID")
    private String sessionId;

    @Schema(description = "đại lýID")
    private String agentId;

    @Schema(description = "Nội dung tóm tắt")
    private String summary;

    @Schema(description = "trạng thái tóm tắt")
    private boolean success;

    @Schema(description = "thông báo lỗi")
    private String errorMessage;

    public AgentChatSummaryDTO() {
        this.success = true;
    }

    public AgentChatSummaryDTO(String sessionId, String agentId, String summary) {
        this.sessionId = sessionId;
        this.agentId = agentId;
        this.summary = summary;
        this.success = true;
    }

    public AgentChatSummaryDTO(String sessionId, String errorMessage) {
        this.sessionId = sessionId;
        this.errorMessage = errorMessage;
        this.success = false;
    }

}