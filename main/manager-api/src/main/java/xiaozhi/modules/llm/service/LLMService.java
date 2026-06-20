package xiaozhi.modules.llm.service;

/**
 * Giao diện dịch vụ LLM
 * Hỗ trợ nhiều cuộc gọi mô hình lớn
 */
public interface LLMService {

    /**
     * Tạo tóm tắt lịch sử trò chuyện
     *
     * @param nội dung cuộc trò chuyện cuộc trò chuyện
     * @param-promptTemplate mẫu từ nhắc nhở
     * @return tóm tắt kết quả
     */
    String generateSummary(String conversation, String promptTemplate);

    /**
     * Tạo tóm tắt trò chuyện (sử dụng các từ nhắc nhở mặc định)
     *
     * @param nội dung cuộc trò chuyện cuộc trò chuyện
     * @return tóm tắt kết quả
     */
    String generateSummary(String conversation);

    /**
     * Tạo bản tóm tắt bản ghi trò chuyện (chỉ định ID mẫu)
     *
     * @param nội dung cuộc trò chuyện cuộc trò chuyện
     * @param modelId ID mô hình
     * @return tóm tắt kết quả
     */
    String generateSummaryWithModel(String conversation, String modelId);

    /**
     * Tạo bản tóm tắt bản ghi trò chuyện (chỉ định ID mẫu và mẫu từ nhắc nhở)
     *
     * @param nội dung cuộc trò chuyện cuộc trò chuyện
     * @param-promptTemplate mẫu từ nhắc nhở
     * @param modelId ID mô hình
     * @return tóm tắt kết quả
     */
    String generateSummary(String conversation, String promptTemplate, String modelId);

    /**
     * Tạo bản tóm tắt bản ghi trò chuyện (bao gồm cả việc hợp nhất bộ nhớ lịch sử)
     *
     * @param nội dung cuộc trò chuyện cuộc trò chuyện
     * @param historyBộ nhớ lịch sử bộ nhớ
     * @param-promptTemplate mẫu từ nhắc nhở
     * @param modelId ID mô hình
     * @return tóm tắt kết quả
     */
    String generateSummaryWithHistory(String conversation, String historyMemory, String promptTemplate, String modelId);

    /**
     * Kiểm tra xem dịch vụ có sẵn không
     *
     * @return có sẵn
     */
    boolean isAvailable();

    /**
     * Kiểm tra xem dịch vụ cho kiểu máy được chỉ định có khả dụng hay không
     *
     * @param modelId ID mô hình
     * @return có sẵn
     */
    boolean isAvailable(String modelId);

    /**
     * Tạo tiêu đề phiên
     *
     * @param nội dung cuộc trò chuyện cuộc trò chuyện
     * @param modelId ID mô hình
     * @return tiêu đề (khoảng 15 từ)
     */
    String generateTitle(String conversation, String modelId);
}