package xiaozhi.modules.knowledge.dto.common;

import lombok.*;
import io.swagger.v3.oas.annotations.media.Schema;
import java.io.Serializable;
import java.util.List;
import java.util.Map;
import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.constraints.*;

@Schema(description = "Các hàm mở rộng chung DTO")
public class CommonDTO {

    // =========== 1. Chi tiết trích dẫn (detail_share_embedded) ==========

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    @Schema(description = "Yêu cầu chi tiết tham khảo")
    public static class ReferenceDetailReq implements Serializable {
        @Schema(description = "lát ID", requiredMode = Schema.RequiredMode.REQUIRED)
        @NotBlank(message = "lát ID không thể trống")
        @JsonProperty("chunk_id")
        private String chunkId;

        @Schema(description = "cơ sở tri thức ID")
        @JsonProperty("knowledge_id")
        private String knowledgeId;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    @Schema(description = "Phản hồi chi tiết báo giá")
    public static class ReferenceDetailVO implements Serializable {
        @Schema(description = "lát ID")
        @JsonProperty("chunk_id")
        private String chunkId;

        @Schema(description = "nội dung đầy đủ")
        @JsonProperty("content_with_weight")
        private String contentWithWeight;

        @Schema(description = "Tên tài liệu")
        @JsonProperty("doc_name")
        private String docName;

        @Schema(description = "hình ảnh ID danh sách")
        @JsonProperty("img_id")
        private String imageId; // Lưu ý：RAGFlow đôi khi trở lại String đôi khi trở lại List，Cần xác nhận theo tình hình thực tế，dự kiến String dùng cho ID

        @Schema(description = "Tài liệu ID")
        @JsonProperty("doc_id")
        private String docId;
    }

    // =========== 2. Hỏi đáp chung (ask_about) - để gỡ lỗi ==========

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    @Schema(description = "Yêu cầu hỏi đáp chung (để gỡ lỗi)")
    public static class AskAboutReq implements Serializable {
        @Schema(description = "Sự cố người dùng", requiredMode = Schema.RequiredMode.REQUIRED, example = "What is this dataset about?")
        @NotBlank(message = "Câu hỏi không thể trống")
        @JsonProperty("question")
        private String question;

        @Schema(description = "Tập dữ liệu ID danh sách", requiredMode = Schema.RequiredMode.REQUIRED)
        @NotEmpty(message = "Danh sách tập dữ liệu không được để trống")
        @JsonProperty("dataset_ids")
        private List<String> datasetIds;
    }

    // Phản hồi thường sử dụng lại cấu trúc Chuỗi hoặc Bản đồ đơn giản, tùy thuộc vào cách triển khai cụ thể. Chưa có VO chuyên dụng nào được xác định.
}
