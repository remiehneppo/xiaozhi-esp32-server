package xiaozhi.modules.knowledge.entity;

import java.io.Serializable;
import java.util.Date;

import com.baomidou.mybatisplus.annotation.FieldFill;
import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

/**
 * Bảng tài liệu (Shadow DB cho tài liệu RAGFlow)
 * Tên bảng tương ứng: ai_know_document
 */
@Data
@TableName(value = "ai_rag_knowledge_document", autoResultMap = true)
@Schema(description = "Bảng tài liệu cơ sở kiến thức")
public class DocumentEntity implements Serializable {
    private static final long serialVersionUID = 1L;

    @TableId(type = IdType.ASSIGN_UUID)
    @Schema(description = "Chỉ địa phươngID")
    private String id;

    @Schema(description = "cơ sở tri thứcID (hiệp hội ai_rag_dataset.dataset_id)")
    private String datasetId;

    @Schema(description = "RAGFlowTài liệuID (từ xaID)")
    private String documentId;

    @Schema(description = "Tên tài liệu")
    private String name;

    @Schema(description = "kích thước tập tin(Bytes)")
    private Long size;

    @Schema(description = "Loại tệp(pdf/doc/txtĐợi đã)")
    private String type;

    @Schema(description = "Phương pháp chia nhỏ")
    private String chunkMethod;

    @Schema(description = "Cấu hình phân tích(JSON String)")
    private String parserConfig;

    @Schema(description = "Trạng thái sẵn có (1: kích hoạt/bình thường, 0: Vô hiệu hóa/không hợp lệ)")
    private String status;

    @Schema(description = "Trạng thái chạy (UNSTART/RUNNING/CANCEL/DONE/FAIL)")
    private String run;

    @Schema(description = "Tiến trình phân tích cú pháp (0.0 ~ 1.0)")
    private Double progress;

    @Schema(description = "hình thu nhỏ (Base64 hoặc URL)")
    private String thumbnail;

    @Schema(description = "Phân tích cần có thời gian (đơn vị: giây)")
    private Double processDuration;

    @Schema(description = "Siêu dữ liệu tùy chỉnh (JSON định dạng)")
    private String metaFields;

    @Schema(description = "Loại nguồn (local, s3, url Đợi đã)")
    private String sourceType;

    @Schema(description = "Phân tích thông báo lỗi")
    private String error;

    @Schema(description = "Số lượng khối")
    private Integer chunkCount;

    @Schema(description = "Tokensố lượng")
    private Long tokenCount;

    @Schema(description = "Có bật hay không (0:Vô hiệu hóa 1:kích hoạt)")
    private Integer enabled;

    @Schema(description = "Người sáng tạo")
    @TableField(fill = FieldFill.INSERT)
    private Long creator;

    @Schema(description = "thời gian sáng tạo")
    @TableField(fill = FieldFill.INSERT)
    private Date createdAt;

    @Schema(description = "Thời gian cập nhật")
    @TableField(fill = FieldFill.UPDATE)
    private Date updatedAt;

    @Schema(description = "Thời gian đồng bộ hóa mới nhất")
    private Date lastSyncAt;
}
