package xiaozhi.modules.device;

import java.util.HashMap;
import java.util.UUID;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;

import lombok.extern.slf4j.Slf4j;
import xiaozhi.common.redis.RedisUtils;
import xiaozhi.modules.sys.dto.SysUserDTO;
import xiaozhi.modules.sys.service.SysUserService;

@Slf4j
@SpringBootTest
@ActiveProfiles("dev")
@DisplayName("Thử nghiệm thiết bị")
public class DeviceTest {

    @Autowired
    private RedisUtils redisUtils;
    @Autowired
    private SysUserService sysUserService;

    @Test
    public void testSaveUser() {
        SysUserDTO userDTO = new SysUserDTO();
        userDTO.setUsername("test");
        userDTO.setPassword(UUID.randomUUID().toString());
        sysUserService.save(userDTO);
    }

    @Test
    @DisplayName("Thử nghiệm ghi thông tin thiết bị")
    public void testWriteDeviceInfo() {
        log.info("Bắt đầu thử nghiệm ghi thông tin thiết bị...");
        // Mô phỏng địa chỉ MAC của thiết bị
        String macAddress = "00:11:22:33:44:66";
        // Mô phỏng mã xác thực của thiết bị
        String deviceCode = "123456";

        HashMap<String, Object> map = new HashMap<>();
        map.put("mac_address", macAddress);
        map.put("activation_code", deviceCode);
        map.put("board", "Mẫu phần cứng");
        map.put("app_version", "0.3.13");

        String safeDeviceId = macAddress.replace(":", "_").toLowerCase();
        String cacheDeviceKey = String.format("ota:activation:data:%s", safeDeviceId);
        redisUtils.set(cacheDeviceKey, map, 300);

        String redisKey = "ota:activation:code:" + deviceCode;
        log.info("Redis Key: {}", redisKey);

        // Ghi thông tin thiết bị vào Redis
        redisUtils.set(redisKey, macAddress, 300);
        log.info("Thông tin thiết bị đã được ghi vào Redis");

        // Xác thực việc ghi thành công
        String savedMacAddress = (String) redisUtils.get(redisKey);
        log.info("Địa chỉ MAC đọc từ Redis: {}", savedMacAddress);

        // Sử dụng khẳng định để xác thực
        Assertions.assertNotNull(savedMacAddress, "Địa chỉ MAC đọc từ Redis không được để trống");
        Assertions.assertEquals(macAddress, savedMacAddress, "Địa chỉ MAC đã lưu không khớp với địa chỉ MAC gốc");

        log.info("Thử nghiệm hoàn tất");
    }
}