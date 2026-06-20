package xiaozhi.common.page;

import java.io.Serializable;
import java.util.List;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

/**
 * Lớp công cụ phân trang
 * Bản quyền (c) Renren Kaiyuan Mọi quyền được bảo lưu.
 * Website: https://www.renren.io
 */
@Data
@Schema(description = "Dữ liệu được phân trang")
public class PageData<T> implements Serializable {
    @Schema(description = "Tổng số hồ sơ")
    private int total;

    @Schema(description = "Liệt kê dữ liệu")
    private List<T> list;

    /**
     * Phân trang
     *
     * dữ liệu danh sách danh sách @param
     * @param tổng số bản ghi
     */
    public PageData(List<T> list, long total) {
        this.list = list;
        this.total = (int) total;
    }
}