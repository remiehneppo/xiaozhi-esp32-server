package xiaozhi.modules.knowledge.dto.document;

import lombok.*;
import io.swagger.v3.oas.annotations.media.Schema;
import java.io.Serializable;
import java.util.List;
import java.util.Map;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import jakarta.validation.constraints.*;

/**
 * Tổng hợp quản lý siêu dữ liệu và truy xuất DTO
 */
@Schema(description = "Tổng hợp quản lý tìm kiếm và siêu dữ liệu DTO")
@JsonIgnoreProperties(ignoreUnknown = true)
public class RetrievalDTO {

    /**
     * Thông tin tổng hợp tài liệu (VO)
     */
    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    @Schema(description = "Thông tin tổng hợp tài liệu")
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class DocAggVO implements Serializable {
        private static final long serialVersionUID = 1L;

        @Schema(description = "Tên tài liệu")
        @JsonProperty("doc_name")
        private String docName;

        @Schema(description = "Tài liệu ID")
        @JsonProperty("doc_id")
        private String docId;

        @Schema(description = "số lượng")
        private Integer count;
    }

    /**
     * Truy xuất các tham số yêu cầu kiểm tra
     */
    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    @Schema(description = "Truy xuất các tham số yêu cầu kiểm tra")
    @JsonIgnoreProperties(ignoreUnknown = true)
    @JsonInclude(JsonInclude.Include.NON_NULL)
    public static class TestReq implements Serializable {
        private static final long serialVersionUID = 1L;

        @Schema(description = "cơ sở tri thức ID danh sách", requiredMode = Schema.RequiredMode.REQUIRED)
        @JsonProperty("dataset_ids")
        @NotEmpty(message = "cơ sở tri thứcIDDanh sách không thể trống")
        private List<String> datasetIds;

        @Schema(description = "Tài liệu ID danh sách (Tùy chọn，Được sử dụng để giới hạn phạm vi tìm kiếm)")
        @JsonProperty("document_ids")
        private List<String> documentIds;

        @Schema(description = "Tìm kiếm câu hỏi", requiredMode = Schema.RequiredMode.REQUIRED)
        @NotBlank(message = "Câu hỏi tìm kiếm không được để trống")
        private String question;

        @Schema(description = "Số trang (Mặc định 1)")
        private Integer page;

        @Schema(description = "Số lượng mỗi trang (Mặc định 10)")
        @JsonProperty("page_size")
        private Integer pageSize;

        @Schema(description = "ngưỡng tương tự (Mặc định 0.2)")
        @JsonProperty("similarity_threshold")
        private Float similarityThreshold;

        @Schema(description = "Trọng số tương tự của vectơ (Mặc định 0.3)")
        @JsonProperty("vector_similarity_weight")
        private Float vectorSimilarityWeight;

        @Schema(description = "Trở lại Top K lát (Mặc định 1024)")
        @JsonProperty("top_k")
        private Integer topK;

        @Schema(description = "mô hình sắp xếp lại ID")
        @JsonProperty("rerank_id")
        private String rerankId;

        @Schema(description = "Có làm nổi bật từ khóa hay không")
        private Boolean highlight;

        @Schema(description = "Có bật tìm kiếm từ khóa hay không")
        private Boolean keyword;

        @Schema(description = "Danh sách dịch đa ngôn ngữ (Tùy chọn)")
        @JsonProperty("cross_languages")
        private List<String> crossLanguages;

        @Schema(description = "Bộ lọc siêu dữ liệu (JSON vật thể)")
        @JsonProperty("metadata_condition")
        private Map<String, Object> metadataCondition;
    }

    /**
     * Truy xuất lượt truy cập (VO)
     */
    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    @Schema(description = "Truy xuất chi tiết lát truy cập")
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class HitVO implements Serializable {
        private static final long serialVersionUID = 1L;

        @Schema(description = "lát ID", requiredMode = Schema.RequiredMode.REQUIRED)
        private String id;

        @Schema(description = "nội dung lát", requiredMode = Schema.RequiredMode.REQUIRED)
        private String content;

        @Schema(description = "Tài liệu thuộc sở hữu ID", requiredMode = Schema.RequiredMode.REQUIRED)
        @JsonProperty("document_id")
        private String documentId;

        @Schema(description = "Cơ sở tri thức thuộc về ID")
        @JsonProperty("dataset_id")
        private String datasetId;

        @Schema(description = "Tên tài liệu")
        @JsonProperty("document_name")
        private String documentName;

        @Schema(description = "Từ khóa tài liệu")
        @JsonProperty("document_keyword")
        private String documentKeyword;

        @Schema(description = "Sự tương đồng toàn diện", requiredMode = Schema.RequiredMode.REQUIRED)
        private Float similarity;

        @Schema(description = "véc tơ tương tự")
        @JsonProperty("vector_similarity")
        private Float vectorSimilarity;

        @Schema(description = "độ tương tự từ khóa")
        @JsonProperty("term_similarity")
        private Float termSimilarity;

        @Schema(description = "vị trí chỉ số")
        private Integer index;

        @Schema(description = "Làm nổi bật nội dung")
        private String highlight;

        @Schema(description = "Danh sách từ khóa quan trọng")
        @JsonProperty("important_keywords")
        private List<String> importantKeywords;

        @Schema(description = "Danh sách câu hỏi mặc định")
        private List<String> questions;

        @Schema(description = "hình ảnh ID")
        @JsonProperty("image_id")
        private String imageId;

        @Schema(description = "chỉ số vị trí (RAGFlowTrả về mảng lồng nhau, Chẳng hạn như [[start, end, filename]])")
        private Object positions;
    }

    /**
     * Tóm tắt siêu dữ liệu cơ sở kiến thức (VO)
     */
    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    @Schema(description = "Thông tin tóm tắt siêu dữ liệu cơ sở kiến thức")
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class MetaSummaryVO implements Serializable {
        private static final long serialVersionUID = 1L;

        @Schema(description = "Tổng số tài liệu", requiredMode = Schema.RequiredMode.REQUIRED)
        @JsonProperty("total_doc_count")
        private Long totalDocCount;

        @Schema(description = "Token tổng cộng", requiredMode = Schema.RequiredMode.REQUIRED)
        @JsonProperty("total_token_count")
        private Long totalTokenCount;

        @Schema(description = "Phân phối loại tệp (key: hậu tố tập tin, value: số lượng)")
        @JsonProperty("file_type_distribution")
        private Map<String, Long> fileTypeDistribution;

        @Schema(description = "Phân phối trạng thái văn bản (key: mã trạng thái, value: số lượng)")
        @JsonProperty("status_distribution")
        private Map<String, Long> statusDistribution;

        @Schema(description = "Thống kê siêu dữ liệu tùy chỉnh (key: Tên trường, value: số lượng/giá trị)")
        @JsonProperty("custom_metadata")
        private Map<String, Object> customMetadata;
    }

    /**
     * Tham số yêu cầu siêu dữ liệu cập nhật hàng loạt
     */
    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    @Schema(description = "Tham số yêu cầu siêu dữ liệu cập nhật hàng loạt")
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class MetaBatchReq implements Serializable {
        private static final long serialVersionUID = 1L;

        @Schema(description = "bộ lọc: Được sử dụng để chỉ định phạm vi tài liệu sẽ được cập nhật (Mặc định tất cả)")
        private Selector selector;

        @Schema(description = "Danh sách siêu dữ liệu mới hoặc cập nhật")
        private List<UpdateItem> updates;

        @Schema(description = "Danh sách các khóa siêu dữ liệu cần xóa")
        private List<DeleteItem> deletes;

        /**
         * Bộ lọc tài liệu
         */
        @Data
        @Builder
        @NoArgsConstructor
        @AllArgsConstructor
        @Schema(description = "Bộ lọc cập nhật siêu dữ liệu")
        @JsonIgnoreProperties(ignoreUnknown = true)
        public static class Selector implements Serializable {
            private static final long serialVersionUID = 1L;

            @Schema(description = "Chỉ định tài liệu ID danh sách")
            @JsonProperty("document_ids")
            private List<String> documentIds;

            @Schema(description = "Khớp điều kiện siêu dữ liệu (key: Tên trường, value: giá trị phù hợp)")
            @JsonProperty("metadata_condition")
            private Map<String, Object> metadataCondition;
        }

        /**
         * Cập nhật mục
         */
        @Data
        @Builder
        @NoArgsConstructor
        @AllArgsConstructor
        @Schema(description = "Các mục cập nhật siêu dữ liệu")
        @JsonIgnoreProperties(ignoreUnknown = true)
        public static class UpdateItem implements Serializable {
            private static final long serialVersionUID = 1L;

            @Schema(description = "Tên khóa siêu dữ liệu", requiredMode = Schema.RequiredMode.REQUIRED)
            private String key;

            @Schema(description = "giá trị siêu dữ liệu", requiredMode = Schema.RequiredMode.REQUIRED)
            private Object value;
        }

        /**
         * Xóa mục
         */
        @Data
        @Builder
        @NoArgsConstructor
        @AllArgsConstructor
        @Schema(description = "xóa siêu dữ liệu")
        @JsonIgnoreProperties(ignoreUnknown = true)
        public static class DeleteItem implements Serializable {
            private static final long serialVersionUID = 1L;

            @Schema(description = "Tên khóa siêu dữ liệu sẽ bị xóa", requiredMode = Schema.RequiredMode.REQUIRED)
            private String key;
        }
    }

    /**
     * Thu hồi phản hồi tổng hợp kết quả kiểm tra
     */
    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    @Schema(description = "Thu hồi phản hồi tổng hợp kết quả kiểm tra")
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class ResultVO implements Serializable {
        private static final long serialVersionUID = 1L;

        @Schema(description = "Truy xuất danh sách các lát cắt")
        private List<HitVO> chunks;

        @Schema(description = "Thống kê phân phối tài liệu")
        @JsonProperty("doc_aggs")
        private List<DocAggVO> docAggs;

        @Schema(description = "Tổng số bản ghi hit")
        private Long total;
    }
}
