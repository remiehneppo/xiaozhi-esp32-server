package xiaozhi.modules.knowledge.dto.bot;

import lombok.*;
import io.swagger.v3.oas.annotations.media.Schema;
import java.io.Serializable;
import java.util.List;
import java.util.Map;
import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.constraints.*;

@Schema(description = "robot bên ngoài (Bot) sự tổng hợp DTO")
public class BotDTO {

    // ========== 1. SearchBot (robot tìm kiếm) ==========

    // Tương ứng với /api/v1/searchbots/ask
    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    @Schema(description = "SearchBot Đặt một câu hỏi")
    public static class SearchAskReq implements Serializable {
        @Schema(description = "Sự cố người dùng", requiredMode = Schema.RequiredMode.REQUIRED, example = "What is RAG?")
        @NotBlank(message = "Câu hỏi không thể trống")
        @JsonProperty("question")
        private String question;

        @Schema(description = "Có trả lại một tài liệu tham khảo hay không", defaultValue = "false")
        @JsonProperty("quote")
        @Builder.Default
        private Boolean quote = false;

        @Schema(description = "Có phát trực tuyến trả lại hay không", defaultValue = "true")
        @JsonProperty("stream")
        @Builder.Default
        private Boolean stream = true;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    @Schema(description = "SearchBot Trả lời câu hỏi")
    public static class SearchAskVO implements Serializable {
        @Schema(description = "Nội dung trả lời")
        @JsonProperty("answer")
        private String answer;

        @Schema(description = "Nguồn trích dẫn (Value Cấu trúc thường tương ứng với RetrievalDTO.HitVO)")
        @JsonProperty("reference")
        private Map<String, Object> reference;
    }

    // Tương ứng với /api/v1/searchbots/rel_questions
    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    @Schema(description = "Yêu cầu câu hỏi liên quan")
    public static class RelatedQuestionReq implements Serializable {
        @Schema(description = "Sự cố người dùng", requiredMode = Schema.RequiredMode.REQUIRED)
        @NotBlank(message = "Câu hỏi không thể trống")
        @JsonProperty("question")
        private String question;
    }

    // Tương ứng với /api/v1/searchbots/mindmap
    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    @Schema(description = "Yêu cầu bản đồ tư duy")
    public static class MindMapReq implements Serializable {
        @Schema(description = "Sự cố người dùng", requiredMode = Schema.RequiredMode.REQUIRED)
        @NotBlank(message = "Câu hỏi không thể trống")
        @JsonProperty("question")
        private String question;
    }

    // =========== 2. AgentBot (Tác nhân được nhúng) ==========

    // Tương ứng với /api/v1/agentbots/{id}/inputs
    @Data
    @Builder
    @AllArgsConstructor
    @Schema(description = "AgentBot Yêu cầu tham số đầu vào")
    public static class AgentInputsReq implements Serializable {
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    @Schema(description = "AgentBot Các tham số đầu vào xác định phản hồi")
    public static class AgentInputsVO implements Serializable {
        @Schema(description = "Danh sách định nghĩa biến biểu mẫu")
        @JsonProperty("variables")
        private List<Map<String, Object>> variables;
    }

    // Tương ứng với /api/v1/agentbots/{id}/completions
    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    @Schema(description = "AgentBot Yêu cầu hội thoại")
    public static class AgentCompletionReq implements Serializable {
        @Schema(description = "Nhập giá trị tham số")
        @JsonProperty("inputs")
        private Map<String, Object> inputs;

        @Schema(description = "Truy vấn của người dùng", requiredMode = Schema.RequiredMode.REQUIRED)
        @NotBlank(message = "Nội dung truy vấn không thể trống")
        @JsonProperty("question")
        private String question;

        @Schema(description = "Có phát trực tuyến trả lại hay không", defaultValue = "true")
        @JsonProperty("stream")
        @Builder.Default
        private Boolean stream = true;

        @Schema(description = "phiên ID")
        @JsonProperty("session_id")
        private String sessionId;
    }
}
