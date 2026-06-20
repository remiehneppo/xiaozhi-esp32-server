package xiaozhi.modules.knowledge.dto.agent;

import lombok.*;
import io.swagger.v3.oas.annotations.media.Schema;
import java.io.Serializable;
import java.util.List;
import java.util.Map;
import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.constraints.*;

@Schema(description = "đại lý (Agent) Quản lý tổng hợp DTO")
public class AgentDTO {

    // ========== 1. Quản lý tác nhân (CRUD) - Giải thích chi tiết về giao diện RAGFlow_Agent tương ứng ===========
    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    @Schema(description = "Agent Tạo yêu cầu")
    public static class CreateReq implements Serializable {
        @Schema(description = "Agent Tiêu đề", requiredMode = Schema.RequiredMode.REQUIRED, example = "My Agent")
        @NotBlank(message = "Agent Tiêu đề không thể trống")
        @JsonProperty("title")
        private String title;

        @Schema(description = "DSL độ nét (vải vẽ JSON)", requiredMode = Schema.RequiredMode.REQUIRED)
        @NotNull(message = "DSL Định nghĩa không thể trống")
        @JsonProperty("dsl")
        private Map<String, Object> dsl;

        @Schema(description = "Mô tả", example = "đây là một bài kiểm tra Agent")
        @JsonProperty("description")
        private String description;

        @Schema(description = "hình đại diện URL", example = "http://example.com/avatar.png")
        @JsonProperty("avatar")
        private String avatar;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    @Schema(description = "Agent yêu cầu cập nhật")
    public static class UpdateReq implements Serializable {
        @Schema(description = "Agent Tiêu đề", example = "Updated Agent")
        @JsonProperty("title")
        private String title;

        @Schema(description = "DSL độ nét (vải vẽ JSON)")
        @JsonProperty("dsl")
        private Map<String, Object> dsl;

        @Schema(description = "Mô tả")
        @JsonProperty("description")
        private String description;

        @Schema(description = "hình đại diện URL")
        @JsonProperty("avatar")
        private String avatar;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    @Schema(description = "Agent yêu cầu danh sách")
    public static class ListReq implements Serializable {
        @Schema(description = "Số trang", defaultValue = "1")
        @JsonProperty("page")
        @Builder.Default
        private Integer page = 1;

        @Schema(description = "kích thước trang", defaultValue = "10")
        @JsonProperty("page_size")
        @Builder.Default
        private Integer pageSize = 10;

        @Schema(description = "trường sắp xếp", defaultValue = "update_time")
        @JsonProperty("orderby")
        @Builder.Default
        private String orderby = "update_time";

        @Schema(description = "Có thứ tự giảm dần", defaultValue = "true")
        @JsonProperty("desc")
        @Builder.Default
        private Boolean desc = true;

        @Schema(description = "Agent ID bộ lọc")
        @JsonProperty("id")
        private String id;

        @Schema(description = "Tìm kiếm mờ tiêu đề")
        @JsonProperty("title")
        private String title;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    @Schema(description = "Agent đối tượng phản hồi")
    public static class AgentVO implements Serializable {
        @Schema(description = "Agent ID")
        @JsonProperty("id")
        private String id;

        @Schema(description = "Tiêu đề")
        @JsonProperty("title")
        private String title;

        @Schema(description = "Mô tả")
        @JsonProperty("description")
        private String description;

        @Schema(description = "hình đại diện")
        @JsonProperty("avatar")
        private String avatar;

        @Schema(description = "DSL độ nét")
        @JsonProperty("dsl")
        private Map<String, Object> dsl;

        @Schema(description = "Người sáng tạo ID")
        @JsonProperty("user_id")
        private String userId;

        @Schema(description = "Phân loại vải")
        @JsonProperty("canvas_category")
        private String canvasCategory;

        @Schema(description = "thời gian sáng tạo (Dấu thời gian)")
        @JsonProperty("create_time")
        private Long createTime;

        @Schema(description = "Thời gian cập nhật (Dấu thời gian)")
        @JsonProperty("update_time")
        private Long updateTime;
    }

    // ========== 2. Gỡ lỗi và theo dõi Webhook - giải thích chi tiết về giao diện RAGFlow_Agent tương ứng ===========
    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    @Schema(description = "Webhook yêu cầu kích hoạt (Động lực tham số)")
    public static class WebhookTriggerReq implements Serializable {
        @Schema(description = "biến đầu vào", requiredMode = Schema.RequiredMode.REQUIRED)
        @NotNull(message = "Biến đầu vào không được để trống")
        @JsonProperty("inputs")
        private Map<String, Object> inputs;

        @Schema(description = "từ truy vấn", example = "Hello")
        @JsonProperty("query")
        private String query;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    @Schema(description = "Webhook Yêu cầu theo dõi")
    public static class WebhookTraceReq implements Serializable {
        @Schema(description = "con trỏ dấu thời gian", example = "1700000000.0")
        @JsonProperty("since_ts")
        private Double sinceTs;

        @Schema(description = "Webhook ID")
        @JsonProperty("webhook_id")
        private String webhookId;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    @Schema(description = "Webhook Theo dõi phản hồi")
    public static class WebhookTraceVO implements Serializable {
        @Schema(description = "Webhook ID")
        @JsonProperty("webhook_id")
        private String webhookId;

        @Schema(description = "Kết thúc rồi à?")
        @JsonProperty("finished")
        private Boolean finished;

        @Schema(description = "con trỏ dấu thời gian cho truy vấn tiếp theo")
        @JsonProperty("next_since_ts")
        private Double nextSinceTs;

        @Schema(description = "danh sách sự kiện")
        @JsonProperty("events")
        private List<TraceEvent> events;

        @Data
        @Builder
        @NoArgsConstructor
        @AllArgsConstructor
        @Schema(description = "Theo dõi các mục sự kiện")
        public static class TraceEvent implements Serializable {
            @Schema(description = "Dấu thời gian")
            @JsonProperty("ts")
            private Double ts;

            @Schema(description = "loại sự kiện")
            @JsonProperty("event")
            private String event;

            @Schema(description = "dữ liệu sự kiện")
            @JsonProperty("data")
            private Object data;
        }
    }

    // ========== 3. Agent Session (Session) - Giải thích chi tiết về giao diện RAGFlow_Agent_Dify tương ứng ===========
    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    @Schema(description = "Session Tạo yêu cầu")
    public static class SessionCreateReq implements Serializable {
        @Schema(description = "người dùng ID")
        @JsonProperty("user_id")
        private String userId;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    @Schema(description = "Session yêu cầu danh sách")
    public static class SessionListReq implements Serializable {
        @Schema(description = "Số trang", defaultValue = "1")
        @JsonProperty("page")
        @Builder.Default
        private Integer page = 1;

        @Schema(description = "kích thước trang", defaultValue = "10")
        @JsonProperty("page_size")
        @Builder.Default
        private Integer pageSize = 10;

        @Schema(description = "trường sắp xếp", defaultValue = "create_time")
        @JsonProperty("orderby")
        @Builder.Default
        private String orderby = "create_time";

        @Schema(description = "Có thứ tự giảm dần", defaultValue = "true")
        @JsonProperty("desc")
        @Builder.Default
        private Boolean desc = true;

        @Schema(description = "Session ID")
        @JsonProperty("id")
        private String id;

        @Schema(description = "người dùng ID")
        @JsonProperty("user_id")
        private String userId;

        @Schema(description = "Có nên quay lại không DSL")
        @JsonProperty("dsl")
        @Builder.Default
        private Boolean dsl = false;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    @Schema(description = "Session Yêu cầu xóa hàng loạt")
    public static class SessionBatchDeleteReq implements Serializable {
        @Schema(description = "phiên ID danh sách", requiredMode = Schema.RequiredMode.REQUIRED)
        @JsonProperty("ids")
        @NotEmpty(message = "IDDanh sách không thể trống")
        private List<String> ids;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    @Schema(description = "Session đối tượng phản hồi")
    public static class SessionVO implements Serializable {
        @Schema(description = "Session ID")
        @JsonProperty("id")
        private String id;

        @Schema(description = "Agent ID")
        @JsonProperty("agent_id")
        private String agentId;

        @Schema(description = "người dùng ID")
        @JsonProperty("user_id")
        private String userId;

        @Schema(description = "Nguồn")
        @JsonProperty("source")
        private String source;

        @Schema(description = "DSL độ nét")
        @JsonProperty("dsl")
        private Map<String, Object> dsl;

        @Schema(description = "Danh sách tin nhắn")
        @JsonProperty("messages")
        private List<Map<String, Object>> messages;
    }

    // ========== 4. Đối thoại với Agent (Hoàn thành) - Giải thích chi tiết về giao diện RAGFlow_Agent_Dify tương ứng ===========
    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    @Schema(description = "Completion Yêu cầu hội thoại")
    public static class CompletionReq implements Serializable {
        @Schema(description = "phiên ID", requiredMode = Schema.RequiredMode.REQUIRED)
        @NotBlank(message = "phiên ID không thể trống")
        @JsonProperty("session_id")
        private String sessionId;

        @Schema(description = "Sự cố người dùng")
        @JsonProperty("question")
        private String question;

        @Schema(description = "Có phát trực tuyến trả lại hay không", defaultValue = "true")
        @JsonProperty("stream")
        @Builder.Default
        private Boolean stream = true;

        @Schema(description = "Có trả lại thông tin theo dõi hay không", defaultValue = "false")
        @JsonProperty("return_trace")
        @Builder.Default
        private Boolean returnTrace = false;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    @Schema(description = "Completion Phản hồi cuộc trò chuyện")
    public static class CompletionVO implements Serializable {
        @Schema(description = "phiên ID")
        @JsonProperty("id")
        private String id;

        @Schema(description = "Trả lời nội dung")
        @JsonProperty("content")
        private String content;

        @Schema(description = "Nguồn trích dẫn")
        @JsonProperty("reference")
        private Map<String, Object> reference;

        @Schema(description = "Thông tin theo dõi")
        @JsonProperty("trace")
        private List<Object> trace;
    }

    // ========== 5. Tìm kiếm tương thích Dify - giải thích chi tiết về giao diện RAGFlow_Agent_Dify tương ứng ===========
    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    @Schema(description = "Dify Yêu cầu tìm kiếm tương thích")
    public static class DifyRetrievalReq implements Serializable {
        @Schema(description = "cơ sở tri thức ID")
        @JsonProperty("knowledge_id")
        private String knowledgeId;

        @Schema(description = "từ truy vấn")
        @JsonProperty("query")
        private String query;

        @Schema(description = "Truy xuất cài đặt")
        @JsonProperty("retrieval_setting")
        private Map<String, Object> retrievalSetting;

        @Schema(description = "Bộ lọc siêu dữ liệu")
        @JsonProperty("metadata_condition")
        private Map<String, Object> metadataCondition;

        @Schema(description = "Có nên sử dụng biểu đồ tri thức hay không")
        @JsonProperty("use_kg")
        private Boolean useKg;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    @Schema(description = "Dify Phản hồi truy xuất tương thích")
    public static class DifyRetrievalVO implements Serializable {
        @Schema(description = "Danh sách kết quả tìm kiếm")
        @JsonProperty("records")
        private List<Record> records;

        @Data
        @Builder
        @NoArgsConstructor
        @AllArgsConstructor
        @Schema(description = "Truy xuất hồ sơ")
        public static class Record implements Serializable {
            @Schema(description = "nội dung")
            @JsonProperty("content")
            private String content;

            @Schema(description = "điểm tương đồng")
            @JsonProperty("score")
            private Double score;

            @Schema(description = "Tiêu đề")
            @JsonProperty("title")
            private String title;

            @Schema(description = "Siêu dữ liệu")
            @JsonProperty("metadata")
            private Map<String, Object> metadata;
        }
    }
}
