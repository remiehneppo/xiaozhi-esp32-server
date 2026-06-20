package xiaozhi.common.utils;

import java.io.Serializable;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;
import xiaozhi.common.exception.ErrorCode;

/**
 * dữ liệu phản hồi
 * Bản quyền (c) Renren Kaiyuan Mọi quyền được bảo lưu.
 * Website: https://www.renren.io
 */
@Data
@Schema(description = "phản ứng")
public class Result<T> implements Serializable {

    /**
     * Mã hóa: 0 biểu thị thành công, các giá trị khác biểu thị thất bại
     */
    @Schema(description = "mã hóa：0chỉ ra sự thành công，Các giá trị khác cho thấy sự thất bại")
    private int code = 0;
    /**
     * Nội dung tin nhắn
     */
    @Schema(description = "Nội dung tin nhắn")
    private String msg = "success";
    /**
     * dữ liệu phản hồi
     */
    @Schema(description = "dữ liệu phản hồi")
    private T data;

    public Result<T> ok(T data) {
        this.setData(data);
        return this;
    }

    public Result<T> error() {
        this.code = ErrorCode.INTERNAL_SERVER_ERROR;
        this.msg = MessageUtils.getMessage(this.code);
        return this;
    }

    public Result<T> error(int code) {
        this.code = code;
        this.msg = MessageUtils.getMessage(this.code);
        return this;
    }

    public Result<T> error(int code, String msg) {
        this.code = code;
        this.msg = msg;
        return this;
    }

    public Result<T> error(String msg) {
        this.code = ErrorCode.INTERNAL_SERVER_ERROR;
        this.msg = msg;
        return this;
    }

}