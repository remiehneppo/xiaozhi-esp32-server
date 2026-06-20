package xiaozhi.modules.timbre.entity;

import java.util.Date;

import com.baomidou.mybatisplus.annotation.FieldFill;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableName;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;
import lombok.EqualsAndHashCode;

/**
 * Lớp thực thể bảng giai điệu
 *
 * @author zjy
 * @since 2025-3-21
 */
@Data
@EqualsAndHashCode(callSuper = false)
@TableName("ai_tts_voice")
@Schema(description = "thông tin âm sắc")
public class TimbreEntity {

    @Schema(description = "id")
    private String id;

    @Schema(description = "Ngôn ngữ")
    private String languages;

    @Schema(description = "Tên giọng nói")
    private String name;

    @Schema(description = "Bình luận")
    private String remark;

    @Schema(description = "Đường dẫn âm thanh tham chiếu")
    private String referenceAudio;

    @Schema(description = "Văn bản tham khảo")
    private String referenceText;

    @Schema(description = "sắp xếp")
    private long sort;

    @Schema(description = "tương ứng TTS Khóa chính của mô hình")
    private String ttsModelId;

    @Schema(description = "mã hóa âm sắc")
    private String ttsVoice;

    @Schema(description = "Địa chỉ phát lại âm thanh")
    private String voiceDemo;

    @Schema(description = "Trình cập nhật")
    @TableField(fill = FieldFill.UPDATE)
    private Long updater;

    @Schema(description = "Thời gian cập nhật")
    @TableField(fill = FieldFill.UPDATE)
    private Date updateDate;

    @Schema(description = "Người sáng tạo")
    @TableField(fill = FieldFill.INSERT)
    private Long creator;

    @Schema(description = "thời gian sáng tạo")
    @TableField(fill = FieldFill.INSERT)
    private Date createDate;

}