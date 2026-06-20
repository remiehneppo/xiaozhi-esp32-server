package xiaozhi.modules.agent.dto;

import java.io.Serializable;
import java.math.BigDecimal;
import java.util.HashMap;
import java.util.List;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

/**
 * Cập nhật đại lý DTO
 * Dành riêng cho việc cập nhật tác nhân, trường id là bắt buộc và được sử dụng để xác định tác nhân cần cập nhật.
 * Tất cả các trường khác là tùy chọn, chỉ những trường được cung cấp mới được cập nhật.
 */
@Data
@Schema(description = "Đối tượng cập nhật đại lý")
public class AgentUpdateDTO implements Serializable {
    private static final long serialVersionUID = 1L;

    @Schema(description = "mã hóa đại lý", example = "AGT_1234567890", nullable = true)
    private String agentCode;

    @Schema(description = "Tên đại lý", example = "Trợ lý dịch vụ khách hàng", nullable = true)
    private String agentName;

    @Schema(description = "Nhận dạng mô hình nhận dạng giọng nói", example = "asr_model_02", nullable = true)
    private String asrModelId;

    @Schema(description = "Logo phát hiện hoạt động giọng nói", example = "vad_model_02", nullable = true)
    private String vadModelId;

    @Schema(description = "Mã định danh mô hình ngôn ngữ lớn", example = "llm_model_02", nullable = true)
    private String llmModelId;

    @Schema(description = "logo mô hình nhỏ", example = "slm_model_02", nullable = true)
    private String slmModelId;

    @Schema(description = "VLLMnhận dạng mô hình", example = "vllm_model_02", required = false)
    private String vllmModelId;

    @Schema(description = "Nhận dạng mô hình tổng hợp giọng nói", example = "tts_model_02", required = false)
    private String ttsModelId;

    @Schema(description = "nhận dạng âm sắc", example = "voice_02", nullable = true)
    private String ttsVoiceId;

    @Schema(description = "ngôn ngữ âm sắc", example = "tiếng quan thoại", nullable = true)
    private String ttsLanguage;

    @Schema(description = "TTSkhối lượng", example = "50", nullable = true)
    private Integer ttsVolume;

    @Schema(description = "TTStốc độ nói", example = "50", nullable = true)
    private Integer ttsRate;

    @Schema(description = "TTScao độ", example = "50", nullable = true)
    private Integer ttsPitch;

    @Schema(description = "mã định danh mô hình bộ nhớ", example = "mem_model_02", nullable = true)
    private String memModelId;

    @Schema(description = "Mã nhận dạng mô hình ý định", example = "intent_model_02", nullable = true)
    private String intentModelId;

    @Schema(description = "Thông tin chức năng plug-in", nullable = true)
    private List<FunctionInfo> functions;

    @Schema(description = "Thông số cài đặt ký tự", example = "Bạn là trợ lý dịch vụ khách hàng chuyên nghiệp，Chịu trách nhiệm trả lời các câu hỏi của người dùng và cung cấp hỗ trợ", nullable = true)
    private String systemPrompt;

    @Schema(description = "Bộ nhớ tóm tắt", example = "Xây dựng mạng bộ nhớ động có thể phát triển，Lưu giữ thông tin quan trọng trong một không gian hạn chế，Theo dõi sự phát triển của thông tin bảo trì thông minh\n"
            + "Theo bản ghi cuộc trò chuyện，Tóm tắtuserthông tin quan trọng，để cung cấp dịch vụ được cá nhân hóa hơn trong các cuộc trò chuyện trong tương lai.", nullable = true)
    private String summaryMemory;

    @Schema(description = "Cấu hình lịch sử trò chuyện（0Không ghi lại 1Chỉ ghi lại văn bản 2Ghi lại văn bản và lời nói）", example = "3", nullable = true)
    private Integer chatHistoryConf;

    @Schema(description = "mã hóa ngôn ngữ", example = "zh_CN", nullable = true)
    private String langCode;

    @Schema(description = "ngôn ngữ tương tác", example = "Tiếng Trung", nullable = true)
    private String language;

    @Schema(description = "sắp xếp", example = "1", nullable = true)
    private Integer sort;

    @Schema(description = "Cấu hình nguồn ngữ cảnh", nullable = true)
    private List<ContextProviderDTO> contextProviders;

    @Schema(description = "tập tin từ thay thếIDdanh sách", nullable = true)
    private List<String> correctWordFileIds;

    @Data
    @Schema(description = "Thông tin chức năng plug-in")
    public static class FunctionInfo implements Serializable {
        @Schema(description = "trình cắm thêmID", example = "plugin_01")
        private String pluginId;

        @Schema(description = "Thông tin tham số chức năng", nullable = true)
        private HashMap<String, Object> paramInfo;

        private static final long serialVersionUID = 1L;
    }
}