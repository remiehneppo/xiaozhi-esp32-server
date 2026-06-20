package xiaozhi.common.utils;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Test;

public class AESUtilsTest {

    @Test
    public void testEncryptAndDecrypt() {
        String key = "xiaozhi1234567890";
        String plainText = "Hello, Tiểu Trí!";

        System.out.println("Văn bản gốc: " + plainText);
        System.out.println("Khóa: " + key);

        // Mã hóa
        String encrypted = AESUtils.encrypt(key, plainText);
        System.out.println("Kết quả mã hóa: " + encrypted);

        // Giải mã
        String decrypted = AESUtils.decrypt(key, encrypted);
        System.out.println("Kết quả giải mã: " + decrypted);

        // Xác thực
        assertEquals(plainText, decrypted, "Kết quả mã hóa và giải mã phải khớp nhau");
        System.out.println("Tính nhất quán của mã hóa/giải mã: " + plainText.equals(decrypted));
    }

    @Test
    public void testDifferentKeyLengths() {
        String[] keys = {
                "1234567890123456", // 16 ký tự
                "123456789012345678901234", // 24 ký tự
                "12345678901234567890123456789012", // 32 ký tự
                "short", // Khóa ngắn
                "verylongkeythatwillbetruncatedto32bytes" // Khóa dài
        };

        String plainText = "Văn bản thử nghiệm";

        for (String key : keys) {
            String encrypted = AESUtils.encrypt(key, plainText);
            String decrypted = AESUtils.decrypt(key, encrypted);
            assertEquals(plainText, decrypted, "Độ dài khóa: " + key.length());
        }
    }

    @Test
    public void testSpecialCharacters() {
        String key = "xiaozhi1234567890";
        String[] testTexts = {
                "Hello World",
                "Chào thế giới",
                "Hello, Tiểu Trí!",
                "Ký tự đặc biệt: !@#$%^&*()",
                "Số 123 và chữ Trung Quốc hỗn hợp",
                "Emoji: 😀🎉🚀",
                "Thử nghiệm chuỗi trống",
                ""
        };

        for (String text : testTexts) {
            String encrypted = AESUtils.encrypt(key, text);
            String decrypted = AESUtils.decrypt(key, encrypted);
            assertEquals(text, decrypted, "Văn bản thử nghiệm: " + text);
        }
    }

    @Test
    public void testCrossLanguageCompatibility() {
        // Đây là kết quả mã hóa được tạo bởi phiên bản Python, dùng để kiểm tra tính tương thích đa ngôn ngữ
        String key = "xiaozhi1234567890";
        String plainText = "Hello, Tiểu Trí!";

        // Kết quả mã hóa được tạo bởi phiên bản Python (cần chạy thử nghiệm Python để lấy)
        // String pythonEncrypted = "Kết quả mã hóa lấy từ thử nghiệm Python";
        // String decrypted = AESUtils.decrypt(key, pythonEncrypted);
        // assertEquals(plainText, decrypted, "Java nên có thể giải mã kết quả mã hóa của Python");

        // Tạo kết quả mã hóa Java để thử nghiệm Python
        String javaEncrypted = AESUtils.encrypt(key, plainText);
        System.out.println("Kết quả mã hóa Java để thử nghiệm Python: " + javaEncrypted);
    }
}