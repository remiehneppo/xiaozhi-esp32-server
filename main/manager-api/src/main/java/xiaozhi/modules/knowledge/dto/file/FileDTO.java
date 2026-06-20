package xiaozhi.modules.knowledge.dto.file;

import lombok.*;
import io.swagger.v3.oas.annotations.media.Schema;
import java.io.Serializable;
import java.util.List;
import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.constraints.*;
import org.springframework.web.multipart.MultipartFile;

/**
 * Tổng hợp quản lý tệp DTO
 * <p>
 * Lớp vùng chứa chứa các định nghĩa lớp tĩnh bên trong cho tất cả các đối tượng yêu cầu/phản hồi của mô-đun tệp.
 * </p>
 */
@Schema(description = "Tổng hợp quản lý tập tin DTO")
public class FileDTO {

    // ========== Yêu cầu lớp ===========

    /**
     * Yêu cầu upload file (tương ứng với giao diện 1: upload)
     */
    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    @Schema(description = "Yêu cầu tải tập tin lên")
    public static class UploadReq implements Serializable {

        @NotNull(message = "Tệp không thể trống")
        @Schema(description = "Tệp đã tải lên", requiredMode = Schema.RequiredMode.REQUIRED)
        private MultipartFile file;

        @Schema(description = "thư mục mẹ ID (Nếu trống, tải lên thư mục gốc)", example = "folder_001")
        @JsonProperty("parent_id")
        private String parentId;
    }

    /**
     * Yêu cầu thư mục mới (tương ứng với giao diện 2: tạo)
     */
    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    @Schema(description = "Yêu cầu thư mục mới")
    public static class CreateReq implements Serializable {

        @NotBlank(message = "Tên thư mục không được để trống")
        @Schema(description = "tên thư mục", requiredMode = Schema.RequiredMode.REQUIRED, example = "Tạo thư mục mới")
        private String name;

        @Schema(description = "thư mục mẹ ID (Nếu trống, nó sẽ được tạo trong thư mục gốc.)", example = "folder_001")
        @JsonProperty("parent_id")
        private String parentId;

        @NotBlank(message = "Loại không được để trống")
        @Schema(description = "loại: FOLDER", requiredMode = Schema.RequiredMode.REQUIRED, example = "FOLDER")
        @Builder.Default
        private String type = "FOLDER";
    }

    /**
     * Yêu cầu đổi tên (tương ứng với giao diện 6: đổi tên)
     */
    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    @Schema(description = "Yêu cầu đổi tên")
    public static class RenameReq implements Serializable {

        @NotBlank(message = "tập tin ID không thể trống")
        @Schema(description = "tập tin/thư mục ID", requiredMode = Schema.RequiredMode.REQUIRED, example = "file_001")
        @JsonProperty("file_id")
        private String fileId;

        @NotBlank(message = "Tên mới không được để trống")
        @Schema(description = "tên mới", requiredMode = Schema.RequiredMode.REQUIRED, example = "Đã đổi tên tệp")
        private String name;
    }

    /**
     * Yêu cầu di chuyển (tương ứng với giao diện 7: di chuyển)
     */
    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    @Schema(description = "yêu cầu di chuyển")
    public static class MoveReq implements Serializable {

        @NotEmpty(message = "tập tin nguồn ID Danh sách không thể trống")
        @Schema(description = "tập tin nguồn/thư mục ID danh sách", requiredMode = Schema.RequiredMode.REQUIRED, example = "[\"file_001\", \"file_002\"]")
        @JsonProperty("src_file_ids")
        private List<String> srcFileIds;

        @NotBlank(message = "thư mục đích ID không thể trống")
        @Schema(description = "thư mục đích ID", requiredMode = Schema.RequiredMode.REQUIRED, example = "folder_002")
        @JsonProperty("dest_file_id")
        private String destFileId;
    }

    /**
     * Yêu cầu xóa hàng loạt (tương ứng với giao diện 8:rm)
     */
    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    @Schema(description = "Yêu cầu xóa hàng loạt")
    public static class RemoveReq implements Serializable {

        @NotEmpty(message = "tập tin ID Danh sách không thể trống")
        @Schema(description = "tập tin/thư mục ID danh sách", requiredMode = Schema.RequiredMode.REQUIRED, example = "[\"file_001\", \"file_002\"]")
        @JsonProperty("file_ids")
        private List<String> fileIds;
    }

    /**
     * Nhập yêu cầu cơ sở tri thức (tương ứng với giao diện 9:chuyển đổi)
     */
    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    @Schema(description = "Nhập yêu cầu cơ sở kiến thức")
    public static class ConvertReq implements Serializable {

        @NotEmpty(message = "tập tin ID Danh sách không thể trống")
        @Schema(description = "tập tin ID danh sách", requiredMode = Schema.RequiredMode.REQUIRED, example = "[\"file_001\", \"file_002\"]")
        @JsonProperty("file_ids")
        private List<String> fileIds;

        @NotEmpty(message = "cơ sở tri thức ID Danh sách không thể trống")
        @Schema(description = "cơ sở tri thức mục tiêu ID danh sách", requiredMode = Schema.RequiredMode.REQUIRED, example = "[\"kb_001\"]")
        @JsonProperty("kb_ids")
        private List<String> kbIds;
    }

    /**
     * Yêu cầu truy vấn danh sách (tương ứng với giao diện 3: list_files)
     */
    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    @Schema(description = "Danh sách yêu cầu truy vấn")
    public static class ListReq implements Serializable {

        @Schema(description = "thư mục mẹ ID (Nếu trống, truy vấn thư mục gốc)", example = "folder_001")
        @JsonProperty("parent_id")
        private String parentId;

        @Schema(description = "tìm kiếm từ khóa", example = "Tài liệu")
        private String keywords;

        @Schema(description = "Số trang (từ 1 bắt đầu)", example = "1")
        private Integer page;

        @Schema(description = "Số lượng mỗi trang", example = "30")
        @JsonProperty("page_size")
        private Integer pageSize;

        @Schema(description = "trường sắp xếp: create_time / update_time / name / size", example = "create_time")
        private String orderby;

        @Schema(description = "Có thứ tự giảm dần", example = "true")
        private Boolean desc;
    }

    // ========== Lớp phản hồi ===========

    /**
     * Thông tin cơ bản về tập tin/thư mục VO
     */
    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    @Schema(description = "tập tin/Thông tin cơ bản về thư mục")
    public static class InfoVO implements Serializable {

        @Schema(description = "tập tin/thư mục ID", example = "file_001")
        private String id;

        @Schema(description = "thư mục mẹ ID", example = "folder_001")
        @JsonProperty("parent_id")
        private String parentId;

        @Schema(description = "người thuê nhà ID", example = "tenant_001")
        @JsonProperty("tenant_id")
        private String tenantId;

        @Schema(description = "Người sáng tạo ID", example = "user_001")
        @JsonProperty("created_by")
        private String createdBy;

        @Schema(description = "loại: FOLDER / FILE", example = "FOLDER")
        private String type;

        @Schema(description = "Tên", example = "thư mục của tôi")
        private String name;

        @Schema(description = "vị trí đường dẫn", example = "/root/folder")
        private String location;

        @Schema(description = "kích thước tập tin (Byte)", example = "1024")
        private Long size;

        @Schema(description = "Loại nguồn", example = "local")
        @JsonProperty("source_type")
        private String sourceType;

        @Schema(description = "thời gian sáng tạo (Dấu thời gian)", example = "1700000000000")
        @JsonProperty("create_time")
        private Long createTime;

        @Schema(description = "Ngày tạo (định dạng)", example = "2024-01-15 10:30:00")
        @JsonProperty("create_date")
        private String createDate;

        @Schema(description = "Thời gian cập nhật (Dấu thời gian)", example = "1700000001000")
        @JsonProperty("update_time")
        private Long updateTime;

        @Schema(description = "ngày cập nhật (định dạng)", example = "2024-01-15 11:00:00")
        @JsonProperty("update_date")
        private String updateDate;

        @Schema(description = "phần mở rộng tập tin", example = "pdf")
        private String extension;
    }

    /**
     * Danh sách phản hồi VO (tương ứng với giao diện 3: list_files)
     */
    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    @Schema(description = "phản hồi danh sách tập tin")
    public static class ListVO implements Serializable {

        @Schema(description = "Tổng số hồ sơ", example = "100")
        private Long total;

        @Schema(description = "Thông tin thư mục mẹ hiện tại")
        @JsonProperty("parent_folder")
        private InfoVO parentFolder;

        @Schema(description = "tập tin/danh sách thư mục")
        private List<InfoVO> files;

        @Schema(description = "Đường dẫn điều hướng Breadcrumb")
        private List<InfoVO> breadcrumb;
    }

    /**
     * Mục kết quả chuyển đổi VO (tương ứng với giao diện 9: chuyển đổi)
     */
    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    @Schema(description = "Mục kết quả chuyển đổi tệp")
    public static class ConvertVO implements Serializable {

        @Schema(description = "bản ghi chuyển đổi ID", example = "convert_001")
        private String id;

        @Schema(description = "tập tin nguồn ID", example = "file_001")
        @JsonProperty("file_id")
        private String fileId;

        @Schema(description = "tài liệu mục tiêu ID", example = "doc_001")
        @JsonProperty("document_id")
        private String documentId;

        @Schema(description = "thời gian sáng tạo (Dấu thời gian)", example = "1700000000000")
        @JsonProperty("create_time")
        private Long createTime;

        @Schema(description = "Ngày tạo (định dạng)", example = "2024-01-15 10:30:00")
        @JsonProperty("create_date")
        private String createDate;

        @Schema(description = "Thời gian cập nhật (Dấu thời gian)", example = "1700000001000")
        @JsonProperty("update_time")
        private Long updateTime;

        @Schema(description = "ngày cập nhật (định dạng)", example = "2024-01-15 11:00:00")
        @JsonProperty("update_date")
        private String updateDate;
    }

    /**
     * Trạng thái chuyển đổi VO (tương ứng với giao diện 10: get_convert_status)
     */
    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    @Schema(description = "Trạng thái chuyển đổi tập tin")
    public static class ConvertStatusVO implements Serializable {

        @Schema(description = "Trạng thái chuyển tiếp: pending / processing / completed / failed", example = "completed")
        private String status;

        @Schema(description = "Tiến trình chuyển đổi (0.0 - 1.0)", example = "1.0")
        private Float progress;

        @Schema(description = "thông báo trạng thái", example = "Đã hoàn tất chuyển đổi")
        private String message;
    }

    /**
     * Breadcrumbs VO (tương ứng với giao diện 12: all_parent_folder)
     */
    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    @Schema(description = "vụn bánh mì (tất cả các thư mục mẹ)")
    public static class BreadcrumbVO implements Serializable {

        @Schema(description = "Danh sách thư mục mẹ (đường dẫn từ gốc đến hiện tại)")
        @JsonProperty("parent_folders")
        private List<InfoVO> parentFolders;
    }

    /**
     * Thông tin thư mục gốc VO (tương ứng với giao diện 10: get_root_folder)
     */
    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    @Schema(description = "thông tin thư mục gốc")
    public static class RootFolderVO implements Serializable {

        @Schema(description = "Thông tin thư mục gốc")
        @JsonProperty("root_folder")
        private InfoVO rootFolder;
    }

    /**
     * Thông tin thư mục cha VO (tương ứng với giao diện 11: get_parent_folder)
     */
    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    @Schema(description = "Thông tin thư mục cha mẹ")
    public static class ParentFolderVO implements Serializable {

        @Schema(description = "Thông tin thư mục gốc")
        @JsonProperty("parent_folder")
        private InfoVO parentFolder;
    }
}
