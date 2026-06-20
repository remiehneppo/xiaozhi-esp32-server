package xiaozhi.modules.knowledge.dto.chat;

import lombok.*;
import io.swagger.v3.oas.annotations.media.Schema;
import java.io.Serializable;
import java.util.List;
import java.util.Map;
import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.constraints.*;

/**
 * DTO tổng hợp quản lý hộp thoại
 * <p>
 * Lớp vùng chứa chứa tất cả các đối tượng yêu cầu/phản hồi cho trợ lý hộp thoại, phiên và tin nhắn.
 * </p>
 */
@Schema(description = "Tổng hợp quản lý hội thoại DTO")
public class ChatDTO {

    // =========== 1. Liên quan đến Trợ lý hội thoại (Trợ lý/Bot) ==========

    /**
     * Cấu hình từ nhắc nhở
     */
    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    @Schema(description = "Cấu hình từ nhắc nhở")
    public static class PromptConfig implements Serializable {

        @Schema(description = "Lời nhắc hệ thống", example = "Bạn là trợ lý dịch vụ khách hàng chuyên nghiệp...")
        @JsonProperty("prompt")
        private String systemPrompt;

        @Schema(description = "phát biểu khai mạc", example = "xin chào，Tôi là trợ lý thông minh của bạn，Tôi có thể giúp gì cho bạn?？")
        private String opener;

        @Schema(description = "Trả lời kết quả trống", example = "xin lỗi，Tôi không tìm thấy thông tin liên quan。")
        @JsonProperty("empty_response")
        private String emptyResponse;

        @Schema(description = "Có hiển thị tài liệu tham khảo hay không", example = "true")
        @JsonProperty("show_quote")
        private Boolean quote;

        @Schema(description = "Có bật hay không TTS", example = "false")
        private Boolean tts;

        @Schema(description = "ngưỡng tương tự (0.0 - 1.0)", example = "0.2")
        @JsonProperty("similarity_threshold")
        private Float similarityThreshold;

        @Schema(description = "Trọng số tương tự của từ khóa (0.0 - 1.0)", example = "0.7")
        @JsonProperty("keywords_similarity_weight")
        private Float vectorSimilarityWeight;

        @Schema(description = "Tìm kiếm Top N", example = "6")
        @JsonProperty("top_n")
        private Integer topK;

        @Schema(description = "Rerank người mẫu", example = "rerank_model_001")
        @JsonProperty("rerank_model")
        private String rerankId;

        @Schema(description = "Có bật tối ưu hóa hội thoại nhiều vòng hay không", example = "false")
        @JsonProperty("refine_multiturn")
        private Boolean refineMultigraph;

        @Schema(description = "danh sách biến")
        private List<Map<String, Object>> variables;
    }

    /**
     * Cấu hình LLM
     */
    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    @Schema(description = "LLM Cấu hình mô hình")
    public static class LLMConfig implements Serializable {

        @NotBlank(message = "Tên mẫu không được để trống")
        @Schema(description = "Tên mẫu", requiredMode = Schema.RequiredMode.REQUIRED, example = "gpt-4")
        @JsonProperty("model_name")
        private String modelName;

        @Schema(description = "Thông số nhiệt độ (0.0 - 2.0)", example = "0.7")
        private Float temperature;

        @Schema(description = "Top P lấy mẫu", example = "0.9")
        @JsonProperty("top_p")
        private Float topP;

        @Schema(description = "tối đa Token con số", example = "4096")
        @JsonProperty("max_tokens")
        private Integer maxTokens;

        @Schema(description = "Có sự trừng phạt", example = "0.0")
        @JsonProperty("presence_penalty")
        private Float presencePenalty;

        @Schema(description = "hình phạt tần số", example = "0.0")
        @JsonProperty("frequency_penalty")
        private Float frequencyPenalty;
    }

    /**
     * Tạo yêu cầu trợ giúp
     */
    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    @Schema(description = "Tạo yêu cầu trợ giúp")
    public static class AssistantCreateReq implements Serializable {

        @NotBlank(message = "Tên trợ lý không được để trống")
        @Schema(description = "Tên trợ lý", requiredMode = Schema.RequiredMode.REQUIRED, example = "Trợ lý dịch vụ khách hàng thông minh")
        private String name;

        @Schema(description = "Hình đại diện trợ lý (Base64 mã hóa)", example = "")
        private String avatar;

        @Schema(description = "cơ sở kiến thức liên quan ID danh sách", example = "[\"kb_001\", \"kb_002\"]")
        @JsonProperty("dataset_ids")
        private List<String> datasetIds;

        @Schema(description = "Mô tả trợ lý", example = "Đây là trợ lý dịch vụ khách hàng thông minh")
        private String description;

        @Schema(description = "LLM Cấu hình mô hình")
        @JsonProperty("llm")
        private LLMConfig llm;

        @Schema(description = "Cấu hình từ nhắc nhở")
        @JsonProperty("prompt")
        private PromptConfig promptConfig;
    }

    /**
     * Cập nhật yêu cầu trợ lý
     */
    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    @Schema(description = "Cập nhật yêu cầu trợ lý")
    public static class AssistantUpdateReq implements Serializable {

        @Schema(description = "Tên trợ lý", example = "Trợ lý dịch vụ khách hàng thông minh V2")
        private String name;

        @Schema(description = "Hình đại diện trợ lý (Base64 mã hóa)", example = "")
        private String avatar;

        @Schema(description = "cơ sở kiến thức liên quan ID danh sách", example = "[\"kb_001\", \"kb_002\"]")
        @JsonProperty("dataset_ids")
        private List<String> datasetIds;

        @Schema(description = "Mô tả trợ lý", example = "Đây là trợ lý dịch vụ khách hàng thông minh")
        private String description;

        @Schema(description = "LLM Cấu hình mô hình")
        @JsonProperty("llm")
        private LLMConfig llm;

        @Schema(description = "Cấu hình từ nhắc nhở")
        @JsonProperty("prompt")
        private PromptConfig promptConfig;
    }

    /**
     * Yêu cầu danh sách hỗ trợ truy vấn
     */
    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    @Schema(description = "Yêu cầu danh sách hỗ trợ truy vấn")
    public static class AssistantListReq implements Serializable {

        @Schema(description = "Số trang (từ 1 bắt đầu)", example = "1")
        private Integer page;

        @Schema(description = "Số lượng mỗi trang", example = "30")
        @JsonProperty("page_size")
        private Integer pageSize;

        @Schema(description = "Lọc theo tên (kết hợp mờ)", example = "dịch vụ khách hàng")
        private String name;

        @Schema(description = "trường sắp xếp: create_time / update_time", example = "create_time")
        private String orderby;

        @Schema(description = "Có thứ tự giảm dần", example = "true")
        private Boolean desc;

        @Schema(description = "nhấn ID Lọc chính xác", example = "assistant_001")
        private String id;
    }

    /**
     * Chi tiết trợ lý VO
     */
    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    @Schema(description = "Thông tin chi tiết về trợ lý VO")
    public static class AssistantVO implements Serializable {

        @Schema(description = "Trợ lý ID", example = "assistant_001")
        private String id;

        @Schema(description = "người thuê nhà ID", example = "tenant_001")
        @JsonProperty("tenant_id")
        private String tenantId;

        @Schema(description = "Tên trợ lý", example = "Trợ lý dịch vụ khách hàng thông minh")
        private String name;

        @Schema(description = "Hình đại diện trợ lý", example = "")
        private String avatar;

        @Schema(description = "cơ sở kiến thức liên quan ID danh sách")
        @JsonProperty("dataset_ids")
        private List<String> datasetIds;

        @Schema(description = "Danh sách cơ sở kiến thức liên quan (Chi tiết)")
        private List<SimpleDatasetVO> datasets;

        @Schema(description = "Mô tả trợ lý")
        private String description;

        @Schema(description = "LLM Cấu hình mô hình")
        @JsonProperty("llm")
        private LLMConfig llm;

        @Schema(description = "Cấu hình từ nhắc nhở")
        @JsonProperty("prompt")
        private PromptConfig promptConfig;

        @Schema(description = "thời gian sáng tạo (Dấu thời gian)", example = "1700000000000")
        @JsonProperty("create_time")
        private Long createTime;

        @Schema(description = "Thời gian cập nhật (Dấu thời gian)", example = "1700000001000")
        @JsonProperty("update_time")
        private Long updateTime;
    }

    /**
     * Xóa yêu cầu trợ giúp
     */
    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    @Schema(description = "Xóa yêu cầu trợ giúp")
    public static class AssistantDeleteReq implements Serializable {

        @Schema(description = "Trợ lý để xóa ID danh sách", example = "[\"assistant_001\", \"assistant_002\"]")
        private List<String> ids;
    }

    // ========== 2. Liên quan đến phiên ==========

    /**
     * Tạo yêu cầu phiên
     */
    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    @Schema(description = "Tạo yêu cầu phiên")
    public static class SessionCreateReq implements Serializable {

        @Schema(description = "tên phiên", example = "Buổi tư vấn kỹ thuật")
        private String name;

        @Schema(description = "người dùng ID", example = "user_001")
        @JsonProperty("user_id")
        private String userId;
    }

    /**
     * Yêu cầu phiên cập nhật
     */
    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    @Schema(description = "Yêu cầu phiên cập nhật")
    public static class SessionUpdateReq implements Serializable {

        @Schema(description = "tên phiên", example = "Buổi tư vấn kỹ thuật - cập nhật")
        private String name;
    }

    /**
     * Yêu cầu danh sách phiên truy vấn
     */
    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    @Schema(description = "Yêu cầu danh sách phiên truy vấn")
    public static class SessionListReq implements Serializable {

        @Schema(description = "Trợ lý ID", example = "assistant_001")
        @JsonProperty("assistant_id")
        private String assistantId;

        @Schema(description = "Số trang (từ 1 bắt đầu)", example = "1")
        private Integer page;

        @Schema(description = "Số lượng mỗi trang", example = "30")
        @JsonProperty("page_size")
        private Integer pageSize;

        @Schema(description = "Lọc theo tên", example = "công nghệ")
        private String name;

        @Schema(description = "trường sắp xếp", example = "create_time")
        private String orderby;

        @Schema(description = "Có thứ tự giảm dần", example = "true")
        private Boolean desc;

        @Schema(description = "phiên ID Lọc chính xác", example = "session_001")
        private String id;

        @Schema(description = "Lọc ID người dùng", example = "user_001")
        @JsonProperty("user_id")
        private String userId;
    }

    /**
     * Chi tiết phiên VO
     */
    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    @Schema(description = "Chi tiết phiên VO")
    public static class SessionVO implements Serializable {

        @Schema(description = "phiên ID", example = "session_001")
        private String id;

        @Schema(description = "Trợ lý ID", example = "assistant_001")
        @JsonProperty("chat_id")
        private String chatId;

        @Schema(description = "Trợ lý ID (Tương thích với các phiên bản cũ hơn)", example = "assistant_001")
        @JsonProperty("assistant_id")
        private String assistantId;

        @Schema(description = "tên phiên", example = "Buổi tư vấn kỹ thuật")
        private String name;

        @Schema(description = "thời gian sáng tạo (Dấu thời gian)", example = "1700000000000")
        @JsonProperty("create_time")
        private Long createTime;

        @Schema(description = "Thời gian cập nhật (Dấu thời gian)", example = "1700000001000")
        @JsonProperty("update_time")
        private Long updateTime;

        @Schema(description = "Ngày tạo", example = "2024-05-01 10:00:00")
        @JsonProperty("create_date")
        private String createDate;

        @Schema(description = "ngày cập nhật", example = "2024-05-01 10:00:00")
        @JsonProperty("update_date")
        private String updateDate;

        @Schema(description = "người dùng ID", example = "user_001")
        @JsonProperty("user_id")
        private String userId;

        @Schema(description = "Danh sách tin nhắn lịch sử hội thoại")
        private List<Map<String, Object>> messages;
    }

    /**
     * Xóa yêu cầu phiên
     */
    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    @Schema(description = "Xóa yêu cầu phiên")
    public static class SessionDeleteReq implements Serializable {

        @Schema(description = "cuộc trò chuyện cần xóa ID danh sách", example = "[\"session_001\", \"session_002\"]")
        private List<String> ids;
    }

    // ========== 3. Tin nhắn/Cuộc trò chuyện (Hoàn thành) liên quan ===========

    /**
     * Gửi yêu cầu tin nhắn
     */
    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    @Schema(description = "Gửi yêu cầu tin nhắn")
    public static class CompletionReq implements Serializable {

        @NotBlank(message = "Nội dung câu hỏi không được để trống")
        @Schema(description = "Sự cố người dùng", requiredMode = Schema.RequiredMode.REQUIRED, example = "Hãy giới thiệu sản phẩm của bạn")
        private String question;

        @Schema(description = "Có nên sử dụng phản hồi phát trực tuyến hay không (SSE)", example = "true")
        @Builder.Default
        private Boolean stream = true;

        @NotBlank(message = "phiên ID không thể trống")
        @Schema(description = "phiên ID (Tùy chọn，Nếu không được thông qua, một phiên mới sẽ được tạo.)", example = "session_001")
        @JsonProperty("session_id")
        private String sessionId;

        @Schema(description = "Có hiển thị tài liệu tham khảo hay không", example = "true")
        private Boolean quote;

        @Schema(description = "Chỉ định tài liệu để lấy ID danh sách (được phân tách bằng dấu phẩy)", example = "doc_001,doc_002")
        @JsonProperty("doc_ids")
        private String docIds;

        @Schema(description = "Bộ lọc siêu dữ liệu")
        @JsonProperty("metadata_condition")
        private Map<String, Object> metadataCondition;
    }

    /**
     * Phản hồi tin nhắn VO
     */
    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    @Schema(description = "phản hồi tin nhắn VO")
    public static class CompletionVO implements Serializable {

        @Schema(description = "AI Nội dung trả lời")
        private String answer;

        @Schema(description = "Thông tin trích dẫn")
        private Reference reference;

        @Schema(description = "phiên ID", example = "session_001")
        @JsonProperty("session_id")
        private String sessionId;

        @Schema(description = "Nhiệm vụ ID (Để theo dõi phản hồi trực tuyến)", example = "task_001")
        @JsonProperty("task_id")
        private String taskId;

        /**
         * Thông tin trích dẫn (truy xuất kết quả truy xuất)
         */
        @Data
        @NoArgsConstructor
        @AllArgsConstructor
        @Builder
        @Schema(description = "Thông tin trích dẫn")
        public static class Reference implements Serializable {

            @Schema(description = "Danh sách các khối tài liệu lần truy cập")
            private List<xiaozhi.modules.knowledge.dto.document.RetrievalDTO.HitVO> chunks;

            @Schema(description = "Thông tin tổng hợp tài liệu")
            @JsonProperty("doc_aggs")
            private List<DocAgg> docAggs;
        }

        /**
         * Thông tin tổng hợp tài liệu
         */
        @Data
        @NoArgsConstructor
        @AllArgsConstructor
        @Builder
        @Schema(description = "Thông tin tổng hợp tài liệu")
        public static class DocAgg implements Serializable {

            @Schema(description = "Tài liệu ID", example = "doc_001")
            @JsonProperty("doc_id")
            private String docId;

            @Schema(description = "Tên tài liệu", example = "Hướng dẫn sử dụng sản phẩm.pdf")
            @JsonProperty("doc_name")
            private String docName;

            @Schema(description = "Số lượt truy cập", example = "3")
            private Integer count;
        }
    }

    /**
     * Cơ sở kiến thức đơn giản VO (dành cho danh sách Trợ lý)
     */
    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    @Schema(description = "Cơ sở kiến thức đơn giản VO")
    public static class SimpleDatasetVO implements Serializable {
        @Schema(description = "cơ sở tri thức ID")
        private String id;
        @Schema(description = "Tên cơ sở kiến thức")
        private String name;
        @Schema(description = "hình đại diện")
        private String avatar;
        @Schema(description = "Số lượng khối")
        @JsonProperty("chunk_num")
        private Integer chunkNum;
    }
}
