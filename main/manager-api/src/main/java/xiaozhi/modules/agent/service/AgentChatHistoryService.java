package xiaozhi.modules.agent.service;

import java.util.List;
import java.util.Map;

import com.baomidou.mybatisplus.extension.service.IService;

import xiaozhi.common.page.PageData;
import xiaozhi.modules.agent.dto.AgentChatHistoryDTO;
import xiaozhi.modules.agent.dto.AgentChatSessionDTO;
import xiaozhi.modules.agent.entity.AgentChatHistoryEntity;
import xiaozhi.modules.agent.vo.AgentChatHistoryUserVO;

/**
 * Dịch vụ xử lý bảng ghi cuộc trò chuyện của đại lý
 *
 * @author Goody
 * @version 1.0, 2025/4/30
 * @since 1.0.0
 */
public interface AgentChatHistoryService extends IService<AgentChatHistoryEntity> {

    /**
     * Nhận danh sách phiên dựa trên ID đại lý
     *
     * @param tham số truy vấn, bao gồm AgentId, page, limit
     * @return danh sách phiên được phân trang
     */
    PageData<AgentChatSessionDTO> getSessionListByAgentId(Map<String, Object> params);

    /**
     * Nhận danh sách lịch sử trò chuyện dựa trên ID phiên
     *
     * @param ID đại lý ID đại lý
     * @param sessionId ID phiên
     * @return Danh sách lịch sử trò chuyện
     */
    List<AgentChatHistoryDTO> getChatHistoryBySessionId(String agentId, String sessionId);

    /**
     * Xóa lịch sử trò chuyện dựa trên ID đại lý
     *
     * @param ID đại lý ID đại lý
     * @param deleteAudio có nên xóa âm thanh không
     * @param deleteText có nên xóa văn bản không
     */
    void deleteByAgentId(String agentId, Boolean deleteAudio, Boolean deleteText);

    /**
     * Nhận dữ liệu lịch sử trò chuyện mới nhất của 50 người dùng (có dữ liệu âm thanh) dựa trên ID tác nhân
     *
     * @param AgentId id đại lý
     * @return Danh sách lịch sử trò chuyện (chỉ người dùng)
     */
    List<AgentChatHistoryUserVO> getRecentlyFiftyByAgentId(String agentId);

    /**
     * Nhận nội dung trò chuyện dựa trên ID dữ liệu âm thanh
     *
     * @param audioId id âm thanh
     * @return nội dung trò chuyện
     */
    String getContentByAudioId(String audioId);


    /**
     * Truy vấn xem id âm thanh này có thuộc về tác nhân này không
     *
     * @param audioId id âm thanh
     * @param id âm thanh AgentId
     * @return T: thuộc về F: không thuộc về
     */
    boolean isAudioOwnedByAgent(String audioId,String agentId);
}
