package xiaozhi.modules.config.dto;

import java.util.Map;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.Data;

@Data
@Schema(description = "Nhận cấu hình mô hình đại lýDTO")
public class AgentModelsDTO {

    @NotBlank(message = "Thiết bịMACĐịa chỉ không thể trống")
    @Schema(description = "Thiết bịMACđịa chỉ")
    private String macAddress;

    @NotBlank(message = "khách hàngIDkhông thể trống")
    @Schema(description = "khách hàngID")
    private String clientId;

    @NotNull(message = "Mô hình do khách hàng khởi tạo không được để trống")
    @Schema(description = "Mô hình do khách hàng khởi tạo")
    private Map<String, String> selectedModule;
}