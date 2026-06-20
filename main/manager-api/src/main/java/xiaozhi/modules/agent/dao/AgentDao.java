package xiaozhi.modules.agent.dao;

import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import org.apache.ibatis.annotations.Select;
import xiaozhi.common.dao.BaseDao;
import xiaozhi.modules.agent.entity.AgentEntity;
import xiaozhi.modules.agent.vo.AgentInfoVO;

@Mapper
public interface AgentDao extends BaseDao<AgentEntity> {
    /**
     * Lấy số lượng thiết bị của đại lý
     *
     * @param ID đại lý ID đại lý
     * @return số lượng thiết bị
     */
    Integer getDeviceCountByAgentId(@Param("agentId") String agentId);

    /**
     * Truy vấn thông tin tác nhân mặc định của thiết bị tương ứng dựa trên địa chỉ MAC của thiết bị
     *
     * @param macĐịa chỉ MAC của thiết bị
     * @return thông tin đại lý mặc định
     */
    @Select(" SELECT a.* FROM ai_device d " +
            " LEFT JOIN ai_agent a ON d.agent_id = a.id " +
            " WHERE d.mac_address = #{macAddress} " +
            " ORDER BY d.id DESC LIMIT 1")
    AgentEntity getDefaultAgentByMacAddress(@Param("macAddress") String macAddress);

    /**
     * Thông tin tác nhân truy vấn dựa trên ID, bao gồm thông tin phần bổ trợ
     *
     * @param ID đại lý ID đại lý
     */
    AgentInfoVO selectAgentInfoById(@Param("agentId") String agentId);
}
