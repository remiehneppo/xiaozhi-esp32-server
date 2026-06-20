package xiaozhi.modules.device.controller;

import java.util.List;
import java.util.Map;

import org.apache.commons.lang3.StringUtils;
import org.apache.shiro.authz.annotation.RequiresPermissions;
import org.springframework.beans.BeanUtils;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import xiaozhi.common.exception.ErrorCode;
import xiaozhi.common.redis.RedisKeys;
import xiaozhi.common.redis.RedisUtils;
import xiaozhi.common.user.UserDetail;
import xiaozhi.common.utils.Result;
import xiaozhi.modules.device.dto.DeviceAddressBookAliasDTO;
import xiaozhi.modules.device.dto.DeviceAddressBookPermissionDTO;
import xiaozhi.modules.device.dto.DeviceManualAddDTO;
import xiaozhi.modules.device.dto.DeviceRegisterDTO;
import xiaozhi.modules.device.dto.DeviceToolsCallReqDTO;
import xiaozhi.modules.device.dto.DeviceUnBindDTO;
import xiaozhi.modules.device.dto.DeviceUpdateDTO;
import xiaozhi.modules.device.entity.DeviceEntity;
import xiaozhi.modules.device.service.DeviceAddressBookService;
import xiaozhi.modules.device.service.DeviceService;
import xiaozhi.modules.device.vo.UserShowDeviceListVO;
import xiaozhi.modules.security.user.SecurityUser;
import xiaozhi.modules.sys.service.SysParamsService;

@Tag(name = "Quản lý thiết bị")
@RestController
@RequestMapping("/device")
public class DeviceController {
    private final DeviceService deviceService;
    private final DeviceAddressBookService deviceAddressBookService;
    private final RedisUtils redisUtils;
    private final SysParamsService sysParamsService;

    public DeviceController(DeviceService deviceService, DeviceAddressBookService deviceAddressBookService,
            RedisUtils redisUtils, SysParamsService sysParamsService) {
        this.deviceService = deviceService;
        this.deviceAddressBookService = deviceAddressBookService;
        this.redisUtils = redisUtils;
        this.sysParamsService = sysParamsService;
    }

    @PostMapping("/bind/{agentId}/{deviceCode}")
    @Operation(summary = "Thiết bị liên kết")
    @RequiresPermissions("sys:role:normal")
    public Result<Void> bindDevice(@PathVariable String agentId, @PathVariable String deviceCode) {
        deviceService.deviceActivation(agentId, deviceCode);
        return new Result<>();
    }

    @PostMapping("/register")
    @Operation(summary = "Đăng ký thiết bị")
    public Result<String> registerDevice(@RequestBody DeviceRegisterDTO deviceRegisterDTO) {
        String macAddress = deviceRegisterDTO.getMacAddress();
        if (StringUtils.isBlank(macAddress)) {
            return new Result<String>().error(ErrorCode.MCA_NOT_NULL);
        }
        // Tạo mã xác minh gồm sáu chữ số
        String code;
        String key;
        String existsMac = null;
        do {
            code = String.valueOf(Math.random()).substring(2, 8);
            key = RedisKeys.getDeviceCaptchaKey(code);
            existsMac = (String) redisUtils.get(key);
        } while (StringUtils.isNotBlank(existsMac));

        redisUtils.set(key, macAddress);
        return new Result<String>().ok(code);
    }

    @GetMapping("/bind/{agentId}")
    @Operation(summary = "Nhận các thiết bị bị ràng buộc")
    @RequiresPermissions("sys:role:normal")
    public Result<List<UserShowDeviceListVO>> getUserDevices(@PathVariable String agentId) {
        UserDetail user = SecurityUser.getUser();
        List<UserShowDeviceListVO> devices = deviceService.getUserDeviceList(user.getId(), agentId);
        return new Result<List<UserShowDeviceListVO>>().ok(devices);
    }

    @PostMapping("/bind/{agentId}")
    @Operation(summary = "Giao diện trực tuyến của thiết bị")
    @RequiresPermissions("sys:role:normal")
    public Result<String> forwardToMqttGateway(@PathVariable String agentId, @RequestBody String requestBody) {
        try {
            return new Result<String>().ok(deviceService.getDeviceOnlineData(agentId));
        } catch (Exception e) {
            return new Result<String>().error("Yêu cầu chuyển tiếp không thành công: " + e.getMessage());
        }
    }

    @PostMapping("/unbind")
    @Operation(summary = "Hủy liên kết thiết bị")
    @RequiresPermissions("sys:role:normal")
    public Result<Void> unbindDevice(@RequestBody DeviceUnBindDTO unDeviveBind) {
        UserDetail user = SecurityUser.getUser();
        deviceService.unbindDevice(user.getId(), unDeviveBind.getDeviceId());
        return new Result<Void>();
    }

    @PutMapping("/update/{id}")
    @Operation(summary = "Cập nhật thông tin thiết bị")
    @RequiresPermissions("sys:role:normal")
    public Result<Void> updateDeviceInfo(@PathVariable String id, @Valid @RequestBody DeviceUpdateDTO deviceUpdateDTO) {
        DeviceEntity entity = deviceService.selectById(id);
        if (entity == null) {
            return new Result<Void>().error("Thiết bị không tồn tại");
        }
        UserDetail user = SecurityUser.getUser();
        if (!entity.getUserId().equals(user.getId())) {
            return new Result<Void>().error("Thiết bị không tồn tại");
        }
        BeanUtils.copyProperties(deviceUpdateDTO, entity);
        deviceService.updateById(entity);
        return new Result<Void>();
    }

    @PostMapping("/manual-add")
    @Operation(summary = "Thêm thiết bị theo cách thủ công")
    @RequiresPermissions("sys:role:normal")
    public Result<Void> manualAddDevice(@RequestBody @Valid DeviceManualAddDTO dto) {
        UserDetail user = SecurityUser.getUser();
        deviceService.manualAddDevice(user.getId(), dto);
        return new Result<>();
    }

    @PostMapping("/tools/list/{deviceId}")
    @Operation(summary = "Nhận danh sách công cụ thiết bị")
    @RequiresPermissions("sys:role:normal")
    public Result<Object> getDeviceTools(@PathVariable String deviceId) {
        Object toolsData = deviceService.getDeviceTools(deviceId);
        if (toolsData == null) {
            return new Result<Object>().error(ErrorCode.DEVICE_NOT_EXIST);
        }

        return new Result<Object>().ok(toolsData);
    }

    @PostMapping("/tools/call/{deviceId}")
    @Operation(summary = "Công cụ thiết bị gọi")
    @RequiresPermissions("sys:role:normal")
    public Result<Object> callDeviceTool(@PathVariable String deviceId,
            @Valid @RequestBody DeviceToolsCallReqDTO request) {
        String toolName = request.getName();
        Map<String, Object> arguments = request.getArguments();

        Object result = deviceService.callDeviceTool(deviceId, toolName, arguments);
        if (result == null) {
            return new Result<Object>().error(ErrorCode.DEVICE_NOT_EXIST);
        }

        Result<Object> response = new Result<Object>();
        response.setMsg("Tools called successfully");
        return response.ok(result);
    }

    @GetMapping("/address-book/{macAddress}")
    @Operation(summary = "Nhận sổ địa chỉ thiết bị")
    @RequiresPermissions("sys:role:normal")
    public Result<Object> getAddressBook(@PathVariable String macAddress) {
        return new Result<Object>().ok(deviceAddressBookService.getAddressBookList(macAddress));
    }

    @GetMapping("/address-book/lookup")
    @Operation(summary = "Tìm thiết bị mục tiêu dựa trên biệt danh")
    public Result<Map<String, String>> lookupByNickname(String callerMac, String nickname) {
        Map<String, String> result = deviceAddressBookService.lookupByNickname(callerMac, nickname);
        if (result == null) {
            return new Result<Map<String, String>>().error("Không tìm thấy thiết bị tương ứng");
        }
        return new Result<Map<String, String>>().ok(result);
    }

    @PutMapping("/address-book/alias")
    @Operation(summary = "Cập nhật bí danh sổ địa chỉ thiết bị")
    @RequiresPermissions("sys:role:normal")
    public Result<Void> updateAlias(@Valid @RequestBody DeviceAddressBookAliasDTO dto) {
        deviceAddressBookService.saveOrUpdate(dto.getMacAddress(), dto.getTargetMac(), dto.getAlias(), null);
        return new Result<Void>();
    }

    @PutMapping("/address-book/permission")
    @Operation(summary = "Cập nhật quyền sổ địa chỉ thiết bị")
    @RequiresPermissions("sys:role:normal")
    public Result<Void> updatePermission(@Valid @RequestBody DeviceAddressBookPermissionDTO dto) {
        deviceAddressBookService.saveOrUpdate(dto.getMacAddress(), dto.getTargetMac(), null, dto.getHasPermission());
        return new Result<Void>();
    }

    @GetMapping("/call/forward")
    @Operation(summary = "Chuyển tiếp yêu cầu cuộc gọi đến cổng")
    public Result<Map<String, Object>> forwardCallRequest(String callerMac, String targetMac, String callerNickname) {
        Map<String, Object> result = deviceService.forwardCallRequest(callerMac, targetMac, callerNickname);
        return new Result<Map<String, Object>>().ok(result);
    }
}