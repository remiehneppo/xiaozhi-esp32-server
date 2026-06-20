package xiaozhi.modules.agent.service.impl;

import java.net.URI;
import java.net.URISyntaxException;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.util.List;
import java.util.Map;
import java.util.concurrent.TimeUnit;
import java.util.stream.Collectors;

import org.apache.commons.lang3.StringUtils;
import org.springframework.stereotype.Service;

import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import xiaozhi.common.constant.Constant;
import xiaozhi.common.utils.AESUtils;
import xiaozhi.common.utils.HashEncryptionUtil;
import xiaozhi.common.utils.JsonUtils;
import xiaozhi.modules.agent.Enums.XiaoZhiMcpJsonRpcJson;
import xiaozhi.modules.agent.service.AgentMcpAccessPointService;
import xiaozhi.modules.sys.service.SysParamsService;
import xiaozhi.modules.sys.utils.WebSocketClientManager;

@AllArgsConstructor
@Service
@Slf4j
public class AgentMcpAccessPointServiceImpl implements AgentMcpAccessPointService {
    private SysParamsService sysParamsService;

    @Override
    public String getAgentMcpAccessAddress(String id) {
        // Lấy địa chỉ của mcp
        String url = sysParamsService.getValue(Constant.SERVER_MCP_ENDPOINT, true);
        if (StringUtils.isBlank(url) || "null".equals(url)) {
            return null;
        }
        URI uri = getURI(url);
        // Lấy tiền tố url của đại lý mcp
        String agentMcpUrl = getAgentMcpUrl(uri);
        // Nhận chìa khóa
        String key = getSecretKey(uri);
        // Nhận mã thông báo được mã hóa
        String encryptToken = encryptToken(id, key);
        // Mã hóa URL mã thông báo
        String encodedToken = URLEncoder.encode(encryptToken, StandardCharsets.UTF_8);
        // Trả về định dạng của đường dẫn Mcp của tác nhân
        agentMcpUrl = "%s/mcp/?token=%s".formatted(agentMcpUrl, encodedToken);
        return agentMcpUrl;
    }

    @Override
    public List<String> getAgentMcpToolsList(String id) {
        String wsUrl = getAgentMcpAccessAddress(id);
        if (StringUtils.isBlank(wsUrl)) {
            return List.of();
        }

        // Thay thế/mcp bằng/gọi
        wsUrl = wsUrl.replace("/mcp/", "/call/");

        try {
            // Tạo kết nối WebSocket và tăng thời gian chờ lên 15 giây
            try (WebSocketClientManager client = WebSocketClientManager.build(
                    new WebSocketClientManager.Builder()
                            .uri(wsUrl)
                            .bufferSize(1024 * 1024)
                            .connectTimeout(8, TimeUnit.SECONDS)
                            .maxSessionDuration(10, TimeUnit.SECONDS))) {

                // Bước 1: Gửi tin nhắn khởi tạo và chờ phản hồi
                log.info("gửiMCPthông báo khởi tạo，đại lýID: {}", id);
                client.sendText(XiaoZhiMcpJsonRpcJson.getInitializeJson());

                // Đợi phản hồi khởi tạo (id=1) - xóa độ trễ cố định và thay đổi thành hướng phản hồi
                List<String> initResponses = client.listenerWithoutClose(response -> {
                    try {
                        Map<String, Object> jsonMap = JsonUtils.parseObject(response, Map.class);
                        if (jsonMap != null && Integer.valueOf(1).equals(jsonMap.get("id"))) {
                            // Kiểm tra xem có trường kết quả hay không, cho biết khởi tạo thành công
                            return jsonMap.containsKey("result") && !jsonMap.containsKey("error");
                        }
                        return false;
                    } catch (Exception e) {
                        log.warn("Không thể phân tích cú pháp phản hồi khởi tạo: {}", response, e);
                        return false;
                    }
                });

                // Xác minh phản hồi khởi tạo
                boolean initSucceeded = false;
                for (String response : initResponses) {
                    try {
                        Map<String, Object> jsonMap = JsonUtils.parseObject(response, Map.class);
                        if (jsonMap != null && Integer.valueOf(1).equals(jsonMap.get("id"))) {
                            if (jsonMap.containsKey("result")) {
                                log.info("MCPKhởi tạo thành công，đại lýID: {}", id);
                                initSucceeded = true;
                                break;
                            } else if (jsonMap.containsKey("error")) {
                                log.error("MCPKhởi tạo không thành công，đại lýID: {}, Lỗi: {}", id, jsonMap.get("error"));
                                return List.of();
                            }
                        }
                    } catch (Exception e) {
                        log.warn("Không thể xử lý phản hồi khởi tạo: {}", response, e);
                    }
                }

                if (!initSucceeded) {
                    log.error("Không nhận được hợp lệMCPphản hồi khởi tạo，đại lýID: {}", id);
                    return List.of();
                }

                // Bước 2: Gửi thông báo hoàn thành khởi tạo - chỉ gửi sau khi nhận được phản hồi khởi tạo
                log.info("gửiMCPThông báo hoàn thành khởi tạo，đại lýID: {}", id);
                client.sendText(XiaoZhiMcpJsonRpcJson.getNotificationsInitializedJson());
                // Bước 3: Gửi yêu cầu danh sách công cụ - ngay lập tức, không chậm trễ
                log.info("gửiMCPYêu cầu danh sách công cụ，đại lýID: {}", id);
                client.sendText(XiaoZhiMcpJsonRpcJson.getToolsListJson());

                // Đang chờ phản hồi danh sách công cụ (id=2)
                List<String> toolsResponses = client.listener(response -> {
                    try {
                        Map<String, Object> jsonMap = JsonUtils.parseObject(response, Map.class);
                        return jsonMap != null && Integer.valueOf(2).equals(jsonMap.get("id"));
                    } catch (Exception e) {
                        log.warn("Phản hồi danh sách công cụ phân tích cú pháp không thành công: {}", response, e);
                        return false;
                    }
                });

                // Xử lý phản hồi danh sách công cụ
                for (String response : toolsResponses) {
                    try {
                        Map<String, Object> jsonMap = JsonUtils.parseObject(response, Map.class);
                        if (jsonMap != null && Integer.valueOf(2).equals(jsonMap.get("id"))) {
                            // Kiểm tra xem có trường kết quả không
                            Object resultObj = jsonMap.get("result");
                            if (resultObj instanceof Map) {
                                Map<String, Object> resultMap = (Map<String, Object>) resultObj;
                                Object toolsObj = resultMap.get("tools");
                                if (toolsObj instanceof List) {
                                    List<Map<String, Object>> toolsList = (List<Map<String, Object>>) toolsObj;
                                    // Danh sách tên công cụ trích xuất
                                    List<String> result = toolsList.stream()
                                            .map(tool -> (String) tool.get("name"))
                                            .filter(name -> name != null)
                                            .sorted()
                                            .collect(Collectors.toList());
                                    log.info("thu được thành côngMCPDanh sách công cụ，đại lýID: {}, Số lượng công cụ: {}", id, result.size());
                                    return result;
                                }
                            } else if (jsonMap.containsKey("error")) {
                                log.error("Không lấy được danh sách công cụ，đại lýID: {}, Lỗi: {}", id, jsonMap.get("error"));
                                return List.of();
                            }
                        }
                    } catch (Exception e) {
                        log.warn("Phản hồi danh sách công cụ xử lý không thành công: {}", response, e);
                    }
                }

                log.warn("Không tìm thấy phản hồi danh sách công cụ hợp lệ，đại lýID: {}", id);
                return List.of();

            }
        } catch (Exception e) {
            log.error("Nhận đại lý MCP Danh sách công cụ không thành công，đại lýID: {},Lý do lỗi：{}", id, e.getMessage());
            return List.of();
        }
    }

    /**
     * Nhận đối tượng URI
     *
     * đường dẫn url @param
     * @return đối tượng URI
     */
    private static URI getURI(String url) {
        try {
            return new URI(url);
        } catch (URISyntaxException e) {
            log.error("Định dạng đường dẫn là đường dẫn không chính xác：{}，\nthông báo lỗi:{}", url, e.getMessage());
            throw new RuntimeException("mcpCó lỗi trong địa chỉ，Vui lòng nhập quản lý tham số để sửa đổimcpđịa chỉ điểm truy cập");
        }
    }

    /**
     * Nhận chìa khóa
     *
     * @param uri địa chỉ mcp
     * @return chìa khóa
     */
    private static String getSecretKey(URI uri) {
        // Nhận thông số
        String query = uri.getQuery();
        // Nhận khóa mã hóa aes
        String str = "key=";
        return query.substring(query.indexOf(str) + str.length());
    }

    /**
     * Nhận url điểm truy cập mcp của đại lý
     *
     * @param uri địa chỉ mcp
     * @return đại lý url điểm truy cập mcp
     */
    private String getAgentMcpUrl(URI uri) {
        // Nhận thỏa thuận
        String wsScheme = (uri.getScheme().equals("https")) ? "wss" : "ws";
        // Nhận máy chủ, cổng, đường dẫn
        String path = uri.getSchemeSpecificPart();
        // Nhận đường dẫn trước / cuối cùng
        path = path.substring(0, path.lastIndexOf("/"));
        return wsScheme + ":" + path;
    }

    /**
     * Nhận mã thông báo được mã hóa của id đại lý
     *
     * @param AgentId id đại lý
     * Khóa mã hóa khóa @param
     * @return mã thông báo được mã hóa
     */
    private static String encryptToken(String agentId, String key) {
        // Sử dụng md5 để mã hóa ID tác nhân
        String md5 = HashEncryptionUtil.Md5hexDigest(agentId);
        // aes yêu cầu văn bản được mã hóa
        String json = "{\"agentId\": \"%s\"}".formatted(md5);
        // Được mã hóa thành giá trị mã thông báo
        return AESUtils.encrypt(key, json);
    }
}