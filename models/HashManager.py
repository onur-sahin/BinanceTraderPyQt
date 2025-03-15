from PyQt6.QtCore import QByteArray, QCryptographicHash
from PyQt6.QtCore import QJsonDocument
from PyQt6.QtCore import QFile, QTextStream
import json

class HashManager:
    _instance = None  # Singleton instance

    @staticmethod
    def get_instance():
        """HashManager'ın tekil örneğini döndürür."""
        if HashManager._instance is None:
            HashManager._instance = HashManager()
        return HashManager._instance

    def hash(self, input_str: str) -> str:
        """Verilen girdiyi SHA-256 ile hashler ve hex olarak döndürür."""
        prefix = "ZxkoFEWp24LUi1wRo9V7U9Wxlpb1fj3bRLsvj80OD7nxN9YhHS4Ap7z4LthwTld8"
        byte_array = QByteArray((prefix + input_str).encode('utf-8'))
        
        # SHA-256 hash işlemi
        hash_result = QCryptographicHash.hash(byte_array, QCryptographicHash.Algorithm.Sha256)
        
        return hash_result.toHex().data().decode('utf-8')

    def save_hash_to_json_file(self, file_path: str, account_name: str, hash_value: str):
        """Hash değerini belirtilen dosyaya JSON formatında kaydeder."""
        data = {account_name: hash_value}

        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)
            print(f"Hash kaydedildi: {file_path}")
        except Exception as e:
            print(f"Hata: {e}")

# Kullanım örneği:
if __name__ == "__main__":
    manager = HashManager.get_instance()
    hashed_value = manager.hash("my_secure_password")
    print("Hashed:", hashed_value)
    manager.save_hash_to_json_file("hashes.json", "user1", hashed_value)
