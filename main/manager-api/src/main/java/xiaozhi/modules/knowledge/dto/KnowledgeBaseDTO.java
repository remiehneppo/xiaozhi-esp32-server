package xiaozhi.modules.knowledge.dto;

import java.io.Serial;
import java.io.Serializable;
import java.util.Date;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

@Data
@Schema(description = "Cơ sở kiến thứcCơ sở kiến thức")
public class KnowledgeBaseDTO implements Serializable {

    @Serial
    private static final long serialVersionUID = 1L;

    @Schema(description = "mã định danh duy nhất")
    private String id;

    @Schema(description = "cơ sở tri thứcID")
    private String datasetId;

    @Schema(description = "RAGCấu hình mô hìnhID")
    private String ragModelId;

    @Schema(description = "Tên cơ sở kiến thức")
    private String name;

    @Schema(description = "Hình đại diện cơ sở kiến thức(Base64)")
    private String avatar;

    @Schema(description = "Mô tả cơ sở kiến thức")
    private String description;

    @Schema(description = "Nhúng tên mẫu")
    private String embeddingModel;

    @Schema(description = "Cài đặt quyền: me/team")
    private String permission;

    @Schema(description = "Phương pháp chia nhỏ")
    private String chunkMethod;

    @Schema(description = "Cấu hình trình phân tích cú pháp(JSON String)")
    private String parserConfig;

    @Schema(description = "Tổng số khối")
    private Long chunkCount;

    @Schema(description = "tổng cộngTokencon số")
    private Long tokenNum;

    @Schema(description = "Trạng thái(0:Vô hiệu hóa 1:kích hoạt)")
    private Integer status;

    @Schema(description = "Người sáng tạo")
    private Long creator;

    @Schema(description = "thời gian sáng tạo")
    private Date createdAt;

    @Schema(description = "Trình cập nhật")
    private Long updater;

    @Schema(description = "Thời gian cập nhật")
    private Date updatedAt;

    @Schema(description = "Số lượng tài liệu")
    private Integer documentCount;
}