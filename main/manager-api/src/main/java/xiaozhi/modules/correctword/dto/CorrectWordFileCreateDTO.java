package xiaozhi.modules.correctword.dto;

import java.util.List;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotEmpty;
import lombok.Data;

@Data
@Schema(description = "Tạo một tập tin từ thay thếDTO")
public class CorrectWordFileCreateDTO {

    @NotBlank(message = "Tên tệp không được để trống")
    @Schema(description = "tên tập tin")
    private String fileName;

    @NotEmpty(message = "Nội dung từ thay thế không được để trống")
    @Schema(description = "Thay thế nội dung từ，Mỗi định dạng：từ gốc|từ thay thế")
    private List<String> content;

    @Schema(description = "kích thước tập tin（Byte），không thể vượt quá1MB")
    private Long fileSize;
}
