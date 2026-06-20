package xiaozhi.modules.knowledge.entity;

import java.util.Date;

import com.baomidou.mybatisplus.annotation.FieldFill;
import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

@Data
@TableName(value = "ai_rag_dataset", autoResultMap = true)
@Schema(description = "Bảng cơ sở kiến thức cơ sở kiến thức")
public class KnowledgeBaseEntity {

    @TableId(type = IdType.ASSIGN_UUID)
    @Schema(description = "mã định danh duy nhất")
    private String id;

    @Schema(description = "cơ sở tri thứcID")
    private String datasetId;

//    @Deprecated
    @Schema(description = "RAGCấu hình mô hìnhID (kết nốiRAGFlowcon trỏ thông tin xác thực)")
    private String ragModelId;

    @Schema(description = "người thuê nhàID")
    private String tenantId;

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

    @Schema(description = "Tổng số tài liệu")
    private Long documentCount;

    @Schema(description = "tổng cộngTokencon số")
    private Long tokenNum;

    @Schema(description = "Trạng thái(0:Vô hiệu hóa 1:kích hoạt)")
    private Integer status;

    @Schema(description = "Người sáng tạo")
    @TableField(fill = FieldFill.INSERT)
    private Long creator;

    @Schema(description = "thời gian sáng tạo")
    @TableField(fill = FieldFill.INSERT)
    private Date createdAt;

    @Schema(description = "Trình cập nhật")
    @TableField(fill = FieldFill.UPDATE)
    private Long updater;

    @Schema(description = "Thời gian cập nhật")
    @TableField(fill = FieldFill.UPDATE)
    private Date updatedAt;
}