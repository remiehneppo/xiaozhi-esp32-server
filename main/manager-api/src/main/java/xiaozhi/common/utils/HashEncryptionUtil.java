package xiaozhi.common.utils;

import lombok.extern.slf4j.Slf4j;

import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

/**
 * Lớp công cụ thuật toán mã hóa băm
 * @author zjy
 */
@Slf4j
public class HashEncryptionUtil {
    /**
     * Mã hóa bằng md5
     * @param bối cảnh nội dung được mã hóa
     * @return giá trị băm
     */
    public static String Md5hexDigest(String context){
        return hexDigest(context,"MD5");
    }

    /**
     * Chỉ định thuật toán băm để mã hóa
     * @param bối cảnh nội dung được mã hóa
     * Thuật toán băm @param
     * @return giá trị băm
     */
   public static String hexDigest(String context,String algorithm ){
       // Nhận phiên bản thuật toán MD5
       MessageDigest md = null;
       try {
           md = MessageDigest.getInstance(algorithm);
       } catch (NoSuchAlgorithmException e) {
           log.error("Thuật toán mã hóa không thành công：{}",algorithm);
           throw new RuntimeException("Mã hóa không thành công，"+ algorithm +"Hệ thống thuật toán băm không hỗ trợ");
       }
       // Tính giá trị MD5 của id tác nhân
       byte[] messageDigest = md.digest(context.getBytes());
       // Chuyển đổi mảng byte thành chuỗi hex
       StringBuilder hexString = new StringBuilder();
       for (byte b : messageDigest) {
           String hex = Integer.toHexString(0xFF & b);
           if (hex.length() == 1) {
               hexString.append('0');
           }
           hexString.append(hex);
       }
       return hexString.toString();
   }

}
