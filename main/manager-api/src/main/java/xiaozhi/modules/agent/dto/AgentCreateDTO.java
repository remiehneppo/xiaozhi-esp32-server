package xiaozhi.modules.agent.dto;

import java.io.Serializable;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;
import lombok.Data;

/**
 * Đại lý tạo DTO
 * Dành riêng cho việc thêm các đại lý mới, nó không bao gồm các trường id, AgentCode và sắp xếp. Các trường này được hệ thống tự động tạo/đặt thành giá trị mặc định.
 */
@Data
@Schema(description = "Tác nhân tạo đối tượng")
public class AgentCreateDTO implements Serializable {
    private static final long serialVersionUID = 1L;

    @Schema(description = "Tên đại lý", example = "Trợ lý dịch vụ khách hàng")
    @NotBlank(message = "Tên đại lý không được để trống")
    private String agentName;
}