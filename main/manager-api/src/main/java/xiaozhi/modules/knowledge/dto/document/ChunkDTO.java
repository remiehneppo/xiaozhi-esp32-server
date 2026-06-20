package xiaozhi.modules.knowledge.dto.document;

import lombok.*;
import io.swagger.v3.oas.annotations.media.Schema;
import java.io.Serializable;
import java.util.List;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import jakarta.validation.constraints.*;

/**
 * DTO tổng hợp quản lý lát cắt
 */
@Schema(description = "Tổng hợp quản lý lát cắt DTO")
@JsonIgnoreProperties(ignoreUnknown = true)
public class ChunkDTO {

    /**
     * Đã thêm tham số yêu cầu lát
     */
    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    @Schema(description = "Đã thêm tham số yêu cầu lát")
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class AddReq implements Serializable {
        private static final long serialVersionUID = 1L;

        @Schema(description = "nội dung lát", requiredMode = Schema.RequiredMode.REQUIRED)
        @NotBlank(message = "Nội dung lát cắt không được để trống")
        private String content;

        @Schema(description = "Danh sách từ khóa quan trọng")
        @JsonProperty("important_keywords")
        private List<String> importantKeywords;

        @Schema(description = "Danh sách câu hỏi mặc định")
        private List<String> questions;
    }

    /**
     * Cập nhật tham số yêu cầu lát
     */
    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    @Schema(description = "Cập nhật tham số yêu cầu lát")
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class UpdateReq implements Serializable {
        private static final long serialVersionUID = 1L;

        @Schema(description = "Nội dung lát cắt mới")
        private String content;

        @Schema(description = "Cập nhật danh sách từ khóa (Ghi đè danh sách ban đầu)")
        @JsonProperty("important_keywords")
        private List<String> importantKeywords;

        @Schema(description = "kích hoạt/Vô hiệu hóa (true: kích hoạt, false: Vô hiệu hóa)")
        private Boolean available;
    }

    /**
     * Nhận tham số yêu cầu danh sách lát
     */
    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    @Schema(description = "Nhận tham số yêu cầu danh sách lát")
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class ListReq implements Serializable {
        private static final long serialVersionUID = 1L;

        @Schema(description = "Số trang (Mặc định 1)")
        private Integer page;

        @Schema(description = "Số lượng mỗi trang (Mặc định 30)")
        @JsonProperty("page_size")
        private Integer pageSize;

        @Schema(description = "Tìm kiếm từ khóa (Tìm kiếm toàn văn)")
        private String keywords;

        @Schema(description = "Cắt chính xác ID")
        private String id;
    }

    /**
     * Xóa các tham số yêu cầu lát theo lô
     */
    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    @Schema(description = "Xóa các tham số yêu cầu lát theo lô")
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class RemoveReq implements Serializable {
        private static final long serialVersionUID = 1L;

        @Schema(description = "lát ID danh sách", requiredMode = Schema.RequiredMode.REQUIRED)
        @JsonProperty("chunk_ids")
        @NotEmpty(message = "látIDDanh sách không thể trống")
        private List<String> chunkIds;
    }

    /**
     * Thông tin lát tài liệu VO
     */
    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    @Schema(description = "Thông tin lát tài liệu")
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class InfoVO implements Serializable {
        private static final long serialVersionUID = 1L;

        @Schema(description = "lát ID (Thông thường document_id + chỉ mục)", requiredMode = Schema.RequiredMode.REQUIRED)
        private String id;

        @Schema(description = "Cắt nội dung văn bản (Đối tượng chính của tìm kiếm toàn văn)", requiredMode = Schema.RequiredMode.REQUIRED)
        private String content;

        @Schema(description = "Tài liệu thuộc sở hữu ID", requiredMode = Schema.RequiredMode.REQUIRED)
        @JsonProperty("document_id")
        private String documentId;

        @Schema(description = "Tên tài liệu / từ khóa")
        @JsonProperty("docnm_kwd")
        private String docnmKwd;

        @Schema(description = "Danh sách từ khóa quan trọng (Được sử dụng cho tìm kiếm nâng cao từ khóa)")
        @JsonProperty("important_keywords")
        private List<String> importantKeywords;

        @Schema(description = "Danh sách câu hỏi mặc định (dùng cho Q&A Cải tiến chế độ)")
        private List<String> questions;

        @Schema(description = "Hình ảnh liên quan ID")
        @JsonProperty("image_id")
        private String imageId;

        @Schema(description = "Cơ sở tri thức thuộc về ID")
        @JsonProperty("dataset_id")
        private String datasetId;

        @Schema(description = "Miếng này có sẵn không? (true: Tham gia tìm kiếm, false: bị vô hiệu hóa)")
        private Boolean available;

        @Schema(description = "Danh sách chỉ mục vị trí của slice trong văn bản gốc (RAGFlowTrả về mảng lồng nhau, Chẳng hạn như [[start, end, filename]])")
        private List<List<Object>> positions;

        @Schema(description = "Token ID danh sách")
        @JsonProperty("token")
        private List<Integer> token;
    }

    /**
     * Phản hồi tổng hợp về danh sách được chia nhỏ
     */
    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    @Schema(description = "Phản hồi tổng hợp về danh sách được chia nhỏ")
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class ListVO implements Serializable {
        private static final long serialVersionUID = 1L;

        @Schema(description = "Danh sách thông tin lát")
        private List<InfoVO> chunks;

        @Schema(description = "Chi tiết tài liệu liên quan")
        private DocumentDTO.InfoVO doc;

        @Schema(description = "Tổng số hồ sơ")
        private Long total;
    }
}
