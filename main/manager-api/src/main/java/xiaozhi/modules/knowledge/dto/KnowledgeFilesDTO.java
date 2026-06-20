package xiaozhi.modules.knowledge.dto;

import java.io.Serial;
import java.io.Serializable;
import java.util.Date;
import java.util.Map;

import io.swagger.v3.oas.annotations.media.Schema;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.Data;

@Data
@Schema(description = "Tài liệu cơ sở tri thức")
@JsonIgnoreProperties(ignoreUnknown = true)
public class KnowledgeFilesDTO implements Serializable {

    @Serial
    private static final long serialVersionUID = 1L;
    @Schema(description = "mã định danh duy nhất")
    private String id;

    @Schema(description = "Tài liệuID")
    private String documentId;

    @Schema(description = "cơ sở tri thứcID")
    private String datasetId;

    @Schema(description = "Tên tài liệu")
    private String name;

    @Schema(description = "Loại tài liệu")
    private String fileType;

    @Schema(description = "kích thước tập tin（Byte）")
    private Long fileSize;

    @Schema(description = "đường dẫn tập tin")
    private String filePath;

    @Schema(description = "Tiến trình phân tích cú pháp (0.0 ~ 1.0)")
    private Double progress;

    @Schema(description = "hình thu nhỏ (Base64 hoặc URL)")
    private String thumbnail;

    @Schema(description = "Phân tích cần có thời gian (đơn vị: giây)")
    private Double processDuration;

    @Schema(description = "Loại nguồn (local, s3, url Đợi đã)")
    private String sourceType;

    @Schema(description = "trường siêu dữ liệu (Map định dạng)")
    private Map<String, Object> metaFields;

    @Schema(description = "Phương pháp chia nhỏ")
    private String chunkMethod;

    @Schema(description = "Cấu hình trình phân tích cú pháp")
    private Map<String, Object> parserConfig;

    @Schema(description = "Trạng thái sẵn có (1: kích hoạt/bình thường, 0: Vô hiệu hóa/không hợp lệ)")
    private String status;

    @Schema(description = "Trạng thái chạy (UNSTART/RUNNING/CANCEL/DONE/FAIL)")
    private String run;

    @Schema(description = "Người sáng tạo")
    private Long creator;

    @Schema(description = "thời gian sáng tạo")
    private Date createdAt;

    @Schema(description = "Trình cập nhật")
    private Long updater;

    @Schema(description = "Thời gian cập nhật")
    private Date updatedAt;

    @Schema(description = "Số lượng khối")
    private Integer chunkCount;

    @Schema(description = "Tokensố lượng")
    private Long tokenCount;

    @Schema(description = "Phân tích thông báo lỗi")
    private String error;

    // Định nghĩa hằng số trạng thái phân tích tài liệu
    private static final Integer STATUS_UNSTART = 0;
    private static final Integer STATUS_RUNNING = 1;
    private static final Integer STATUS_CANCEL = 2;
    private static final Integer STATUS_DONE = 3;
    private static final Integer STATUS_FAIL = 4;

    /**
     * Nhận mã trạng thái phân tích tài liệu (dựa trên chuyển đổi trường chạy)
     */
    public Integer getParseStatusCode() {
        if (run == null) {
            return STATUS_UNSTART;
        }

        // RAGFlow ánh xạ trực tiếp tới mã trạng thái tương ứng dựa trên giá trị của trường chạy.
        switch (run.toUpperCase()) {
            case "RUNNING":
                return STATUS_RUNNING;
            case "CANCEL":
                return STATUS_CANCEL;
            case "DONE":
                return STATUS_DONE;
            case "FAIL":
                return STATUS_FAIL;
            case "UNSTART":
            default:
                return STATUS_UNSTART;
        }
    }

}