from PyQt6.QtCore import QByteArray, QIODevice, QFile, QStringConverter, QLoggingCategory
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import base64

log = QLoggingCategory("CryptoManager")

class CryptoManager:
    def __init__(self):
        self.m_key = None
        self.m_iv = None

    def loadKey(self, keySource: str, fromFile: bool):
        if fromFile:
            self.loadKeyFromFile(keySource)
        else:
            self.loadKeyFromString(keySource)

    def loadKeyFromFile(self, keyFile: str):
        file = QFile(keyFile)
        if not file.open(QIODevice.ReadOnly):
            log.warning("Could not open key file.")
            return

        keyData = file.readAll()
        if len(keyData) < 48:
            log.warning("Key file must contain at least 48 bytes (32-byte key + 16-byte IV).")
            return

        self.m_key = keyData[:32]
        self.m_iv = keyData[32:48]

    def loadKeyFromString(self, keyString: str):
        try:
            keyData = base64.b64decode(keyString.encode('utf-8'))
            if len(keyData) < 48:
                log.warning("Key string must contain at least 48 bytes (32-byte key + 16-byte IV).")
                return

            self.m_key = keyData[:32]
            self.m_iv = keyData[32:48]
        except Exception as e:
            log.warning(f"Failed to decode key string: {e}")

    def encrypt(self, plaintext: str) -> str:
        if self.m_key is None or self.m_iv is None:
            log.warning("Encryption key and IV not set.")
            return ""

        try:
            cipher = Cipher(algorithms.AES(self.m_key), modes.CBC(self.m_iv), backend=default_backend())
            encryptor = cipher.encryptor()

            inputData = plaintext.encode('utf-8')
            padder = padding.PKCS7(128).padder()
            padded_data = padder.update(inputData) + padder.finalize()

            ciphertext = encryptor.update(padded_data) + encryptor.finalize()
            return base64.b64encode(ciphertext).decode('utf-8')
        except Exception as e:
            log.warning(f"Encryption failed: {e}")
            return ""

    def decrypt(self, ciphertext: str) -> str:
        if self.m_key is None or self.m_iv is None:
            log.warning("Decryption key and IV not set.")
            return ""

        try:
            cipher = Cipher(algorithms.AES(self.m_key), modes.CBC(self.m_iv), backend=default_backend())
            decryptor = cipher.decryptor()

            encryptedData = base64.b64decode(ciphertext.encode('utf-8'))
            decryptedData = decryptor.update(encryptedData) + decryptor.finalize()

            unpadder = padding.PKCS7(128).unpadder()
            unpadded_data = unpadder.update(decryptedData) + unpadder.finalize()

            return unpadded_data.decode('utf-8')
        except Exception as e:
            log.warning(f"Decryption failed: {e}")
            return ""
