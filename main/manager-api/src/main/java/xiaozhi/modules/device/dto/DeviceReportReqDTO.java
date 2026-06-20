package xiaozhi.modules.device.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Getter;
import lombok.Setter;

import java.io.Serializable;
import java.util.List;

@Setter
@Getter
@Schema(description = "Nội dung yêu cầu báo cáo thông tin phần mềm cơ sở của thiết bị")
public class DeviceReportReqDTO implements Serializable {
    private static final long serialVersionUID = 1L;
    // thuộc tính thực thể khu vực
    @Schema(description = "Số phiên bản chương trình cơ sở của bo mạch")
    private Integer version;

    @Schema(description = "kích thước bộ nhớ flash（đơn vị：Byte）")
    @JsonProperty("flash_size")
    private Integer flashSize;

    @Schema(description = "Bộ nhớ heap trống tối thiểu（Byte）")
    @JsonProperty("minimum_free_heap_size")
    private Integer minimumFreeHeapSize;

    @Schema(description = "Thiết bị MAC địa chỉ")
    @JsonProperty("mac_address")
    private String macAddress;

    @Schema(description = "Mã định danh duy nhất của thiết bị UUID")
    private String uuid;

    @Schema(description = "Tên mẫu chip")
    @JsonProperty("chip_model_name")
    private String chipModelName;

    @Schema(description = "Chi tiết chip")
    @JsonProperty("chip_info")
    private ChipInfo chipInfo;

    @Schema(description = "Thông tin ứng dụng")
    private Application application;

    @Schema(description = "Danh sách bảng phân vùng")
    @JsonProperty("partition_table")
    private List<Partition> partitionTable;

    @Schema(description = "hiện đang chạy OTA Thông tin phân vùng")
    private OtaInfo ota;

    @Schema(description = "Thông tin cấu hình bo mạch")
    private BoardInfo board;

    // endregion

    @Getter
    @Setter
    @Schema(description = "Thông tin chip")
    public static class ChipInfo {
        @Schema(description = "Mã mẫu chip")
        private Integer model;

        @Schema(description = "Số lượng lõi")
        private Integer cores;

        @Schema(description = "Sửa đổi phần cứng")
        private Integer revision;

        @Schema(description = "Bit cờ chức năng chip")
        private Integer features;
    }

    @Getter
    @Setter
    @Schema(description = "Thông tin tổng hợp hội đồng quản trị")
    public static class Application {
        @Schema(description = "Tên")
        private String name;

        @Schema(description = "Số phiên bản ứng dụng")
        private String version;

        @Schema(description = "thời gian biên dịch（UTC ISOđịnh dạng）")
        @JsonProperty("compile_time")
        private String compileTime;

        @Schema(description = "ESP-IDF số phiên bản")
        @JsonProperty("idf_version")
        private String idfVersion;

        @Schema(description = "ELF tập tin SHA256 Xác minh")
        @JsonProperty("elf_sha256")
        private String elfSha256;
    }

    @Getter
    @Setter
    @Schema(description = "Thông tin phân vùng")
    public static class Partition {
        @Schema(description = "Tên nhãn phân vùng")
        private String label;

        @Schema(description = "Loại phân vùng")
        private Integer type;

        @Schema(description = "tiểu loại")
        private Integer subtype;

        @Schema(description = "địa chỉ bắt đầu")
        private Integer address;

        @Schema(description = "Kích thước phân vùng")
        private Integer size;
    }

    @Getter
    @Setter
    @Schema(description = "OTAthông tin")
    public static class OtaInfo {
        @Schema(description = "hiện tạiOTAnhãn")
        private String label;
    }

    @Getter
    @Setter
    @Schema(description = "Kết nối bo mạch và thông tin mạng")
    public static class BoardInfo {
        @Schema(description = "Loại bảng")
        private String type;

        @Schema(description = "đã kết nối Wi-Fi SSID")
        private String ssid;

        @Schema(description = "Wi-Fi cường độ tín hiệu（RSSI）")
        private Integer rssi;

        @Schema(description = "Wi-Fi kênh")
        private Integer channel;

        @Schema(description = "IP địa chỉ")
        private String ip;

        @Schema(description = "MAC địa chỉ")
        private String mac;
    }
}
