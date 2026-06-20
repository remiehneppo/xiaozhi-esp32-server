package xiaozhi.modules.sys.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import xiaozhi.modules.sys.enums.ServerActionEnum;

/**
 * Gửi hoạt động máy chủ python DTO
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class EmitSeverActionDTO
{
    @Schema(description = "mục tiêuwsđịa chỉ")
    @NotEmpty(message = "mục tiêuwsĐịa chỉ không thể trống")
    private String targetWs;

    @Schema(description = "Chỉ định hoạt động")
    @NotNull(message = "Hoạt động không thể trống")
    private ServerActionEnum action;
}
