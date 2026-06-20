package xiaozhi.modules.voiceclone.dto;

import java.util.Date;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

/**
 * Phản hồi nhân bản âm thanh DTO
 * Được sử dụng để hiển thị thông tin bản sao âm thanh ở mặt trước, bao gồm tên model và tên người dùng
 */
@Data
@Schema(description = "phản hồi nhân bản âm thanhDTO")
public class VoiceCloneResponseDTO {

    @Schema(description = "mã định danh duy nhất")
    private String id;

    @Schema(description = "tên âm thanh")
    private String name;

    @Schema(description = "người mẫuid")
    private String modelId;

    @Schema(description = "Tên mẫu")
    private String modelName;

    @Schema(description = "âm thanhid")
    private String voiceId;

    @Schema(description = "Ngôn ngữ")
    private String languages;

    @Schema(description = "người dùngID（Bảng người dùng liên quan）")
    private Long userId;

    @Schema(description = "Tên người dùng")
    private String userName;

    @Schema(description = "tình trạng đào tạo：0Để được đào tạo 1trong đào tạo 2Đào tạo thành công 3Đào tạo không thành công")
    private Integer trainStatus;

    @Schema(description = "Nguyên nhân dẫn đến sai sót trong đào tạo")
    private String trainError;

    @Schema(description = "thời gian sáng tạo")
    private Date createDate;

    @Schema(description = "Có dữ liệu âm thanh?")
    private Boolean hasVoice;
}