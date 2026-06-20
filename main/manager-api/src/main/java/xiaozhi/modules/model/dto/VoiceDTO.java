package xiaozhi.modules.model.dto;

import java.io.Serializable;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Schema(description = "thông tin âm sắc")
public class VoiceDTO implements Serializable {
    private static final long serialVersionUID = 1L;

    @Schema(description = "âm sắcID")
    private String id;

    @Schema(description = "Tên giọng nói")
    private String name;

    @Schema(description = "Địa chỉ phát lại âm thanh")
    private String voiceDemo;
    
    @Schema(description = "loại ngôn ngữ")
    private String languages;
    
    @Schema(description = "Cho dù đó là một âm thanh nhân bản")
    private Boolean isClone;

    // Thêm hàm tạo hai tham số để duy trì khả năng tương thích ngược
    public VoiceDTO(String id, String name) {
        this.id = id;
        this.name = name;
        this.voiceDemo = null;
        this.languages = null;
        this.isClone = false; // Không được sao chép theo mặc định
    }
    
    // Đã thêm hàm tạo ba tham số cho âm sắc thông thường
    public VoiceDTO(String id, String name, String voiceDemo) {
        this.id = id;
        this.name = name;
        this.voiceDemo = voiceDemo;
        this.languages = null;
        this.isClone = false;
    }

}