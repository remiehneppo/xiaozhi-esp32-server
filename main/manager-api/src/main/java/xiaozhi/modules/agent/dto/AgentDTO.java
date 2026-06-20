package xiaozhi.modules.agent.dto;

import java.util.Date;
import java.util.List;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;
import xiaozhi.modules.agent.dto.AgentTagDTO;

/**
 * Đối tượng truyền dữ liệu đại lý
 * Được sử dụng để truyền dữ liệu liên quan đến tác nhân giữa lớp dịch vụ và lớp điều khiển
 */
@Data
@Schema(description = "đối tượng đại lý")
public class AgentDTO {
    @Schema(description = "mã hóa đại lý", example = "AGT_1234567890")
    private String id;

    @Schema(description = "Tên đại lý", example = "Trợ lý dịch vụ khách hàng")
    private String agentName;

    @Schema(description = "Tên mô hình tổng hợp giọng nói", example = "tts_model_01")
    private String ttsModelName;

    @Schema(description = "Tên giọng nói", example = "voice_01")
    private String ttsVoiceName;

    @Schema(description = "Tên mô hình ngôn ngữ lớn", example = "llm_model_01")
    private String llmModelName;

    @Schema(description = "Tên mô hình trực quan", example = "vllm_model_01")
    private String vllmModelName;

    @Schema(description = "mô hình bộ nhớID", example = "mem_model_01")
    private String memModelId;

    @Schema(description = "Thông số cài đặt ký tự", example = "Bạn là trợ lý dịch vụ khách hàng chuyên nghiệp，Chịu trách nhiệm trả lời các câu hỏi của người dùng và cung cấp hỗ trợ")
    private String systemPrompt;

    @Schema(description = "Bộ nhớ tóm tắt", example = "Xây dựng mạng bộ nhớ động có thể phát triển，Lưu giữ thông tin quan trọng trong một không gian hạn chế，Theo dõi sự phát triển của thông tin bảo trì thông minh\n" +
            "Theo bản ghi cuộc trò chuyện，Tóm tắtuserthông tin quan trọng，để cung cấp dịch vụ được cá nhân hóa hơn trong các cuộc trò chuyện trong tương lai.", required = false)
    private String summaryMemory;

    @Schema(description = "Lần kết nối cuối cùng", example = "2024-03-20 10:00:00")
    private Date lastConnectedAt;

    @Schema(description = "Số lượng thiết bị", example = "10")
    private Integer deviceCount;

    @Schema(description = "danh sách thẻ")
    private List<AgentTagDTO> tags;
}