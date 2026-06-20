package xiaozhi.modules.knowledge.dto.chat;

import java.io.Serializable;
import java.util.List;
import java.util.Map;

import com.fasterxml.jackson.annotation.JsonProperty;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

/**
 * Yêu cầu trò chuyện trò chuyện DTO (định dạng tương thích với OpenAI)
 */
@Data
@Schema(description = "Yêu cầu trò chuyện trò chuyện")
public class ChatCompletionRequest implements Serializable {

    @Schema(description = "nhận dạng mô hình (tương ứng agent_id hoặc bot_id)", requiredMode = Schema.RequiredMode.REQUIRED)
    @JsonProperty("model")
    private String model;

    @Schema(description = "Danh sách tin nhắn hội thoại", requiredMode = Schema.RequiredMode.REQUIRED)
    @JsonProperty("messages")
    private List<Message> messages;

    @Schema(description = "Có phát trực tuyến trả lại hay không", defaultValue = "false")
    @JsonProperty("stream")
    private Boolean stream = false;

    @Schema(description = "hệ số nhiệt độ (0-1)", defaultValue = "0.7")
    @JsonProperty("temperature")
    private Double temperature;

    @Schema(description = "Session ID (Tùy chọn，Được sử dụng để tiếp tục một phiên)")
    @JsonProperty("session_id")
    private String sessionId;

    @Schema(description = "KhácRAGFlowthông số cụ thể (Tùy chọn)")
    private Map<String, Object> extra;

    @Data
    public static class Message implements Serializable {
        @Schema(description = "vai trò (system, user, assistant)", requiredMode = Schema.RequiredMode.REQUIRED)
        private String role;

        @Schema(description = "nội dung", requiredMode = Schema.RequiredMode.REQUIRED)
        private String content;
    }
}
