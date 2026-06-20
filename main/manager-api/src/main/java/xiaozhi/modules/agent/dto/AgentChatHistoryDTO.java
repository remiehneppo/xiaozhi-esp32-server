package xiaozhi.modules.agent.dto;

import java.util.Date;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

/**
 * Bản ghi trò chuyện của đại lý DTO
 */
@Data
@Schema(description = "Lịch sử trò chuyện của đại lý")
public class AgentChatHistoryDTO {
    @Schema(description = "thời gian sáng tạo")
    private Date createdAt;

    @Schema(description = "Loại tin nhắn: 1-người dùng, 2-đại lý")
    private Byte chatType;

    @Schema(description = "Nội dung trò chuyện")
    private String content;

    @Schema(description = "Âm thanhID")
    private String audioId;

    @Schema(description = "MACđịa chỉ")
    private String macAddress;
}