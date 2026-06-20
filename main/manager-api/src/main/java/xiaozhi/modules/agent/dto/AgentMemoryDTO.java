package xiaozhi.modules.agent.dto;

import java.io.Serializable;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

/**
 * Cập nhật bộ nhớ tác nhân DTO
 */
@Data
@Schema(description = "Đối tượng cập nhật bộ nhớ tác nhân")
public class AgentMemoryDTO implements Serializable {
    private static final long serialVersionUID = 1L;

    @Schema(description = "Bộ nhớ tóm tắt", example = "Xây dựng mạng bộ nhớ động có thể phát triển，Lưu giữ thông tin quan trọng trong một không gian hạn chế，Theo dõi sự phát triển của thông tin bảo trì thông minh\n" +
            "Theo bản ghi cuộc trò chuyện，Tóm tắtuserthông tin quan trọng，để cung cấp dịch vụ được cá nhân hóa hơn trong các cuộc trò chuyện trong tương lai.", required = false)
    private String summaryMemory;
}