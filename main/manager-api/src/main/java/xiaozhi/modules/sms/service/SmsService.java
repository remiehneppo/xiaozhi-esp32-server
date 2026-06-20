package xiaozhi.modules.sms.service;

/**
 * Giao diện định nghĩa phương thức dịch vụ SMS
 *
 * @author zjy
 * @since 2025-05-12
 */
public interface SmsService {

    /**
     * Gửi SMS mã xác minh
     * @param số điện thoại di động
     * @param Mã xác minh Mã xác minh
     */
    void sendVerificationCodeSms(String phone, String VerificationCode) ;
}
