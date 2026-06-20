package xiaozhi.modules.sys.vo;

import java.io.Serializable;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

/**
 * Dữ liệu từ điển VO
 */
@Data
@Schema(description = "Mục dữ liệu từ điển")
public class SysDictDataItem implements Serializable {

    @Schema(description = "thẻ từ điển")
    private String name;

    @Schema(description = "Giá trị từ điển")
    private String key;
}
