package xiaozhi.modules.agent.vo;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

/**
 * VO của dữ liệu trò chuyện cá nhân của người dùng đại lý
 */
@Data
public class AgentChatHistoryUserVO {
    @Schema(description = "Nội dung trò chuyện")
    private String content;

    @Schema(description = "Âm thanhID")
    private String audioId;
}
