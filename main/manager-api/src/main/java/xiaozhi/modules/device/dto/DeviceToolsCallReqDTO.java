package xiaozhi.modules.device.dto;

import java.util.Map;

import jakarta.validation.constraints.NotBlank;
import lombok.Data;

@Data
public class DeviceToolsCallReqDTO {

    @NotBlank(message = "Tên công cụ không được để trống")
    private String name;

    private Map<String, Object> arguments;
}