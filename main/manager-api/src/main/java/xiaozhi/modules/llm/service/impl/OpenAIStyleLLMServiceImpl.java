package xiaozhi.modules.llm.service.impl;

import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

import org.apache.commons.lang3.StringUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import cn.hutool.json.JSONArray;
import cn.hutool.json.JSONObject;
import cn.hutool.json.JSONUtil;
import lombok.extern.slf4j.Slf4j;
import xiaozhi.modules.llm.service.LLMService;
import xiaozhi.modules.model.entity.ModelConfigEntity;
import xiaozhi.modules.model.service.ModelConfigService;

/**
 * Triển khai dịch vụ LLM của API kiểu OpenAI
 * Hỗ trợ các mô hình tương thích API OpenAI như Alibaba Cloud, DeepSeek, ChatGLM, v.v.
 */
@Slf4j
@Service
public class OpenAIStyleLLMServiceImpl implements LLMService {

    // Tên miền nền tảng và các tham số tương ứng của nó cần tắt chế độ tư duy
    private static final Map<String, Map<String, Object>> THINKING_DISABLED_DOMAINS = new LinkedHashMap<>();
    static {
        THINKING_DISABLED_DOMAINS.put("aliyuncs.com", Map.of("enable_thinking", false));
        Map<String, Object> thinkingDisabled = Map.of("thinking", Map.of("type", "disabled"));
        THINKING_DISABLED_DOMAINS.put("bigmodel.cn", thinkingDisabled);
        THINKING_DISABLED_DOMAINS.put("moonshot.cn", thinkingDisabled);
        THINKING_DISABLED_DOMAINS.put("volces.com", thinkingDisabled);
    }

    @Autowired
    private ModelConfigService modelConfigService;

    private final RestTemplate restTemplate = new RestTemplate();

    /**
     * Tự động tắt chế độ suy nghĩ dựa trên tên miền
     */
    private void applyThinkingDisabled(String baseUrl, Map<String, Object> requestBody) {
        for (Map.Entry<String, Map<String, Object>> entry : THINKING_DISABLED_DOMAINS.entrySet()) {
            if (baseUrl.contains(entry.getKey())) {
                requestBody.putAll(entry.getValue());
                log.info("cho tên miền {} Tắt chế độ suy nghĩ，thông số: {}", baseUrl, entry.getValue());
                break;
            }
        }
    }

    private static final String DEFAULT_SUMMARY_PROMPT = "Bạn là bộ phận tóm tắt ký ức cho trợ lý giọng nói tiếng Việt.\n"
            + "Nhiệm vụ: trích xuất thông tin bền vững và hữu ích về người dùng để cá nhân hóa các cuộc trò chuyện sau này.\n"
            + "Quy tắc:\n"
            + "1. Chỉ lưu thông tin có giá trị lâu dài như tên, cách xưng hô, nghề nghiệp, sở thích, người thân, địa điểm thường dùng, thiết bị nhà thông minh và sở thích giao tiếp.\n"
            + "2. Không lưu câu chào hỏi, câu tạm biệt, lệnh điều khiển thiết bị một lần, kết quả thời tiết/tin tức nhất thời, lỗi hệ thống hoặc nội dung vô nghĩa.\n"
            + "3. Không lặp lại ký ức cũ. Nếu có ký ức lịch sử, hãy hợp nhất với thông tin mới, giữ thông tin còn đúng và cập nhật thông tin mâu thuẫn bằng dữ liệu mới hơn.\n"
            + "4. Không thêm mã, XML, Markdown, lời giải thích hoặc ghi chú ngoài bản tóm tắt.\n"
            + "5. Viết bằng tiếng Việt tự nhiên, ngắn gọn, tối đa khoảng 1800 từ.\n"
            + "6. Nếu cuộc trò chuyện mới không có thông tin đáng lưu, hãy trả lại ký ức lịch sử hiện có; nếu không có ký ức lịch sử thì trả chuỗi rỗng.\n\n"
            + "Ký ức lịch sử:\n{history_memory}\n\n"
            + "Nội dung hội thoại mới:\n{conversation}";

    private static final String DEFAULT_TITLE_PROMPT = "Đọc đoạn hội thoại dưới đây và tạo một tiêu đề phiên thật ngắn bằng tiếng Việt, tối đa khoảng 15 từ. Chỉ trả về tiêu đề, không giải thích, không thêm dấu câu ở cuối:\n{conversation}";

    @Override
    public String generateSummary(String conversation) {
        return generateSummary(conversation, null, null);
    }

    @Override
    public String generateSummaryWithModel(String conversation, String modelId) {
        return generateSummary(conversation, null, modelId);
    }

    @Override
    public String generateSummary(String conversation, String promptTemplate, String modelId) {
        if (!isAvailable()) {
            log.warn("Dịch vụ LLM không khả dụng, không thể tạo tóm tắt");
            return "Dịch vụ LLM không khả dụng, không thể tạo tóm tắt";
        }

        try {
            // Lấy cấu hình mô hình LLM từ bảng điều khiển thông minh
            ModelConfigEntity llmConfig;
            if (modelId != null && !modelId.trim().isEmpty()) {
                // Lấy cấu hình qua ID mô hình cụ thể
                llmConfig = modelConfigService.getModelByIdFromCache(modelId);
            } else {
                // Để duy trì khả năng tương thích ngược, hãy sử dụng cấu hình mặc định
                llmConfig = getDefaultLLMConfig();
            }

            if (llmConfig == null || llmConfig.getConfigJson() == null) {
                log.error("Không tìm thấy cấu hình mô hình LLM khả dụng, modelId: {}", modelId);
                return "Không tìm thấy cấu hình mô hình LLM khả dụng";
            }

            JSONObject configJson = llmConfig.getConfigJson();
            String baseUrl = configJson.getStr("base_url");
            String model = configJson.getStr("model_name");
            String apiKey = configJson.getStr("api_key");
            Double temperature = configJson.getDouble("temperature");
            Integer maxTokens = configJson.getInt("max_tokens");

            if (StringUtils.isBlank(baseUrl) || StringUtils.isBlank(apiKey)) {
                log.error("Cấu hình LLM không đầy đủ, baseUrl hoặc apiKey trống");
                return "Cấu hình LLM không đầy đủ, không thể tạo tóm tắt";
            }

            // Xây dựng các từ gợi ý
            String prompt = (promptTemplate != null ? promptTemplate : DEFAULT_SUMMARY_PROMPT).replace("{conversation}",
                    conversation);

            // Xây dựng thân yêu cầu
            Map<String, Object> requestBody = new HashMap<>();
            requestBody.put("model", model != null ? model : "gpt-3.5-turbo");

            Map<String, Object>[] messages = new Map[1];
            Map<String, Object> message = new HashMap<>();
            message.put("role", "user");
            message.put("content", prompt);
            messages[0] = message;

            requestBody.put("messages", messages);
            requestBody.put("temperature", temperature != null ? temperature : 0.7);
            requestBody.put("max_tokens", maxTokens != null ? maxTokens : 2000);

            // Vô hiệu hóa chế độ suy nghĩ
            applyThinkingDisabled(baseUrl, requestBody);

            // Gửi yêu cầu HTTP
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            headers.set("Authorization", "Bearer " + apiKey);

            HttpEntity<Map<String, Object>> entity = new HttpEntity<>(requestBody, headers);

            // Xây dựng URL API đầy đủ
            String apiUrl = baseUrl;
            if (!apiUrl.endsWith("/chat/completions")) {
                if (!apiUrl.endsWith("/")) {
                    apiUrl += "/";
                }
                apiUrl += "chat/completions";
            }

            ResponseEntity<String> response = restTemplate.exchange(
                    apiUrl, HttpMethod.POST, entity, String.class);

            if (response.getStatusCode().is2xxSuccessful()) {
                JSONObject responseJson = JSONUtil.parseObj(response.getBody());
                JSONArray choices = responseJson.getJSONArray("choices");
                if (choices != null && choices.size() > 0) {
                    JSONObject choice = choices.getJSONObject(0);
                    JSONObject messageObj = choice.getJSONObject("message");
                    return messageObj.getStr("content");
                }
            } else {
                log.error("Gọi LLM API thất bại, mã trạng thái: {}, phản hồi: {}", response.getStatusCode(), response.getBody());
            }
        } catch (Exception e) {
            log.error("{Xảy ra ngoại lệ khi gọi dịch vụ LLM để tạo tóm tắt, modelId: {}{}", modelId, e);
        }

        return "Tạo tóm tắt thất bại, vui lòng thử lại sau";
    }

    @Override
    public String generateSummary(String conversation, String promptTemplate) {
        return generateSummary(conversation, promptTemplate, null);
    }

    @Override
    public String generateSummaryWithHistory(String conversation, String historyMemory, String promptTemplate,
            String modelId) {
        if (!isAvailable()) {
            log.warn("Dịch vụ LLM không khả dụng, không thể tạo tóm tắt");
            return "Dịch vụ LLM không khả dụng, không thể tạo tóm tắt";
        }

        try {
            // Lấy cấu hình mô hình LLM từ bảng điều khiển thông minh
            ModelConfigEntity llmConfig;
            if (modelId != null && !modelId.trim().isEmpty()) {
                llmConfig = modelConfigService.getModelByIdFromCache(modelId);
            } else {
                llmConfig = getDefaultLLMConfig();
            }

            if (llmConfig == null || llmConfig.getConfigJson() == null) {
                log.error("Không tìm thấy cấu hình mô hình LLM khả dụng, modelId: {}", modelId);
                return "Không tìm thấy cấu hình mô hình LLM khả dụng";
            }

            JSONObject configJson = llmConfig.getConfigJson();
            String baseUrl = configJson.getStr("base_url");
            String model = configJson.getStr("model_name");
            String apiKey = configJson.getStr("api_key");

            if (StringUtils.isBlank(baseUrl) || StringUtils.isBlank(apiKey)) {
                log.error("Cấu hình LLM không đầy đủ, baseUrl hoặc apiKey trống");
                return "Cấu hình LLM không đầy đủ, không thể tạo tóm tắt";
            }

            // Xây dựng từ gợi ý (prompt), bao gồm bộ nhớ lịch sử
            String prompt = (promptTemplate != null ? promptTemplate : DEFAULT_SUMMARY_PROMPT)
                    .replace("{history_memory}", historyMemory != null ? historyMemory : "Không có bộ nhớ lịch sử")
                    .replace("{conversation}", conversation);

            // Xây dựng thân yêu cầu
            Map<String, Object> requestBody = new HashMap<>();
            requestBody.put("model", model != null ? model : "gpt-3.5-turbo");

            Map<String, Object>[] messages = new Map[1];
            Map<String, Object> message = new HashMap<>();
            message.put("role", "user");
            message.put("content", prompt);
            messages[0] = message;

            requestBody.put("messages", messages);
            requestBody.put("temperature", 0.2);
            requestBody.put("max_tokens", 2000);

            // Vô hiệu hóa chế độ suy nghĩ
            applyThinkingDisabled(baseUrl, requestBody);

            // Gửi yêu cầu HTTP
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            headers.set("Authorization", "Bearer " + apiKey);

            HttpEntity<Map<String, Object>> entity = new HttpEntity<>(requestBody, headers);

            // Xây dựng URL API đầy đủ
            String apiUrl = baseUrl;
            if (!apiUrl.endsWith("/chat/completions")) {
                if (!apiUrl.endsWith("/")) {
                    apiUrl += "/";
                }
                apiUrl += "chat/completions";
            }

            ResponseEntity<String> response = restTemplate.exchange(
                    apiUrl, HttpMethod.POST, entity, String.class);

            if (response.getStatusCode().is2xxSuccessful()) {
                JSONObject responseJson = JSONUtil.parseObj(response.getBody());
                JSONArray choices = responseJson.getJSONArray("choices");
                if (choices != null && choices.size() > 0) {
                    JSONObject choice = choices.getJSONObject(0);
                    JSONObject messageObj = choice.getJSONObject("message");
                    return messageObj.getStr("content");
                }
            } else {
                log.error("Gọi LLM API thất bại, mã trạng thái: {}, phản hồi: {}", response.getStatusCode(), response.getBody());
            }
        } catch (Exception e) {
            log.error("{Xảy ra ngoại lệ khi gọi dịch vụ LLM để tạo tóm tắt, modelId: {}{}", modelId, e);
        }

        return "Tạo tóm tắt thất bại, vui lòng thử lại sau";
    }

    @Override
    public boolean isAvailable() {
        try {
            ModelConfigEntity defaultLLMConfig = getDefaultLLMConfig();
            if (defaultLLMConfig == null || defaultLLMConfig.getConfigJson() == null) {
                return false;
            }

            JSONObject configJson = defaultLLMConfig.getConfigJson();
            String baseUrl = configJson.getStr("base_url");
            String apiKey = configJson.getStr("api_key");

            return baseUrl != null && !baseUrl.trim().isEmpty() &&
                    apiKey != null && !apiKey.trim().isEmpty();
        } catch (Exception e) {
            log.error("Xảy ra ngoại lệ khi kiểm tra tính khả dụng của dịch vụ LLM:", e);
            return false;
        }
    }

    @Override
    public boolean isAvailable(String modelId) {
        try {
            if (modelId == null || modelId.trim().isEmpty()) {
                return isAvailable();
            }

            // Lấy cấu hình qua ID mô hình cụ thể
            ModelConfigEntity modelConfig = modelConfigService.getModelByIdFromCache(modelId);
            if (modelConfig == null || modelConfig.getConfigJson() == null) {
                log.warn("Không tìm thấy cấu hình mô hình LLM chỉ định, modelId: {}", modelId);
                return false;
            }

            JSONObject configJson = modelConfig.getConfigJson();
            String baseUrl = configJson.getStr("base_url");
            String apiKey = configJson.getStr("api_key");

            return baseUrl != null && !baseUrl.trim().isEmpty() &&
                    apiKey != null && !apiKey.trim().isEmpty();
        } catch (Exception e) {
            log.error("Xảy ra ngoại lệ khi kiểm tra tính khả dụng của dịch vụ LLM, modelId: {}", modelId, e);
            return false;
        }
    }

    /**
     * Lấy cấu hình mô hình LLM mặc định từ bảng điều khiển thông minh
     */
    private ModelConfigEntity getDefaultLLMConfig() {
        try {
            // Lấy tất cả cấu hình mô hình LLM đang bật
            List<ModelConfigEntity> llmConfigs = modelConfigService.getEnabledModelsByType("LLM");
            if (llmConfigs == null || llmConfigs.isEmpty()) {
                return null;
            }

            // Ưu tiên trả về cấu hình mặc định, nếu không có cấu hình mặc định thì trả về cấu hình đầu tiên đang bật
            for (ModelConfigEntity config : llmConfigs) {
                if (config.getIsDefault() != null && config.getIsDefault() == 1) {
                    return config;
                }
            }

            return llmConfigs.get(0);
        } catch (Exception e) {
            log.error("Xảy ra ngoại lệ khi lấy cấu hình mô hình LLM:", e);
            return null;
        }
    }

    @Override
    public String generateTitle(String conversation, String modelId) {
        if (!isAvailable()) {
            log.warn("Dịch vụ LLM không khả dụng, không thể tạo tiêu đề");
            return null;
        }

        try {
            ModelConfigEntity llmConfig;
            if (modelId != null && !modelId.trim().isEmpty()) {
                llmConfig = modelConfigService.getModelByIdFromCache(modelId);
            } else {
                llmConfig = getDefaultLLMConfig();
            }

            if (llmConfig == null || llmConfig.getConfigJson() == null) {
                log.error("Không tìm thấy cấu hình mô hình LLM khả dụng, modelId: {}", modelId);
                return null;
            }

            JSONObject configJson = llmConfig.getConfigJson();
            String baseUrl = configJson.getStr("base_url");
            String model = configJson.getStr("model_name");
            String apiKey = configJson.getStr("api_key");

            if (StringUtils.isBlank(baseUrl) || StringUtils.isBlank(apiKey)) {
                log.error("Cấu hình LLM không đầy đủ, baseUrl hoặc apiKey trống");
                return null;
            }

            String prompt = DEFAULT_TITLE_PROMPT.replace("{conversation}", conversation);

            Map<String, Object> requestBody = new HashMap<>();
            requestBody.put("model", model != null ? model : "gpt-3.5-turbo");

            Map<String, Object>[] messages = new Map[1];
            Map<String, Object> message = new HashMap<>();
            message.put("role", "user");
            message.put("content", prompt);
            messages[0] = message;

            requestBody.put("messages", messages);
            requestBody.put("temperature", 0.3);
            requestBody.put("max_tokens", 50);

            // Vô hiệu hóa chế độ suy nghĩ
            applyThinkingDisabled(baseUrl, requestBody);

            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            headers.set("Authorization", "Bearer " + apiKey);

            HttpEntity<Map<String, Object>> entity = new HttpEntity<>(requestBody, headers);

            String apiUrl = baseUrl;
            if (!apiUrl.endsWith("/chat/completions")) {
                if (!apiUrl.endsWith("/")) {
                    apiUrl += "/";
                }
                apiUrl += "chat/completions";
            }

            ResponseEntity<String> response = restTemplate.exchange(
                    apiUrl, HttpMethod.POST, entity, String.class);

            if (response.getStatusCode().is2xxSuccessful()) {
                JSONObject responseJson = JSONUtil.parseObj(response.getBody());
                JSONArray choices = responseJson.getJSONArray("choices");
                if (choices != null && choices.size() > 0) {
                    JSONObject choice = choices.getJSONObject(0);
                    JSONObject messageObj = choice.getJSONObject("message");
                    String title = messageObj.getStr("content");
                    if (StringUtils.isNotBlank(title)) {
                        title = title.trim().replaceAll("[，。！？、：；''\"\"【】（）]", "");
                        if (title.length() > 15) {
                            title = title.substring(0, 15);
                        }
                        return title;
                    }
                }
            } else {
                log.error("Gọi LLM API thất bại, mã trạng thái: {}, phản hồi: {}", response.getStatusCode(), response.getBody());
            }
        } catch (Exception e) {
            log.error("{Xảy ra ngoại lệ khi gọi dịch vụ LLM để tạo tiêu đề, modelId: {}{}", modelId, e);
        }

        return null;
    }
}
