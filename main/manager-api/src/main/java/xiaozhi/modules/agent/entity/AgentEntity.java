package xiaozhi.modules.agent.entity;

import java.math.BigDecimal;
import java.util.Date;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

@Data
@TableName("ai_agent")
@Schema(description = "Thông tin đại lý")
public class AgentEntity {

    @TableId(type = IdType.ASSIGN_UUID)
    @Schema(description = "Mã định danh duy nhất của đại lý")
    private String id;

    @Schema(description = "người dùngID")
    private Long userId;

    @Schema(description = "mã hóa đại lý")
    private String agentCode;

    @Schema(description = "Tên đại lý")
    private String agentName;

    @Schema(description = "Nhận dạng mô hình nhận dạng giọng nói")
    private String asrModelId;

    @Schema(description = "Logo phát hiện hoạt động giọng nói")
    private String vadModelId;

    @Schema(description = "Mã định danh mô hình ngôn ngữ lớn")
    private String llmModelId;

    @Schema(description = "logo mô hình nhỏ")
    private String slmModelId;

    @Schema(description = "VLLMnhận dạng mô hình")
    private String vllmModelId;

    @Schema(description = "Nhận dạng mô hình tổng hợp giọng nói")
    private String ttsModelId;

    @Schema(description = "nhận dạng âm sắc")
    private String ttsVoiceId;

    @Schema(description = "ngôn ngữ âm sắc")
    private String ttsLanguage;

    @Schema(description = "TTSkhối lượng")
    private Integer ttsVolume;

    @Schema(description = "TTStốc độ nói")
    private Integer ttsRate;

    @Schema(description = "TTScao độ")
    private Integer ttsPitch;

    @Schema(description = "mã định danh mô hình bộ nhớ")
    private String memModelId;

    @Schema(description = "Mã nhận dạng mô hình ý định")
    private String intentModelId;

    @Schema(description = "Cấu hình lịch sử trò chuyện（0Không ghi lại 1Chỉ ghi lại văn bản 2Ghi lại văn bản và lời nói）")
    private Integer chatHistoryConf;

    @Schema(description = "Thông số cài đặt ký tự")
    private String systemPrompt;

    @Schema(description = "Bộ nhớ tóm tắt", example = "Xây dựng mạng bộ nhớ động có thể phát triển，Lưu giữ thông tin quan trọng trong một không gian hạn chế，Theo dõi sự phát triển của thông tin bảo trì thông minh\n" +
            "Theo bản ghi cuộc trò chuyện，Tóm tắtuserthông tin quan trọng，để cung cấp dịch vụ được cá nhân hóa hơn trong các cuộc trò chuyện trong tương lai.", required = false)
    private String summaryMemory;

    @Schema(description = "mã hóa ngôn ngữ")
    private String langCode;

    @Schema(description = "ngôn ngữ tương tác")
    private String language;

    @Schema(description = "sắp xếp")
    private Integer sort;

    @Schema(description = "Người sáng tạo")
    private Long creator;

    @Schema(description = "thời gian sáng tạo")
    private Date createdAt;

    @Schema(description = "Trình cập nhật")
    private Long updater;

    @Schema(description = "Thời gian cập nhật")
    private Date updatedAt;
}