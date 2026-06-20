package xiaozhi.modules.device.controller;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;

import org.apache.commons.lang3.StringUtils;
import org.apache.shiro.authz.annotation.RequiresPermissions;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.Parameters;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import xiaozhi.common.constant.Constant;
import xiaozhi.common.exception.ErrorCode;
import xiaozhi.common.page.PageData;
import xiaozhi.common.redis.RedisKeys;
import xiaozhi.common.redis.RedisUtils;
import xiaozhi.common.utils.Result;
import xiaozhi.common.validator.ValidatorUtils;
import xiaozhi.modules.device.entity.OtaEntity;
import xiaozhi.modules.device.service.OtaService;
import xiaozhi.modules.security.user.SecurityUser;
import xiaozhi.modules.sys.enums.SuperAdminEnum;
import xiaozhi.modules.sys.service.SysParamsService;

@Tag(name = "Quản lý nâng cấp chương trình cơ sở", description = "OTA Giao diện liên quan")
@Slf4j
@RestController
@RequiredArgsConstructor
@RequestMapping("/otaMag")
public class OTAMagController {
    private static final Logger logger = LoggerFactory.getLogger(OTAController.class);
    private final OtaService otaService;
    private final RedisUtils redisUtils;
    private final SysParamsService sysParamsService;

    @GetMapping
    @Operation(summary = "Truy vấn trang OTA Thông tin phần mềm")
    @Parameters({
            @Parameter(name = Constant.PAGE, description = "Số trang hiện tại，từ1bắt đầu", required = true),
            @Parameter(name = Constant.LIMIT, description = "Hiển thị số bản ghi trên mỗi trang", required = true)
    })
    @RequiresPermissions("sys:role:superAdmin")
    public Result<PageData<OtaEntity>> page(@Parameter(hidden = true) @RequestParam Map<String, Object> params) {
        ValidatorUtils.validateEntity(params);
        PageData<OtaEntity> page = otaService.page(params);
        return new Result<PageData<OtaEntity>>().ok(page);
    }

    @GetMapping("{id}")
    @Operation(summary = "thông tin OTA Thông tin phần mềm")
    @RequiresPermissions("sys:role:superAdmin")
    public Result<OtaEntity> get(@PathVariable("id") String id) {
        OtaEntity data = otaService.selectById(id);
        return new Result<OtaEntity>().ok(data);
    }

    @PostMapping
    @Operation(summary = "lưu lại OTA Thông tin phần mềm")
    @RequiresPermissions("sys:role:superAdmin")
    public Result<Void> save(@RequestBody OtaEntity entity) {
        if (entity == null) {
            return new Result<Void>().error("Thông tin phần mềm không được để trống");
        }
        if (StringUtils.isBlank(entity.getFirmwareName())) {
            return new Result<Void>().error("Tên chương trình cơ sở không được để trống");
        }
        if (StringUtils.isBlank(entity.getType())) {
            return new Result<Void>().error("Loại chương trình cơ sở không được để trống");
        }
        if (StringUtils.isBlank(entity.getVersion())) {
            return new Result<Void>().error("Số phiên bản không được để trống");
        }
        try {
            otaService.save(entity);
            return new Result<Void>();
        } catch (RuntimeException e) {
            return new Result<Void>().error(e.getMessage());
        }
    }

    @DeleteMapping("/{id}")
    @Operation(summary = "OTA Xóa")
    @RequiresPermissions("sys:role:superAdmin")
    public Result<Void> delete(@PathVariable("id") String[] ids) {
        if (ids == null || ids.length == 0) {
            return new Result<Void>().error("Đã xóa chương trình cơ sởIDkhông thể trống");
        }
        otaService.delete(ids);
        return new Result<Void>();
    }

    @PutMapping("/{id}")
    @Operation(summary = "sửa đổi OTA Thông tin phần mềm")
    @RequiresPermissions("sys:role:superAdmin")
    public Result<?> update(@PathVariable("id") String id, @RequestBody OtaEntity entity) {
        if (entity == null) {
            return new Result<>().error("Thông tin phần mềm không được để trống");
        }
        entity.setId(id);
        try {
            otaService.update(entity);
            return new Result<>();
        } catch (RuntimeException e) {
            return new Result<>().error(e.getMessage());
        }
    }

    @GetMapping("/getDownloadUrl/{id}")
    @Operation(summary = "nhận được OTA Liên kết tải xuống chương trình cơ sở")
    @RequiresPermissions("sys:role:superAdmin")
    public Result<String> getDownloadUrl(@PathVariable("id") String id) {
        String uuid = UUID.randomUUID().toString();
        redisUtils.set(RedisKeys.getOtaIdKey(uuid), id);
        return new Result<String>().ok(uuid);
    }

    @GetMapping("/download/{uuid}")
    @Operation(summary = "Tải xuống tập tin phần sụn")
    public ResponseEntity<byte[]> downloadFirmware(@PathVariable("uuid") String uuid) {
        String id = (String) redisUtils.get(RedisKeys.getOtaIdKey(uuid));
        if (StringUtils.isBlank(id)) {
            return ResponseEntity.notFound().build();
        }

        // Kiểm tra số lượt tải xuống
        String downloadCountKey = RedisKeys.getOtaDownloadCountKey(uuid);
        Integer downloadCount = (Integer) Optional.ofNullable(redisUtils.get(downloadCountKey)).orElse(0);

        // Nếu số lượt tải vượt quá 3 lần thì trả về 404
        if (downloadCount >= 3) {
            redisUtils.delete(List.of(downloadCountKey, RedisKeys.getOtaIdKey(uuid)));
            logger.warn("Download limit exceeded for UUID: {}", uuid);
            return ResponseEntity.notFound().build();
        }

        redisUtils.set(downloadCountKey, downloadCount + 1);

        try {
            // Nhận thông tin phần mềm
            OtaEntity otaEntity = null;
            if (id.indexOf("file:") == 0) {
                id = id.substring(5);
                otaEntity = new OtaEntity();
                otaEntity.setFirmwarePath(id);
                otaEntity.setType("assets");
                otaEntity.setVersion("1.0.0");
            } else {
                otaEntity = otaService.selectById(id);
            }

            if (otaEntity == null || StringUtils.isBlank(otaEntity.getFirmwarePath())) {
                logger.warn("Firmware not found or path is empty for ID: {}", id);
                return ResponseEntity.notFound().build();
            }

            // Nhận đường dẫn tệp - đảm bảo đường dẫn là tuyệt đối hoặc đường dẫn tương đối chính xác
            String firmwarePath = otaEntity.getFirmwarePath();
            String originalFilename = otaEntity.getType() + "_" + otaEntity.getVersion();
            Path path;

            // Kiểm tra xem đó có phải là đường dẫn tuyệt đối không
            if (Paths.get(firmwarePath).isAbsolute()) {
                path = Paths.get(firmwarePath);
            } else {
                // Nếu đó là đường dẫn tương đối thì nó sẽ được giải quyết từ thư mục làm việc hiện tại.
                path = Paths.get(System.getProperty("user.dir"), firmwarePath);
            }

            logger.info("Attempting to download firmware for ID: {}, DB path: {}, resolved path: {}",
                    id, firmwarePath, path.toAbsolutePath());

            if (!Files.exists(path) || !Files.isRegularFile(path)) {
                // Cố gắng tìm tên tệp trực tiếp từ thư mục phần sụn
                String fileName = new File(firmwarePath).getName();
                Path altPath = Paths.get(System.getProperty("user.dir"), "firmware", fileName);

                logger.info("File not found at primary path, trying alternative path: {}", altPath.toAbsolutePath());

                if (Files.exists(altPath) && Files.isRegularFile(altPath)) {
                    path = altPath;
                } else {
                    logger.error("Firmware file not found at either path: {} or {}",
                            path.toAbsolutePath(), altPath.toAbsolutePath());
                    return ResponseEntity.notFound().build();
                }
            }

            // Đọc nội dung tập tin
            byte[] fileContent = Files.readAllBytes(path);

            // Đặt tiêu đề phản hồi

            if (firmwarePath.contains(".")) {
                String extension = firmwarePath.substring(firmwarePath.lastIndexOf("."));
                originalFilename += extension;
            }

            // Làm sạch tên file, loại bỏ các ký tự không an toàn
            String safeFilename = originalFilename.replaceAll("[^a-zA-Z0-9._-]", "_");

            logger.info("Providing download for firmware ID: {}, filename: {}, size: {} bytes",
                    id, safeFilename, fileContent.length);

            return ResponseEntity.ok()
                    .contentType(MediaType.APPLICATION_OCTET_STREAM)
                    .header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=\"" + safeFilename + "\"")
                    .body(fileContent);
        } catch (IOException e) {
            logger.error("Error reading firmware file for ID: {}", id, e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        } catch (Exception e) {
            logger.error("Unexpected error during firmware download for ID: {}", id, e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }

    @PostMapping("/upload")
    @Operation(summary = "Tải lên tập tin chương trình cơ sở")
    @RequiresPermissions("sys:role:superAdmin")
    public Result<String> uploadFirmware(@RequestParam("file") MultipartFile file) {
        if (file.isEmpty()) {
            return new Result<String>().error("Tệp tải lên không được để trống");
        }

        // Kiểm tra phần mở rộng tập tin
        String originalFilename = file.getOriginalFilename();
        if (originalFilename == null) {
            return new Result<String>().error("Tên tệp không được để trống");
        }

        String extension = originalFilename.substring(originalFilename.lastIndexOf(".")).toLowerCase();
        if (!extension.equals(".bin") && !extension.equals(".apk")) {
            return new Result<String>().error("Chỉ cho phép tải lên.binvà.apktập tin định dạng");
        }

        try {
            // Tính giá trị MD5 của tệp
            String md5 = calculateMD5(file);

            // Đặt đường dẫn lưu trữ
            String uploadDir = "uploadfile";
            Path uploadPath = Paths.get(uploadDir);

            // Nếu thư mục không tồn tại, hãy tạo thư mục
            if (!Files.exists(uploadPath)) {
                Files.createDirectories(uploadPath);
            }

            // Sử dụng MD5 làm tên tệp và luôn sử dụng phần mở rộng .bin.
            String uniqueFileName = md5 + extension;
            Path filePath = uploadPath.resolve(uniqueFileName);

            // Kiểm tra xem tập tin đã tồn tại chưa
            if (Files.exists(filePath)) {
                return new Result<String>().ok(filePath.toString());
            }

            // lưu tập tin
            Files.copy(file.getInputStream(), filePath);

            // Đường dẫn tập tin trả về
            return new Result<String>().ok(filePath.toString());
        } catch (IOException | NoSuchAlgorithmException e) {
            return new Result<String>().error("Tải tệp lên không thành công：" + e.getMessage());
        }
    }

    @PostMapping("/uploadAssetsBin")
    @Operation(summary = "Tải lên tập tin chương trình cơ sở tài nguyên")
    @RequiresPermissions("sys:role:normal")
    public Result<String> uploadAssetsBin(@RequestParam("file") MultipartFile file) {
        String otaUrl = sysParamsService.getValue(Constant.SERVER_OTA, true);
        if (StringUtils.isBlank(otaUrl) || otaUrl.equals("null")) {
            return new Result<String>().error(ErrorCode.OTA_URL_EMPTY);
        }
        logger.info("username:{},uploadAssetsBin size: {}", SecurityUser.getUser().getUsername(), file.getSize());
        // Xác minh kích thước tệp (phần sụn tài nguyên tối đa 20 MB)
        if (file.getSize() > 20 * 1024 * 1024) {
            return new Result<String>().error(ErrorCode.VOICE_CLONE_AUDIO_TOO_LARGE);
        }
        // Người dùng thông thường chỉ có thể tải lên 50 lần mỗi ngày
        if (SecurityUser.getUser().getSuperAdmin() == SuperAdminEnum.NO.value()) {
            String uploadCountKey = RedisKeys.getOtaUploadCountKey(SecurityUser.getUser().getId());
            Integer uploadCount = (Integer) Optional.ofNullable(redisUtils.get(uploadCountKey)).orElse(0);
            if (uploadCount >= 50) {
                return new Result<String>().error(ErrorCode.OTA_UPLOAD_COUNT_EXCEED);
            }
            // Tăng số lượng tải lên
            redisUtils.increment(RedisKeys.getOtaUploadCountKey(SecurityUser.getUser().getId()),
                    RedisUtils.DEFAULT_EXPIRE);
        }
        Result<String> result = uploadFirmware(file);

        // Tạo đường dẫn tệp tài nguyên
        if (StringUtils.isNotBlank(result.getData())) {
            String uuid = UUID.randomUUID().toString();
            redisUtils.set(RedisKeys.getOtaIdKey(uuid), "file:" + result.getData());
            String downloadUrl = otaUrl.replace("/ota/", "/otaMag/download/") + uuid;
            result.setData(downloadUrl);
        }
        return result;
    }

    private String calculateMD5(MultipartFile file) throws IOException, NoSuchAlgorithmException {
        MessageDigest md = MessageDigest.getInstance("MD5");
        byte[] digest = md.digest(file.getBytes());
        StringBuilder sb = new StringBuilder();
        for (byte b : digest) {
            sb.append(String.format("%02x", b));
        }
        return sb.toString();
    }
}
