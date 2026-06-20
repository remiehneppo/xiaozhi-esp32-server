package xiaozhi.modules.agent.dto;

import java.io.Serializable;
import java.util.Map;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

@Data
@Schema(description = "Cấu hình nguồn ngữ cảnhDTO")
public class ContextProviderDTO implements Serializable {
    private static final long serialVersionUID = 1L;

    @Schema(description = "URLđịa chỉ")
    private String url;

    @Schema(description = "Tiêu đề yêu cầu")
    private Map<String, Object> headers;
}
