package xiaozhi.modules.knowledge.dto.document;

import lombok.*;
import io.swagger.v3.oas.annotations.media.Schema;
import java.io.Serializable;
import java.util.List;
import java.util.Map;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonAlias;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import jakarta.validation.constraints.*;

/**
 * Tổng hợp quản lý tài liệu DTO
 */
@Schema(description = "Tổng hợp quản lý tài liệu DTO")
@JsonIgnoreProperties(ignoreUnknown = true)
public class DocumentDTO {

    /**
     * Tải lên các thông số yêu cầu tài liệu
     */
    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    @Schema(description = "Tải lên các thông số yêu cầu tài liệu")
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class UploadReq implements Serializable {
        private static final long serialVersionUID = 1L;

        @Schema(description = "cơ sở tri thức ID (Thuộc tính phải được chỉ định)", requiredMode = Schema.RequiredMode.REQUIRED)
        @JsonProperty("dataset_id")
        @NotBlank(message = "cơ sở tri thứcIDkhông thể trống")
        private String datasetId;

        @Schema(description = "tên tập tin (Nếu được chỉ định，sau đó ghi đè lên tên file gốc)")
        private String name;

        @Schema(description = "Phương pháp chia nhỏ")
        @JsonProperty("chunk_method")
        private DocumentDTO.InfoVO.ChunkMethod chunkMethod;

        @Schema(description = "Cấu hình tham số phân tích cú pháp")
        @JsonProperty("parser_config")
        private DocumentDTO.InfoVO.ParserConfig parserConfig;

        @Schema(description = "Đường dẫn thư mục ảo (Mặc định là /)")
        @JsonProperty("parent_path")
        private String parentPath;

        @Schema(description = "trường siêu dữ liệu")
        @JsonProperty("meta")
        private Map<String, Object> metaFields;

        @Schema(description = "luồng nhị phân của tập tin (hỗ trợ PDF, DOCX, TXT, MD và các định dạng khác)", requiredMode = Schema.RequiredMode.REQUIRED)
        @NotNull(message = "Tệp tải lên không được để trống")
        private org.springframework.web.multipart.MultipartFile file;
    }

    /**
     * Cập nhật các tham số yêu cầu tài liệu
     */
    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    @Schema(description = "Cập nhật các tham số yêu cầu tài liệu")
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class UpdateReq implements Serializable {
        private static final long serialVersionUID = 1L;

        @Schema(description = "Tên tài liệu mới (Phải chứa hậu tố tập tin，và không thể thay đổi loại ban đầu)")
        private String name;

        @Schema(description = "kích hoạt/trạng thái khuyết tật (true: kích hoạt, false: Vô hiệu hóa; Không tham gia truy xuất sau khi bị vô hiệu hóa)")
        private Boolean enabled;

        @Schema(description = "Phương pháp phân tích mới (Việc sửa đổi điều này sẽ đặt lại trạng thái phân tích cú pháp)")
        @JsonProperty("chunk_method")
        private InfoVO.ChunkMethod chunkMethod;

        @Schema(description = "Cấu hình chi tiết trình phân tích cú pháp mới (Nên ở bên chunk_method Được sử dụng cùng nhau)")
        @JsonProperty("parser_config")
        private InfoVO.ParserConfig parserConfig;
    }

    /**
     * Nhận tham số yêu cầu danh sách tài liệu
     */
    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    @Schema(description = "Nhận tham số yêu cầu danh sách tài liệu")
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class ListReq implements Serializable {
        private static final long serialVersionUID = 1L;

        @Schema(description = "Số trang (Mặc định: 1)")
        private Integer page;

        @Schema(description = "Số lượng mỗi trang (Mặc định: 30)")
        @JsonProperty("page_size")
        private Integer pageSize;

        @Schema(description = "trường sắp xếp (Tùy chọn: create_time, name, size; Mặc định: create_time)")
        private String orderby;

        @Schema(description = "Có sắp xếp theo thứ tự giảm dần hay không (true: Mới nhất/lớn nhất đầu tiên; false: lâu đời nhất/nhỏ nhất đầu tiên; Mặc định: true)")
        private Boolean desc;

        @Schema(description = "Lọc chính xác: Tài liệu ID")
        private String id;

        @Schema(description = "Lọc chính xác: Tên đầy đủ của tài liệu (có hậu tố)")
        private String name;

        @Schema(description = "tìm kiếm mờ: Từ khóa tên tài liệu")
        private String keywords;

        @Schema(description = "Lọc: Danh sách hậu tố tập tin (Chẳng hạn như ['pdf', 'docx'])")
        private List<String> suffix;

        @Schema(description = "Lọc: Danh sách trạng thái đang chạy")
        private List<InfoVO.RunStatus> run;

        @Schema(description = "Lọc: Bắt đầu thời gian tạo (Dấu thời gian, mili giây)")
        @JsonProperty("create_time_from")
        private Long createTimeFrom;

        @Schema(description = "Lọc: kết thúc thời gian tạo (Dấu thời gian, mili giây)")
        @JsonProperty("create_time_to")
        private Long createTimeTo;
    }

    /**
     * Các tham số yêu cầu thao tác tài liệu hàng loạt (để xóa, phân tích cú pháp, v.v.)
     */
    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    @Schema(description = "Tham số yêu cầu vận hành tài liệu hàng loạt")
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class BatchIdReq implements Serializable {
        private static final long serialVersionUID = 1L;

        @Schema(description = "Tài liệu ID danh sách", requiredMode = Schema.RequiredMode.REQUIRED)
        @JsonProperty("ids") // để tương thích，Bạn cũng có thể xem xét hỗ trợ document_ids，Nhưng ở đây tất cả đều được gọi là ids
        @JsonAlias("document_ids")
        @NotEmpty(message = "Tài liệuIDDanh sách không thể trống")
        private List<String> ids;
    }

    /**
     * Thông tin tài liệu cơ sở kiến thức VO
     */
    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    @Schema(description = "Thông tin tài liệu cơ sở kiến thức")
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class InfoVO implements Serializable {
        private static final long serialVersionUID = 1L;

        @Schema(description = "Tài liệu ID (mã định danh duy nhất)", requiredMode = Schema.RequiredMode.REQUIRED)
        private String id;

        @Schema(description = "Hình thu nhỏ tài liệu URL (Base64 hoặc liên kết)")
        private String thumbnail;

        @Schema(description = "Cơ sở tri thức thuộc về ID", requiredMode = Schema.RequiredMode.REQUIRED)
        @JsonProperty("dataset_id")
        private String datasetId;

        @Schema(description = "Phương pháp phân tích tài liệu (Xác định cách tài liệu được cắt lát)")
        @JsonProperty("chunk_method")
        private ChunkMethod chunkMethod;

        @Schema(description = "liên quan ETL Pipeline ID (Nếu có)")
        @JsonProperty("pipeline_id")
        private String pipelineId;

        @Schema(description = "Cấu hình chi tiết của trình phân tích tài liệu")
        @JsonProperty("parser_config")
        private ParserConfig parserConfig;

        @Schema(description = "Loại nguồn (Chẳng hạn như local, s3, url Đợi đã)")
        @JsonProperty("source_type")
        private String sourceType;

        @Schema(description = "Loại tệp tài liệu (Chẳng hạn như pdf, docx, txt)", requiredMode = Schema.RequiredMode.REQUIRED)
        private String type;

        @Schema(description = "Người dùng sáng tạo ID")
        @JsonProperty("created_by")
        private String createdBy;

        @Schema(description = "Tên tài liệu (Chứa phần mở rộng)", requiredMode = Schema.RequiredMode.REQUIRED)
        private String name;

        @Schema(description = "Đường dẫn lưu trữ tệp hoặc mã định danh vị trí")
        private String location;

        @Schema(description = "kích thước tập tin (đơn vị: Bytes)")
        private Long size;

        @Schema(description = "bao gồm Token tổng cộng (Thống kê sau khi phân tích)")
        @JsonProperty("token_count")
        private Long tokenCount;

        @Schema(description = "Chứa các lát (Chunk) tổng cộng")
        @JsonProperty("chunk_count")
        private Long chunkCount;

        @Schema(description = "Tiến trình phân tích cú pháp (0.0 ~ 1.0, 1.0 Cho biết sự hoàn thành)")
        private Double progress;

        @Schema(description = "Mô tả tiến trình hiện tại hoặc thông báo lỗi")
        @JsonProperty("progress_msg")
        private String progressMsg;

        @Schema(description = "Dấu thời gian khi quá trình xử lý bắt đầu (RAGFlowTrở lạiRFC1123định dạng)")
        @JsonProperty("process_begin_at")
        private String processBeginAt;

        @Schema(description = "Tổng thời gian xử lý (đơn vị: giây)")
        @JsonProperty("process_duration")
        private Double processDuration;

        @Schema(description = "Trường siêu dữ liệu tùy chỉnh (Key-Value cặp giá trị khóa)")
        @JsonProperty("meta_fields")
        private Map<String, Object> metaFields;

        @Schema(description = "Phần mở rộng tập tin (Không bao gồm dấu chấm)")
        private String suffix;

        @Schema(description = "Trạng thái đang chạy phân tích tài liệu")
        private RunStatus run;

        @Schema(description = "Tình trạng sẵn có của tài liệu (1: kích hoạt/bình thường, 0: Vô hiệu hóa/không hợp lệ)", requiredMode = Schema.RequiredMode.REQUIRED)
        private String status;

        @Schema(description = "thời gian sáng tạo (Dấu thời gian, mili giây)", requiredMode = Schema.RequiredMode.REQUIRED)
        @JsonProperty("create_time")
        private Long createTime;

        @Schema(description = "Ngày tạo (RAGFlowTrở lạiRFC1123định dạng)")
        @JsonProperty("create_date")
        private String createDate;

        @Schema(description = "Cập nhật lần cuối (Dấu thời gian, mili giây)")
        @JsonProperty("update_time")
        private Long updateTime;

        @Schema(description = "ngày cập nhật lần cuối (RAGFlowTrở lạiRFC1123định dạng)")
        @JsonProperty("update_date")
        private String updateDate;

        /**
         * Phân tích phương thức liệt kê (ChunkMethod)
         */
        public enum ChunkMethod {
            @Schema(description = "Chế độ chung: Hoạt động với hầu hết văn bản thuần túy hoặc tài liệu hỗn hợp")
            @JsonProperty("naive")
            NAIVE,
            @Schema(description = "chế độ thủ công: Cho phép người dùng chỉnh sửa các lát cắt theo cách thủ công")
            @JsonProperty("manual")
            MANUAL,
            @Schema(description = "Chế độ hỏi đáp: Tối ưu hóa đặc biệt Q&A định dạng tài liệu")
            @JsonProperty("qa")
            QA,
            @Schema(description = "chế độ bảng: Tối ưu hóa đặc biệt Excel hoặc CSV Chờ dữ liệu bảng")
            @JsonProperty("table")
            TABLE,
            @Schema(description = "Chế độ tiểu luận: Tối ưu hóa cho định dạng bài viết học thuật")
            @JsonProperty("paper")
            PAPER,
            @Schema(description = "chế độ sách: Tối ưu hóa cho cấu trúc chương sách")
            @JsonProperty("book")
            BOOK,
            @Schema(description = "Mô hình pháp lý và quy định: Tối ưu hóa cấu trúc các quy định pháp luật")
            @JsonProperty("laws")
            LAWS,
            @Schema(description = "Chế độ trình bày: Mục tiêu PPT Đang chờ tối ưu hóa tệp trình bày")
            @JsonProperty("presentation")
            PRESENTATION,
            @Schema(description = "Chế độ hình ảnh: Nội dung hình ảnh mục tiêu OCR và mô tả")
            @JsonProperty("picture")
            PICTURE,
            @Schema(description = "mô hình tổng thể: Coi toàn bộ tài liệu như một lát cắt")
            @JsonProperty("one")
            ONE,
            @Schema(description = "Mô hình đồ thị tri thức: Trích xuất các mối quan hệ thực thể để xây dựng biểu đồ")
            @JsonProperty("knowledge_graph")
            KNOWLEDGE_GRAPH,
            @Schema(description = "Chế độ email: Tối ưu hóa cho các định dạng email")
            @JsonProperty("email")
            EMAIL;
        }

        /**
         * Bảng liệt kê RunStatus (RunStatus)
         */
        public enum RunStatus {
            @Schema(description = "Chưa bắt đầu: Đang chờ hàng đợi phân tích cú pháp")
            @JsonProperty("UNSTART")
            UNSTART,
            @Schema(description = "Đang tiến hành: Phân tích cú pháp hoặc lập chỉ mục")
            @JsonProperty("RUNNING")
            RUNNING,
            @Schema(description = "Đã hủy: Người dùng hủy thủ công")
            @JsonProperty("CANCEL")
            CANCEL,
            @Schema(description = "Đã hoàn thành: Đã phân tích cú pháp thành công")
            @JsonProperty("DONE")
            DONE,
            @Schema(description = "thất bại: Đã xảy ra lỗi trong quá trình phân tích cú pháp")
            @JsonProperty("FAIL")
            FAIL;
        }

        /**
         * Mô hình nhận thức về bố cục Enum
         */
        public enum LayoutRecognize {
            @Schema(description = "Mô hình hiểu tài liệu sâu: Thích hợp cho việc sắp chữ phức tạp")
            @JsonProperty("DeepDOC")
            DeepDOC,
            @Schema(description = "mô hình quy tắc đơn giản: Thích hợp cho văn bản thuần túy")
            @JsonProperty("Simple")
            Simple;
        }

        @Data
        @Builder
        @NoArgsConstructor
        @AllArgsConstructor
        @Schema(description = "Cấu hình tham số trình phân tích cú pháp tài liệu")
        @JsonIgnoreProperties(ignoreUnknown = true)
        public static class ParserConfig implements Serializable {
            private static final long serialVersionUID = 1L;

            @Schema(description = "Cắt lát tối đa Token con số (Giá trị đề xuất: 512, 1024, 2048)")
            @JsonProperty("chunk_token_num")
            private Integer chunkTokenNum;

            @Schema(description = "dấu phân cách đoạn văn (Hỗ trợ ký tự thoát, Chẳng hạn như \\n)")
            private String delimiter;

            @Schema(description = "mô hình nhận dạng bố cục (DeepDOC/Simple)")
            @JsonProperty("layout_recognize")
            private LayoutRecognize layoutRecognize;

            @Schema(description = "liệu có nên Excel Chuyển đổi thành HTML bàn")
            @JsonProperty("html4excel")
            private Boolean html4excel;

            @Schema(description = "Tự động trích xuất số lượng từ khóa (0 Cho biết không trích xuất)")
            @JsonProperty("auto_keywords")
            private Integer autoKeywords;

            @Schema(description = "Tự động tạo số lượng câu hỏi (0 Cho biết không tạo ra)")
            @JsonProperty("auto_questions")
            private Integer autoQuestions;

            @Schema(description = "Tự động tạo số lượng nhãn")
            @JsonProperty("topn_tags")
            private Integer topnTags;

            @Schema(description = "RAPTOR Cấu hình chỉ mục nâng cao")
            private RaptorConfig raptor;

            @Schema(description = "GraphRAG Cấu hình sơ đồ tri thức")
            @JsonProperty("graphrag")
            private GraphRagConfig graphRag;

            @Data
            @Builder
            @NoArgsConstructor
            @AllArgsConstructor
            @Schema(description = "RAPTOR (Chỉ số tóm tắt đệ quy) Cấu hình")
            @JsonIgnoreProperties(ignoreUnknown = true)
            public static class RaptorConfig implements Serializable {
                private static final long serialVersionUID = 1L;
                @Schema(description = "Có bật hay không RAPTOR chỉ mục")
                @JsonProperty("use_raptor")
                private Boolean useRaptor;
            }

            @Data
            @Builder
            @NoArgsConstructor
            @AllArgsConstructor
            @Schema(description = "GraphRAG (Truy xuất nâng cao đồ thị) Cấu hình")
            @JsonIgnoreProperties(ignoreUnknown = true)
            public static class GraphRagConfig implements Serializable {
                private static final long serialVersionUID = 1L;
                @Schema(description = "Có bật hay không GraphRAG chỉ mục")
                @JsonProperty("use_graphrag")
                private Boolean useGraphRag;
            }
        }
    }
}
