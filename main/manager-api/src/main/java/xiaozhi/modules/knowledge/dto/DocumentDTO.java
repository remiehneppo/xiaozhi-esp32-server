package xiaozhi.modules.knowledge.dto;

import java.io.Serializable;
import java.util.Date;
import java.util.Map;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

/**
 * Tài liệu DTO
 */
@Data
@Schema(description = "Tài liệu cơ sở tri thức")
public class DocumentDTO implements Serializable {
    private static final long serialVersionUID = 1L;

    @Schema(description = "địa phươngID")
    private String id;

    @Schema(description = "cơ sở tri thứcID")
    private String datasetId;

    @Schema(description = "RAGFlowTài liệuID")
    private String documentId;

    @Schema(description = "Tên tài liệu")
    private String name;

    @Schema(description = "kích thước tập tin")
    private Long size;

    @Schema(description = "Loại tệp")
    private String type;

    @Schema(description = "Phương pháp chia nhỏ")
    private String chunkMethod;

    @Schema(description = "Cấu hình phân tích")
    private Map<String, Object> parserConfig;

    @Schema(description = "Trạng thái xử lý (1:Phân tích cú pháp 3:sự thành công 4:thất bại)")
    private Integer status;

    @Schema(description = "thông báo lỗi")
    private String error;

    @Schema(description = "Số lượng khối")
    private Integer chunkCount;

    @Schema(description = "Tokensố lượng")
    private Long tokenCount;

    @Schema(description = "Có bật hay không")
    private Integer enabled;

    @Schema(description = "thời gian sáng tạo")
    private Date createdAt;

    @Schema(description = "Thời gian cập nhật")
    private Date updatedAt;

    @Schema(description = "Tiến trình tải lên (trường ảo)")
    private Double progress;

    @Schema(description = "hình thu nhỏ/Xem trước (trường ảo)")
    private String thumbnail;
}
