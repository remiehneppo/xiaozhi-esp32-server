import jwt
import time
import json
import os
from datetime import datetime, timedelta, timezone
from typing import Tuple, Optional
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import base64


class AuthToken:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key.encode()  # chuyển đổicho
        # mã hóa (32 for AES-256)
        self.encryption_key = self._derive_key(32)

    def _derive_key(self, length: int) -> bytes:
        """"""
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

        # làm chosử dụng（làm chosử dụng）
        salt = b"fixed_salt_placeholder"  # chotạo
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=length,
            salt=salt,
            iterations=100000,
            backend=default_backend(),
        )
        return kdf.derive(self.secret_key)

    def _encrypt_payload(self, payload: dict) -> str:
        """làm chosử dụngAES-GCMmã hóapayload"""
        # sẽpayloadchuyển đổichoJSONký tự
        payload_json = json.dumps(payload)

        # tạoIV
        iv = os.urandom(12)
        # tạomã hóa
        cipher = Cipher(
            algorithms.AES(self.encryption_key),
            modes.GCM(iv),
            backend=default_backend(),
        )
        encryptor = cipher.encryptor()

        # mã hóavàtạo
        ciphertext = encryptor.update(payload_json.encode()) + encryptor.finalize()
        tag = encryptor.tag

        #  IV +  + 
        encrypted_data = iv + ciphertext + tag
        return base64.urlsafe_b64encode(encrypted_data).decode()

    def _decrypt_payload(self, encrypted_data: str) -> dict:
        """giải mãAES-GCMmã hóapayload"""
        # giải mãBase64
        data = base64.urlsafe_b64decode(encrypted_data.encode())
        # 
        iv = data[:12]
        tag = data[-16:]
        ciphertext = data[12:-16]

        # tạogiải mã
        cipher = Cipher(
            algorithms.AES(self.encryption_key),
            modes.GCM(iv, tag),
            backend=default_backend(),
        )
        decryptor = cipher.decryptor()

        # giải mã
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        return json.loads(plaintext.decode())

    def generate_token(self, device_id: str) -> str:
        """
        tạoJWT token
        :param device_id: ID
        :return: JWT tokenký tự
        """
        # đặtquathời giancho1thờisau
        expire_time = datetime.now(timezone.utc) + timedelta(hours=1)

        # tạoban đầupayload
        payload = {"device_id": device_id, "exp": expire_time.timestamp()}

        # mã hóapayload
        encrypted_payload = self._encrypt_payload(payload)

        # tạongoàipayload，mã hóadữ liệu
        outer_payload = {"data": encrypted_payload}

        # làm chosử dụngJWTtiến hànhmã hóa
        token = jwt.encode(outer_payload, self.secret_key, algorithm="HS256")
        return token

    def verify_token(self, token: str) -> Tuple[bool, Optional[str]]:
        """
        xác thựctoken
        :param token: JWT tokenký tự
        :return: (cóhiệu quả, ID)
        """
        try:
            # xác thựcngoàiJWT（chữ kývàquathời gian）
            outer_payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])

            # giải mãtrongpayload
            inner_payload = self._decrypt_payload(outer_payload["data"])

            # lầnkiểm traquathời gian（xác thực）
            if inner_payload["exp"] < time.time():
                return False, None

            return True, inner_payload["device_id"]

        except jwt.InvalidTokenError:
            return False, None
        except json.JSONDecodeError:
            return False, None
        except Exception as e:  # nócó thểlỗi
            print(f"Token verification failed: {str(e)}")
            return False, None
