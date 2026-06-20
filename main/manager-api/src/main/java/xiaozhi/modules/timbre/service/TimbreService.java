package xiaozhi.modules.timbre.service;

import java.util.List;

import xiaozhi.common.page.PageData;
import xiaozhi.common.service.BaseService;
import xiaozhi.modules.model.dto.VoiceDTO;
import xiaozhi.modules.timbre.dto.TimbreDataDTO;
import xiaozhi.modules.timbre.dto.TimbrePageDTO;
import xiaozhi.modules.timbre.entity.TimbreEntity;
import xiaozhi.modules.timbre.vo.TimbreDetailsVO;

/**
 * Định nghĩa lớp kinh doanh âm sắc
 *
 * @author zjy
 * @since 2025-3-21
 */
public interface TimbreService extends BaseService<TimbreEntity> {
    /**
     * Phân trang để lấy âm sắc theo âm sắc quy định tts
     *
     * @param dto tham số tìm kiếm phân trang
     * @return dữ liệu phân trang danh sách âm sắc
     */
    PageData<TimbreDetailsVO> page(TimbrePageDTO dto);

    /**
     * Nhận thông tin chi tiết về id được chỉ định của âm sắc
     *
     * @param âm sắcId id bảng âm sắc
     * @return thông tin âm sắc
     */
    TimbreDetailsVO get(String timbreId);

    /**
     * Lưu thông tin âm thanh
     *
     * @param dto cần lưu dữ liệu
     */
    void save(TimbreDataDTO dto);

    /**
     * Lưu thông tin âm thanh
     *
     * @param timbreId id cần sửa đổi
     * @param dvào dữ liệu cần sửa đổi
     */
    void update(String timbreId, TimbreDataDTO dto);

    /**
     * Xóa âm thanh hàng loạt
     *
     * @param id danh sách id âm sắc sẽ bị xóa
     */
    void delete(String[] ids);

    List<VoiceDTO> getVoiceNames(String ttsModelId, String voiceName);

    /**
     * Lấy tên âm sắc dựa trên ID
     *
     * @param id ID âm sắc
     * @return tên âm sắc
     */
    String getTimbreNameById(String id);

    /**
     * Lấy thông tin âm sắc dựa trên mã hóa âm sắc
     *
     * @param ttsModelId ID mô hình âm sắc
     * @param voiceCode mã hóa giọng nói
     * @return thông tin âm sắc
     */
    VoiceDTO getByVoiceCode(String ttsModelId, String voiceCode);
}