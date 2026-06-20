package xiaozhi.modules.agent.service.impl;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.apache.commons.lang3.StringUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;

import lombok.RequiredArgsConstructor;
import xiaozhi.common.constant.Constant;
import xiaozhi.modules.agent.dto.AgentChatHistoryDTO;
import xiaozhi.modules.agent.dto.AgentChatSummaryDTO;
import xiaozhi.modules.agent.dto.AgentMemoryDTO;
import xiaozhi.modules.agent.dto.AgentUpdateDTO;
import xiaozhi.modules.agent.entity.AgentChatHistoryEntity;
import xiaozhi.modules.agent.service.AgentChatHistoryService;
import xiaozhi.modules.agent.service.AgentChatSummaryService;
import xiaozhi.modules.agent.service.AgentChatTitleService;
import xiaozhi.modules.agent.service.AgentService;
import xiaozhi.modules.agent.vo.AgentInfoVO;
import xiaozhi.modules.device.entity.DeviceEntity;
import xiaozhi.modules.device.service.DeviceService;
import xiaozhi.modules.llm.service.LLMService;
import xiaozhi.modules.model.entity.ModelConfigEntity;
import xiaozhi.modules.model.service.ModelConfigService;

/**
 * Lớp triển khai dịch vụ tóm tắt bản ghi cuộc trò chuyện của tổng đài viên
 * Triển khai logic tóm tắt trong mem_local_short.py ở phía Python
 */
@Service
@RequiredArgsConstructor
public class AgentChatSummaryServiceImpl implements AgentChatSummaryService {

    private static final Logger log = LoggerFactory.getLogger(AgentChatSummaryServiceImpl.class);

    private final AgentChatHistoryService agentChatHistoryService;
    private final AgentService agentService;
    private final AgentChatTitleService agentChatTitleService;
    private final DeviceService deviceService;
    private final LLMService llmService;
    private final ModelConfigService modelConfigService;

    // Hằng số quy tắc tóm tắt
    private static final int MAX_SUMMARY_LENGTH = 1800; // Độ dài tóm tắt tối đa
    private static final Pattern JSON_PATTERN = Pattern.compile("\\{.*?\\}", Pattern.DOTALL);
    private static final Pattern DEVICE_CONTROL_PATTERN = Pattern.compile("Kiểm soát thiết bị|Vận hành thiết bị|thiết bị điều khiển|Trạng thái thiết bị",
            Pattern.CASE_INSENSITIVE);
    private static final Pattern WEATHER_PATTERN = Pattern.compile("thời tiết|nhiệt độ|Độ ẩm|lượng mưa|Khí tượng học", Pattern.CASE_INSENSITIVE);
    private static final Pattern DATE_PATTERN = Pattern.compile("Ngày|thời gian|tuần|tháng|Năm", Pattern.CASE_INSENSITIVE);

    private AgentChatSummaryDTO generateChatSummary(String sessionId) {
        try {
            System.out.println("Bắt đầu tạo phiên " + sessionId + " Tóm tắt lịch sử trò chuyện");

            // 1. Nhận bản ghi trò chuyện dựa trên sessionId
            List<AgentChatHistoryDTO> chatHistory = getChatHistoryBySessionId(sessionId);
            if (chatHistory == null || chatHistory.isEmpty()) {
                return new AgentChatSummaryDTO(sessionId, "Không tìm thấy lịch sử trò chuyện cho cuộc trò chuyện này");
            }

            // 2. Lấy thông tin đại lý
            String agentId = getAgentIdFromSession(sessionId, chatHistory);
            if (StringUtils.isBlank(agentId)) {
                return new AgentChatSummaryDTO(sessionId, "Không thể lấy được thông tin đại lý");
            }

            // 3. Trích xuất nội dung hội thoại chính
            List<String> meaningfulMessages = extractMeaningfulMessages(chatHistory);
            if (meaningfulMessages.isEmpty()) {
                return new AgentChatSummaryDTO(sessionId, "Không có nội dung hội thoại hợp lệ để tóm tắt");
            }

            // 4. Tạo bản tóm tắt (phương thức generateSummaryFromMessages đã chứa logic giới hạn độ dài)
            String summary = generateSummaryFromMessages(meaningfulMessages, agentId);

            log.info("Phiên được tạo thành công {} Tóm tắt lịch sử trò chuyện，chiều dài: {} nhân vật", sessionId, summary.length());
            return new AgentChatSummaryDTO(sessionId, agentId, summary);

        } catch (Exception e) {
            log.error("Tạo phiên {} Đã xảy ra lỗi khi tóm tắt lịch sử trò chuyện của: {}", sessionId, e.getMessage());
            return new AgentChatSummaryDTO(sessionId, "Đã xảy ra lỗi khi tạo bản tóm tắt: " + e.getMessage());
        }
    }

    @Override
    public boolean generateAndSaveChatSummary(String sessionId) {
        try {
            DeviceEntity device = getDeviceBySessionId(sessionId);
            if (device == null) {
                log.info("không tìm thấy phiên {} Thiết bị liên kết", sessionId);
                return false;
            }

            String agentId = device.getAgentId();
            String memModelId = agentService.getAgentById(agentId).getMemModelId();

            if (memModelId == null || memModelId.equals(Constant.MEMORY_MEM_REPORT_ONLY)) {
                log.info("phiên {} Sử dụng chế độ lịch sử trò chuyện chỉ báo cáo，Bỏ qua tóm tắt bộ nhớ", sessionId);
                return true;
            }

            boolean shouldSummarizeMemory = !memModelId.equals(Constant.MEMORY_NO_MEM)
                    && !memModelId.equals(Constant.MEMORY_MEM0AI)
                    && !memModelId.equals(Constant.MEMORY_POWERMEM);

            if (shouldSummarizeMemory) {
                AgentChatSummaryDTO summaryDTO = generateChatSummary(sessionId);
                if (summaryDTO.isSuccess()) {
                    agentService.updateAgentById(agentId, new AgentUpdateDTO() {
                        {
                            setSummaryMemory(summaryDTO.getSummary());
                        }
                    });
                    log.info("Đã lưu phiên thành công {} Các bản ghi trò chuyện được tóm tắt cho đại lý {}", sessionId, agentId);
                } else {
                    log.info("Không tạo được bản tóm tắt: {}", summaryDTO.getErrorMessage());
                }
            } else {
                log.info("phiên {} sử dụng {} chế độ，Bỏ qua tóm tắt bộ nhớ", sessionId, memModelId);
            }

            return true;

        } catch (Exception e) {
            log.error("lưu phiên {} Đã xảy ra lỗi khi tóm tắt lịch sử trò chuyện của: {}", sessionId, e.getMessage());
            return false;
        }
    }

    @Override
    public boolean generateAndSaveChatTitle(String sessionId) {
        try {
            // Tự động lấy AgentId
            String agentId = findAgentIdBySessionId(sessionId);
            if (StringUtils.isBlank(agentId)) {
                log.warn("phiên {} Không thể lấy được thông tin đại lý，Bỏ qua việc tạo tiêu đề", sessionId);
                return false;
            }

            List<AgentChatHistoryDTO> chatHistory = getChatHistoryBySessionId(sessionId);
            if (chatHistory == null || chatHistory.isEmpty()) {
                return false;
            }

            List<String> meaningfulMessages = extractMeaningfulMessages(chatHistory);
            if (meaningfulMessages.isEmpty()) {
                return false;
            }

            StringBuilder conversation = new StringBuilder();
            for (int i = 0; i < meaningfulMessages.size(); i++) {
                conversation.append("tin tức").append(i + 1).append(": ").append(meaningfulMessages.get(i)).append("\n");
            }

            String slmModelId = getSlmModelId(agentId);
            String title = llmService.generateTitle(conversation.toString(), slmModelId);

            if (StringUtils.isNotBlank(title)) {
                agentChatTitleService.saveOrUpdateTitle(sessionId, title);
                log.info("Đã lưu phiên thành công {} tiêu đề: {}", sessionId, title);
                return true;
            }
            return false;
        } catch (Exception e) {
            log.error("Tạo phiên {} Đã xảy ra lỗi với tiêu đề: {}", sessionId, e.getMessage());
            return false;
        }
    }

    private String getSlmModelId(String agentId) {
        try {
            if (StringUtils.isBlank(agentId)) {
                return null;
            }

            AgentInfoVO agentInfo = agentService.getAgentById(agentId);
            if (agentInfo == null) {
                return null;
            }

            String slmModelId = agentInfo.getSlmModelId();
            if (StringUtils.isNotBlank(slmModelId)) {
                log.info("phiên {} sử dụngSLMngười mẫu: {}", agentId, slmModelId);
                return slmModelId;
            }

            ModelConfigEntity defaultLlmConfig = getDefaultLLMConfig();
            if (defaultLlmConfig != null) {
                log.info("phiên {} Sử dụng mặc địnhLLMngười mẫu: {}", agentId, defaultLlmConfig.getId());
                return defaultLlmConfig.getId();
            }

            String llmModelId = agentInfo.getLlmModelId();
            log.info("phiên {} sử dụngLLMngười mẫu(quay lại cuối cùng): {}", agentId, llmModelId);
            return llmModelId;
        } catch (Exception e) {
            log.error("Nhận đại lýslmngười mẫuIDthất bại，agentId: {}, Lỗi: {}", agentId, e.getMessage());
            return null;
        }
    }

    private ModelConfigEntity getDefaultLLMConfig() {
        try {
            List<ModelConfigEntity> llmConfigs = modelConfigService.getEnabledModelsByType("LLM");
            if (llmConfigs == null || llmConfigs.isEmpty()) {
                return null;
            }

            for (ModelConfigEntity config : llmConfigs) {
                if (config.getIsDefault() != null && config.getIsDefault() == 1) {
                    return config;
                }
            }

            return llmConfigs.get(0);
        } catch (Exception e) {
            log.error("Nhận mặc địnhLLMCấu hình không thành công: {}", e.getMessage());
            return null;
        }
    }

    /**
     * Nhận lịch sử trò chuyện dựa trên ID phiên
     */
    private List<AgentChatHistoryDTO> getChatHistoryBySessionId(String sessionId) {
        try {
            // Tại đây bạn cần lấy bản ghi trò chuyện dựa trên sessionId
            // Vì giao diện hiện tại yêu cầu ID tác nhân nên trước tiên chúng ta cần tìm ID tác nhân được liên kết
            String agentId = findAgentIdBySessionId(sessionId);
            if (StringUtils.isBlank(agentId)) {
                return null;
            }
            return agentChatHistoryService.getChatHistoryBySessionId(agentId, sessionId);
        } catch (Exception e) {
            log.error("Nhận phiên {} Lịch sử trò chuyện không thành công: {}", sessionId, e.getMessage());
            return null;
        }
    }

    /**
     * Tìm ID tác nhân được liên kết dựa trên ID phiên
     */
    private String findAgentIdBySessionId(String sessionId) {
        try {
            // Truy vấn bản ghi đầu tiên của phiên để lấy AgentId
            QueryWrapper<AgentChatHistoryEntity> wrapper = new QueryWrapper<>();
            wrapper.select("agent_id")
                    .eq("session_id", sessionId)
                    .last("LIMIT 1");

            AgentChatHistoryEntity entity = agentChatHistoryService.getOne(wrapper);
            return entity != null ? entity.getAgentId() : null;
        } catch (Exception e) {
            log.error("Theo phiênID {} Tìm một đại lýIDthất bại: {}", sessionId, e.getMessage());
            return null;
        }
    }

    /**
     * Nhận ID đại lý từ phiên
     */
    private String getAgentIdFromSession(String sessionId, List<AgentChatHistoryDTO> chatHistory) {
        // Truy vấn ID đại lý trực tiếp từ cơ sở dữ liệu
        return findAgentIdBySessionId(sessionId);
    }

    /**
     * Trích xuất nội dung hội thoại có ý nghĩa (chỉ trích xuất tin nhắn của người dùng, loại trừ phản hồi của AI)
     */
    private List<String> extractMeaningfulMessages(List<AgentChatHistoryDTO> chatHistory) {
        List<String> meaningfulMessages = new ArrayList<>();

        for (AgentChatHistoryDTO message : chatHistory) {
            // Chỉ xử lý tin nhắn của người dùng (chatType = 1)
            if (message.getChatType() != null && message.getChatType() == 1) {
                String content = extractContentFromMessage(message);
                if (isMeaningfulMessage(content)) {
                    meaningfulMessages.add(content);
                }
            }
        }

        return meaningfulMessages;
    }

    /**
     * Trích xuất nội dung từ tin nhắn (xử lý định dạng JSON)
     */
    private String extractContentFromMessage(AgentChatHistoryDTO message) {
        String content = message.getContent();
        if (StringUtils.isBlank(content)) {
            return "";
        }

        // Xử lý nội dung có định dạng JSON (nhất quán về mặt logic với giao diện ChatHistoryDialog.vue)
        Matcher matcher = JSON_PATTERN.matcher(content);
        if (matcher.find()) {
            String jsonContent = matcher.group();
            // Xử lý đơn giản: trích xuất nội dung văn bản trong JSON
            return extractTextFromJson(jsonContent);
        }

        return content;
    }

    /**
     * Trích xuất nội dung văn bản từ JSON
     */
    private String extractTextFromJson(String jsonContent) {
        // Xử lý đơn giản: trích xuất giá trị của trường "nội dung"
        Pattern contentPattern = Pattern.compile("\"content\"\s*:\s*\"([^\"]*)\"");
        Matcher matcher = contentPattern.matcher(jsonContent);
        if (matcher.find()) {
            return matcher.group(1);
        }
        return jsonContent;
    }

    /**
     * Xác định xem tin nhắn có ý nghĩa hay không
     */
    private boolean isMeaningfulMessage(String content) {
        if (StringUtils.isBlank(content)) {
            return false;
        }

        // Loại trừ thông tin điều khiển thiết bị
        if (DEVICE_CONTROL_PATTERN.matcher(content).find()) {
            return false;
        }

        // Loại trừ nội dung không liên quan như ngày tháng, thời tiết, v.v.
        if (WEATHER_PATTERN.matcher(content).find() || DATE_PATTERN.matcher(content).find()) {
            return false;
        }

        // Loại trừ những tin nhắn quá ngắn
        return content.length() >= 5;
    }

    /**
     * Tạo bản tóm tắt từ tin nhắn
     */
    private String generateSummaryFromMessages(List<String> messages, String agentId) {
        if (messages.isEmpty()) {
            return "Cuộc trò chuyện này có ít nội dung hơn，Không có thông tin quan trọng để tóm tắt。";
        }

        // Xây dựng một cuộc trò chuyện hoàn chỉnh
        StringBuilder conversation = new StringBuilder();
        for (int i = 0; i < messages.size(); i++) {
            conversation.append("tin tức").append(i + 1).append(": ").append(messages.get(i)).append("\n");
        }

        try {
            // Lấy ký ức lịch sử của đại lý hiện tại
            String historyMemory = getCurrentAgentMemory(agentId);

            // Gọi dịch vụ LLM để tóm tắt thông minh, chuyển AgentId để có cấu hình mô hình chính xác
            String summary = callJavaLLMForSummaryWithHistory(conversation.toString(), historyMemory, agentId);

            // Áp dụng quy tắc tóm tắt: giới hạn độ dài tối đa
            if (summary.length() > MAX_SUMMARY_LENGTH) {
                summary = summary.substring(0, MAX_SUMMARY_LENGTH) + "...";
            }

            return summary;
        } catch (Exception e) {
            log.error("gọiJavakết thúcLLMDịch vụ không thành công: {}", e.getMessage());
            throw new RuntimeException("LLMDịch vụ không có sẵn，Không thể tạo tóm tắt trò chuyện");
        }
    }

    /**
     * Lấy ký ức lịch sử của đại lý hiện tại
     */
    private String getCurrentAgentMemory(String agentId) {
        try {
            if (StringUtils.isBlank(agentId)) {
                return null;
            }

            // Nhận thông tin đại lý
            AgentInfoVO agentInfo = agentService.getAgentById(agentId);
            if (agentInfo == null) {
                return null;
            }

            // Trả về bộ nhớ tóm tắt hiện tại của tác nhân
            return agentInfo.getSummaryMemory();
        } catch (Exception e) {
            log.error("Không thể lấy được bộ nhớ lịch sử đại lý，agentId: {}, Lỗi: {}", agentId, e.getMessage());
            return null;
        }
    }

    /**
     * Gọi dịch vụ LLM phía Java để có bản tóm tắt thông minh (hỗ trợ hợp nhất bộ nhớ lịch sử)
     */
    private String callJavaLLMForSummaryWithHistory(String conversation, String historyMemory, String agentId) {
        try {
            String modelId = getSlmModelId(agentId);

            if (StringUtils.isBlank(modelId)) {
                log.info("không tìm thấySLMngười mẫu，Sử dụng mặc địnhLLMdịch vụ");
                return llmService.generateSummaryWithHistory(conversation, historyMemory, null, null);
            }

            String summary = llmService.generateSummaryWithHistory(conversation, historyMemory, null, modelId);

            if (StringUtils.isNotBlank(summary) && !summary.equals("Dịch vụ tạm thời không khả dụng") && !summary.equals("Tạo bản tóm tắt không thành công")) {
                return summary;
            }

            throw new RuntimeException("Javakết thúcLLMDịch vụ trả về ngoại lệ: " + summary);

        } catch (Exception e) {
            log.error("gọiJavakết thúcLLMNgoại lệ dịch vụ，agentId: {}, Lỗi: {}", agentId, e.getMessage());
            throw e;
        }
    }

    /**
     * Gọi dịch vụ LLM phía Java để có bản tóm tắt thông minh
     */
    private String callJavaLLMForSummary(String conversation, String agentId) {
        try {
            String modelId = getSlmModelId(agentId);

            if (StringUtils.isBlank(modelId)) {
                log.info("không tìm thấySLMngười mẫu，Sử dụng mặc địnhLLMdịch vụ");
                return llmService.generateSummary(conversation);
            }

            String summary = llmService.generateSummaryWithModel(conversation, modelId);

            if (StringUtils.isNotBlank(summary) && !summary.equals("Dịch vụ tạm thời không khả dụng") && !summary.equals("Tạo bản tóm tắt không thành công")) {
                return summary;
            }

            throw new RuntimeException("Javakết thúcLLMDịch vụ trả về ngoại lệ: " + summary);

        } catch (Exception e) {
            log.error("gọiJavakết thúcLLMNgoại lệ dịch vụ，agentId: {}, Lỗi: {}", agentId, e.getMessage());
            throw e;
        }
    }

    /**
     * Lấy ID mô hình LLM của bản tóm tắt bộ nhớ
     */
    private String getMemorySummaryModelId(String agentId) {
        try {
            if (StringUtils.isBlank(agentId)) {
                return null;
            }

            // Nhận thông tin đại lý
            AgentInfoVO agentInfo = agentService.getAgentById(agentId);
            if (agentInfo == null) {
                return null;
            }

            // Lấy ID mô hình bộ nhớ của tác nhân
            String memModelId = agentInfo.getMemModelId();
            if (StringUtils.isBlank(memModelId)) {
                return null;
            }

            // Nhận cấu hình mô hình bộ nhớ
            ModelConfigEntity memModelConfig = modelConfigService.getModelByIdFromCache(memModelId);
            if (memModelConfig == null || memModelConfig.getConfigJson() == null) {
                return null;
            }

            // Trích xuất ID mô hình LLM tương ứng từ cấu hình mô hình bộ nhớ
            Map<String, Object> configMap = memModelConfig.getConfigJson();
            String llmModelId = (String) configMap.get("llm");

            if (StringUtils.isBlank(llmModelId)) {
                // Nếu mô hình bộ nhớ không được định cấu hình bằng LLM riêng thì mô hình LLM mặc định của tác nhân sẽ được sử dụng.
                return agentInfo.getLlmModelId();
            }

            return llmModelId;
        } catch (Exception e) {
            log.error("Nhận tóm tắt bộ nhớLLMngười mẫuIDthất bại，agentId: {}, Lỗi: {}", agentId, e.getMessage());
            return null;
        }
    }

    /**
     * Nhận thông tin thiết bị dựa trên ID phiên
     */
    private DeviceEntity getDeviceBySessionId(String sessionId) {
        try {
            // Truy vấn bản ghi đầu tiên của phiên để lấy macAddress
            QueryWrapper<AgentChatHistoryEntity> wrapper = new QueryWrapper<>();
            wrapper.select("mac_address")
                    .eq("session_id", sessionId)
                    .last("LIMIT 1");

            AgentChatHistoryEntity entity = agentChatHistoryService.getOne(wrapper);
            if (entity != null && StringUtils.isNotBlank(entity.getMacAddress())) {
                return deviceService.getDeviceByMacAddress(entity.getMacAddress());
            }
            return null;
        } catch (Exception e) {
            log.error("Theo phiênID {} Không tìm thấy thông tin thiết bị: {}", sessionId, e.getMessage());
            return null;
        }
    }
}