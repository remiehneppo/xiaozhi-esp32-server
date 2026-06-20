package xiaozhi.modules.knowledge.dto.dataset;

import lombok.*;
import io.swagger.v3.oas.annotations.media.Schema;
import java.io.Serializable;
import java.util.List;
import java.util.Map;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonInclude;
import jakarta.validation.constraints.*;

/**
 * DTO tổng hợp quản lý cơ sở tri thức
 * <p>
 * Lớp vùng chứa chứa các định nghĩa lớp nội bộ tĩnh cho tất cả các đối tượng yêu cầu/phản hồi của mô-đun cơ sở kiến thức.
 * </p>
 */
@Schema(description = "Tổng hợp quản lý cơ sở tri thức DTO")
@JsonIgnoreProperties(ignoreUnknown = true)
public class DatasetDTO {

    // ========== Các lớp bên trong chung ===========

    /**
     * Cấu hình trình phân tích cú pháp
     */
    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    @Schema(description = "Cấu hình trình phân tích cú pháp")
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class ParserConfig implements Serializable {

        @Schema(description = "Cắt nhỏ token số lượng", example = "128")
        @JsonProperty("chunk_token_num")
        private Integer chunkTokenNum;

        @Schema(description = "dấu phân cách", example = "\\n!?;。；！？")
        private String delimiter;

        @Schema(description = "mô hình nhận dạng bố cục: DeepDOC / Simple", example = "DeepDOC")
        @JsonProperty("layout_recognize")
        private String layoutRecognize;

        @Schema(description = "liệu có nên Excel chuyển đổi thành HTML", example = "false")
        private Boolean html4excel;

        @Schema(description = "Tự động tạo số lượng từ khóa (0 có nghĩa là đóng cửa)", example = "0")
        @JsonProperty("auto_keywords")
        private Integer autoKeywords;

        @Schema(description = "Tự động tạo số lượng câu hỏi (0 có nghĩa là đóng cửa)", example = "0")
        @JsonProperty("auto_questions")
        private Integer autoQuestions;
    }

    // ========== Yêu cầu lớp ===========

    /**
     * Tạo yêu cầu cơ sở kiến thức (giao diện ánh xạ 1: tạo)
     */
    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    @Schema(description = "Tạo yêu cầu cơ sở kiến thức")
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class CreateReq implements Serializable {

        @NotBlank(message = "Tên cơ sở kiến thức không được để trống")
        @Schema(description = "Tên cơ sở kiến thức", requiredMode = Schema.RequiredMode.REQUIRED, example = "my_dataset")
        private String name;

        @Schema(description = "Hình đại diện cơ sở kiến thức (Base64 mã hóa)", example = "")
        private String avatar;

        @Schema(description = "Mô tả cơ sở kiến thức", example = "Dùng để lưu trữ tài liệu sản phẩm")
        private String description;

        @Schema(description = "Nhúng tên mẫu", example = "BAAI/bge-large-zh-v1.5")
        @JsonProperty("embedding_model")
        private String embeddingModel;

        @Schema(description = "Cài đặt quyền: me / team", example = "me")
        private String permission;

        @Schema(description = "Phương pháp chia nhỏ: naive / manual / qa / table / paper / book / laws / presentation / picture / one / knowledge_graph / email", example = "naive")
        @JsonProperty("chunk_method")
        private String chunkMethod;

        @Schema(description = "Cấu hình trình phân tích cú pháp")
        @JsonProperty("parser_config")
        private ParserConfig parserConfig;
    }

    /**
     * Yêu cầu cập nhật cơ sở tri thức (giao diện ánh xạ 4: cập nhật)
     */
    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    @Schema(description = "Yêu cầu cập nhật cơ sở kiến thức")
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class UpdateReq implements Serializable {

        @Schema(description = "Tên cơ sở kiến thức", example = "updated_dataset")
        private String name;

        @Schema(description = "Hình đại diện cơ sở kiến thức (Base64 mã hóa)", example = "")
        private String avatar;

        @Schema(description = "Mô tả cơ sở kiến thức", example = "Đã cập nhật mô tả")
        private String description;

        @Schema(description = "Cài đặt quyền: me / team", example = "team")
        private String permission;

        @Schema(description = "Nhúng tên mẫu", example = "BAAI/bge-large-zh-v1.5")
        @JsonProperty("embedding_model")
        private String embeddingModel;

        @Schema(description = "Phương pháp chia nhỏ: naive / manual / qa / table / paper / book / laws / presentation / picture / one / knowledge_graph / email", example = "naive")
        @JsonProperty("chunk_method")
        private String chunkMethod;

        @Schema(description = "Cấu hình trình phân tích cú pháp")
        @JsonProperty("parser_config")
        private ParserConfig parserConfig;

        @JsonInclude(JsonInclude.Include.NON_NULL)
        @Schema(description = "PageRank trọng lượng (0-100)", example = "50")
        private Integer pagerank;
    }

    /**
     * Truy vấn yêu cầu danh sách cơ sở kiến thức (giao diện ánh xạ 3: list_datasets)
     */
    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    @Schema(description = "Truy vấn Yêu cầu danh sách cơ sở kiến thức")
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class ListReq implements Serializable {

        @Schema(description = "Số trang (từ 1 bắt đầu)", example = "1")
        private Integer page;

        @Schema(description = "Số lượng mỗi trang", example = "30")
        @JsonProperty("page_size")
        private Integer pageSize;

        @Schema(description = "trường sắp xếp: create_time / update_time", example = "create_time")
        private String orderby;

        @Schema(description = "Có thứ tự giảm dần", example = "true")
        private Boolean desc;

        @Schema(description = "Lọc theo tên (kết hợp mờ)", example = "my_dataset")
        private String name;

        @Schema(description = "Theo cơ sở tri thức ID bộ lọc", example = "abc123")
        private String id;
    }

    /**
     * Xóa hàng loạt yêu cầu cơ sở tri thức (giao diện ánh xạ 2: xóa)
     */
    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    @Schema(description = "Xóa hàng loạt yêu cầu cơ sở kiến thức")
    public static class BatchIdReq implements Serializable {

        @NotNull(message = "cơ sở tri thức ID Danh sách không thể trống")
        @Size(min = 1, message = "Cần có ít nhất một nền tảng kiến thức ID")
        @Schema(description = "cơ sở tri thức ID danh sách", requiredMode = Schema.RequiredMode.REQUIRED, example = "[\"id1\", \"id2\"]")
        private List<String> ids;
    }

    /**
     * Chạy yêu cầu GraphRAG
     */
    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    @Schema(description = "chạy GraphRAG Yêu cầu")
    public static class RunGraphRagReq implements Serializable {

        @Schema(description = "Danh sách loại thực thể", example = "[\"person\", \"organization\"]")
        @JsonProperty("entity_types")
        private List<String> entityTypes;

        @Schema(description = "Phương pháp xây dựng: light / fast / full", example = "light")
        private String method;
    }

    /**
     * Chạy yêu cầu RAPTOR
     */
    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    @Schema(description = "chạy RAPTOR Yêu cầu")
    public static class RunRaptorReq implements Serializable {

        @Schema(description = "Số lượng cụm tối đa", example = "64")
        @JsonProperty("max_cluster")
        private Integer maxCluster;

        @Schema(description = "Từ nhắc nhở tùy chỉnh", example = "Xin tóm tắt như sau...")
        private String prompt;
    }

    /**
     * ID không đồng bộ phản hồi nhiệm vụ VO (giao diện ánh xạ 7/8: run_graphrag/run_raptor)
     */
    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    @Schema(description = "không đồng bộID nhiệm vụ phản ứng")
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class TaskIdVO implements Serializable {

        @Schema(description = "GraphRAG ID nhiệm vụ", example = "task_uuid_12345678")
        @JsonProperty("graphrag_task_id")
        private String graphragTaskId;

        @Schema(description = "RAPTOR ID nhiệm vụ", example = "task_uuid_87654321")
        @JsonProperty("raptor_task_id")
        private String raptorTaskId;
    }

    // ========== Lớp phản hồi ===========

    /**
     * Chi tiết cơ sở kiến thức VO (trả về các mục dữ liệu của 1/3 giao diện ánh xạ)
     */
    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    @Schema(description = "Chi tiết cơ sở kiến thức VO")
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class InfoVO implements Serializable {

        @Schema(description = "cơ sở tri thức ID", example = "abc123")
        private String id;

        @Schema(description = "Tên cơ sở kiến thức", example = "my_dataset")
        private String name;

        @Schema(description = "Hình đại diện cơ sở kiến thức (Base64 mã hóa)", example = "")
        private String avatar;

        @Schema(description = "người thuê nhà ID", example = "tenant_001")
        @JsonProperty("tenant_id")
        private String tenantId;

        @Schema(description = "Mô tả cơ sở kiến thức", example = "Dùng để lưu trữ tài liệu sản phẩm")
        private String description;

        @Schema(description = "Nhúng tên mẫu", example = "BAAI/bge-large-zh-v1.5")
        @JsonProperty("embedding_model")
        private String embeddingModel;

        @Schema(description = "Cài đặt quyền: me / team", example = "me")
        private String permission;

        @Schema(description = "Phương pháp chia nhỏ", example = "naive")
        @JsonProperty("chunk_method")
        private String chunkMethod;

        @Schema(description = "Cấu hình trình phân tích cú pháp")
        @JsonProperty("parser_config")
        private ParserConfig parserConfig;

        @Schema(description = "Tổng số khối", example = "1024")
        @JsonProperty("chunk_count")
        private Long chunkCount;

        @Schema(description = "Tổng số tài liệu", example = "50")
        @JsonProperty("document_count")
        private Long documentCount;

        @Schema(description = "Thời gian tạo (timestamp)", example = "1700000000000")
        @JsonProperty("create_time")
        private Long createTime;

        @Schema(description = "Thời gian cập nhật (timestamp)", example = "1700000001000")
        @JsonProperty("update_time")
        private Long updateTime;

        @Schema(description = "tổng cộng Token con số", example = "102400")
        @JsonProperty("token_num")
        private Long tokenNum;

        @Schema(description = "Ngày tạo (định dạng: yyyy-MM-dd HH:mm:ss)")
        @JsonProperty("create_date")
        private String createDate;

        @Schema(description = "ngày cập nhật lần cuối (định dạng: yyyy-MM-dd HH:mm:ss)")
        @JsonProperty("update_date")
        private String updateDate;
    }

    /**
     * VO phản hồi thao tác hàng loạt
     */
    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    @Schema(description = "VO phản hồi thao tác hàng loạt")
    public static class BatchOperationVO implements Serializable {

        @Schema(description = "Số lượng thao tác thành công", example = "5")
        @JsonProperty("success_count")
        private Integer successCount;

        @Schema(description = "Danh sách lỗi")
        private List<Object> errors;
    }

    // ========== Liên quan đến Đồ thị tri thức ==========

    /**
     * VO dữ liệu Đồ thị tri thức (ánh xạ giao diện 5: knowledge_graph)
     */
    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    @Schema(description = "Dữ liệu biểu đồ tri thức VO")
    public static class GraphVO implements Serializable {

        @Schema(description = "Danh sách nút đồ thị")
        private List<Node> nodes;

        @Schema(description = "Danh sách cạnh đồ thị")
        private List<Edge> edges;

        @Schema(description = "Dữ liệu sơ đồ tư duy")
        @JsonProperty("mind_map")
        private Map<String, Object> mindMap;

        /**
         * Nút đồ thị
         */
        @Data
        @NoArgsConstructor
        @AllArgsConstructor
        @Builder
        @Schema(description = "Nút đồ thị")
        @JsonIgnoreProperties(ignoreUnknown = true)
        public static class Node implements Serializable {

            @Schema(description = "ID nút", example = "node_001")
            private String id;

            @Schema(description = "Nhãn nút", example = "Sản phẩm")
            private String label;

            @Schema(description = "Giá trị PageRank", example = "0.85")
            private Double pagerank;

            @Schema(description = "Màu sắc nút", example = "#FF5733")
            private String color;

            @Schema(description = "URL hình ảnh nút", example = "https://example.com/icon.png")
            private String img;
        }

        /**
         * Cạnh đồ thị
         */
        @Data
        @NoArgsConstructor
        @AllArgsConstructor
        @Builder
        @Schema(description = "Cạnh đồ thị")
        @JsonIgnoreProperties(ignoreUnknown = true)
        public static class Edge implements Serializable {

            @Schema(description = "nguồnID nút", example = "node_001")
            private String source;

            @Schema(description = "mục tiêuID nút", example = "node_002")
            private String target;

            @Schema(description = "Trọng số cạnh", example = "0.75")
            private Double weight;

            @Schema(description = "Nhãn cạnh (mô tả quan hệ)", example = "Thuộc về")
            private String label;
        }
    }

    // ========== Theo dõi nhiệm vụ bất đồng bộ (GraphRAG/RAPTOR) ==========

    /**
     * VO theo dõi nhiệm vụ bất đồng bộ (ánh xạ giao diện 9/10: trả về tiến độ nhiệm vụ)
     */
    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    @Schema(description = "Theo dõi tác vụ không đồng bộ VO")
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class TaskTraceVO implements Serializable {

        @Schema(description = "ID nhiệm vụ", example = "task_001")
        private String id;

        @Schema(description = "ID tài liệu", example = "doc_001")
        @JsonProperty("doc_id")
        private String docId;

        @Schema(description = "Số trang bắt đầu", example = "1")
        @JsonProperty("from_page")
        private Integer fromPage;

        @Schema(description = "Số trang kết thúc", example = "10")
        @JsonProperty("to_page")
        private Integer toPage;

        @Schema(description = "Phần trăm tiến độ (0.0 - 1.0)", example = "0.75")
        private Double progress;

        @Schema(description = "Thông báo tiến độ", example = "Đang xử lý 5 trang...")
        @JsonProperty("progress_msg")
        private String progressMsg;

        @Schema(description = "Thời gian tạo (timestamp)", example = "1700000000000")
        @JsonProperty("create_time")
        private Long createTime;

        @Schema(description = "Thời gian cập nhật (timestamp)", example = "1700000001000")
        @JsonProperty("update_time")
        private Long updateTime;
    }
}
