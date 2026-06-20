package xiaozhi.modules.agent.service;

import java.util.List;
import java.util.Map;

import xiaozhi.common.page.PageData;
import xiaozhi.common.service.BaseService;
import xiaozhi.modules.agent.dto.AgentCreateDTO;
import xiaozhi.modules.agent.dto.AgentDTO;
import xiaozhi.modules.agent.dto.AgentUpdateDTO;
import xiaozhi.modules.agent.entity.AgentEntity;
import xiaozhi.modules.agent.vo.AgentInfoVO;

/**
 * Dịch vụ xử lý bề mặt cơ thể thông minh
 *
 * @author Goody
 * @version 1.0, 2025/4/30
 * @since 1.0.0
 */
public interface AgentService extends BaseService<AgentEntity> {
    /**
     * Lấy danh sách đại lý quản trị viên
     *
     * @param tham số truy vấn thông số
     * @return dữ liệu được phân trang
     */
    PageData<AgentEntity> adminAgentList(Map<String, Object> params);

    /**
     * Nhận đại lý dựa trên ID
     *
     * ID đại lý @param id
     * @return thực thể đại lý
     */
    AgentInfoVO getAgentById(String id);

    /**
     * Chèn tác nhân
     *
     * @param thực thể đại lý thực thể
     * @return xem có thành công không
     */
    boolean insert(AgentEntity entity);

    /**
     * Xóa tác nhân dựa trên ID người dùng
     *
     * @param userId ID người dùng
     */
    void deleteAgentByUserId(Long userId);

    /**
     * Lấy danh sách tác nhân người dùng
     *
     * @param userId ID người dùng
     * Từ khóa tìm kiếm từ khóa @param
     * @param searchType loại tìm kiếm (tên - tìm kiếm theo tên, mac - tìm kiếm theo địa chỉ MAC)
     * @return danh sách đại lý
     */
    List<AgentDTO> getUserAgents(Long userId, String keyword, String searchType);

    /**
     * Lấy số lượng thiết bị dựa trên ID đại lý
     *
     * @param ID đại lý ID đại lý
     * @return số lượng thiết bị
     */
    Integer getDeviceCountByAgentId(String agentId);

    /**
     * Truy vấn thông tin tác nhân mặc định của thiết bị tương ứng dựa trên địa chỉ MAC của thiết bị
     *
     * @param macĐịa chỉ MAC của thiết bị
     * @return Thông tin tác nhân mặc định, trả về null nếu nó không tồn tại
     */
    AgentEntity getDefaultAgentByMacAddress(String macAddress);

    /**
     * Kiểm tra xem người dùng có quyền truy cập vào tác nhân hay không
     *
     * @param ID đại lý ID đại lý
     * @param userId ID người dùng
     * @return có được phép không
     */
    boolean checkAgentPermission(String agentId, Long userId);

    /**
     * Cập nhật đại lý
     *
     * @param ID đại lý ID đại lý
     * @param dto thông tin cần thiết để cập nhật tác nhân
     */
    void updateAgentById(String agentId, AgentUpdateDTO dto);

    /**
     * Tạo một đại lý
     *
     * @param dto thông tin cần thiết để tạo tác nhân
     * @return ID đại lý đã tạo
     */
    String createAgent(AgentCreateDTO dto);


}
