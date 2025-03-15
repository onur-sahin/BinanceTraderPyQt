from PyQt6.QtCore import QAbstractListModel, Qt, QModelIndex
from PyQt6.QtCore import QVariant
from CryptoManager import CryptoManager
from HashManager import HashManager

class AccountListModelMdl(QAbstractListModel):
    AccountNameRole = Qt.ItemDataRole.UserRole + 1
    ApiKeyRole = Qt.ItemDataRole.UserRole + 2
    ApiSecretRole = Qt.ItemDataRole.UserRole + 3
    RealAccountRole = Qt.ItemDataRole.UserRole + 4
    TestResultRole = Qt.ItemDataRole.UserRole + 5
    AccountPassRole = Qt.ItemDataRole.UserRole + 6
    RememberAccountPassRole = Qt.ItemDataRole.UserRole + 7
    IsLockedRole = Qt.ItemDataRole.UserRole + 8
    CryptedApiKeyRole = Qt.ItemDataRole.UserRole + 9
    CryptedApiSecretRole = Qt.ItemDataRole.UserRole + 10
    AccountNotesRole = Qt.ItemDataRole.UserRole + 11
    AccountTypeStringRole = Qt.ItemDataRole.UserRole + 12

    def __init__(self, parent=None):
        super().__init__(parent)
        self.m_items = []  # This would hold your AccountMdl objects or their equivalent

    def rowCount(self, parent=QModelIndex()):
        return len(self.m_items)

    def data(self, index, role):
        if not index.isValid() or index.row() >= len(self.m_items):
            return QVariant()

        item = self.m_items[index.row()]
        
        if role == self.AccountNameRole:
            return item.account_name
        elif role == self.ApiKeyRole:
            return item.api_key
        elif role == self.ApiSecretRole:
            return item.api_secret
        elif role == self.RealAccountRole:
            return item.real_account
        elif role == self.TestResultRole:
            return item.test_result
        elif role == self.AccountPassRole:
            return item.account_pass
        elif role == self.RememberAccountPassRole:
            return item.remember_account_pass
        elif role == self.IsLockedRole:
            return item.is_locked
        elif role == self.CryptedApiKeyRole:
            return item.crypted_api_key
        elif role == self.CryptedApiSecretRole:
            return item.crypted_api_secret
        elif role == self.AccountNotesRole:
            return item.account_notes
        elif role == self.AccountTypeStringRole:
            return item.account_type_string
        else:
            return QVariant()

    def roleNames(self):
        roles = {
            self.AccountNameRole:          "accountName",
            self.ApiKeyRole:               "apiKey",
            self.ApiSecretRole:            "apiSecret",
            self.RealAccountRole:          "realAccount",
            self.TestResultRole:           "testResult",
            self.AccountPassRole:          "accountPass",
            self.RememberAccountPassRole:  "rememberAccountPass",
            self.IsLockedRole:             "isLocked",
            self.CryptedApiKeyRole:        "cryptedApiKey",
            self.CryptedApiSecretRole:     "cryptedApiSecret",
            self.AccountNotesRole:         "accountNotes",
            self.AccountTypeStringRole:    "accountTypeString"
        }
        return roles

    def addItem(self, item):
        self.beginInsertRows(QModelIndex(), len(self.m_items), len(self.m_items))
        self.m_items.append(item)
        self.endInsertRows()

    def getItem(self, index):
        if index < 0 or index >= len(self.m_items):
            return {}

        item = self.m_items[index]
        account_data = {
            "accountName":          item.account_name,
            "apiKey":               item.api_key,
            "apiSecret":            item.api_secret,
            "realAccount":          item.real_account,
            "testResult":           item.test_result,
            "accountPass":          item.account_pass,
            "rememberAccountPass":  item.remember_account_pass,
            "isLocked":             item.is_locked,
            "cryptedApiKey":        item.crypted_api_key,
            "cryptedApiSecret":     item.crypted_api_secret,
            "accountNotes":         item.account_notes,
            "accountTypeString":    item.account_type_string
        }
        return account_data

    def removeRow(self, row, parent=QModelIndex()):
        if row < 0 or row >= len(self.m_items):
            return False

        item = self.m_items.pop(row)
        self.beginRemoveRows(QModelIndex(), row, row)
        self.endRemoveRows()
        
        # Custom deletion logic, similar to the C++ version
        return True

    def testAccount(self, api_key, api_secret):
        # Simulate a binance API call here, just as in the C++ version
        # response = binance_api_request(api_key, api_secret)

    #     try:
    # # Hesap bilgilerini getirerek API anahtarlarının geçerliliğini kontrol et
    #     account_info = client.get_account()
    #     print("API Key geçerli! Hesap bilgileri alındı.")
    #     except BinanceAPIException as e:
    #         print(f"API Key hatalı veya izinler eksik: {e}")
    #     if "uid" in response:
    #         return "Account is valid"
    #     else:
    #         return response

        return "Account is valid"

    def decryptKeys(self, idx, account_pass):
        item = self.m_items[idx]
        # Use a CryptoManager or similar approach
        crypto_manager = CryptoManager()
        hash_value = HashManager.get_instance().hash(account_pass)
        crypto_manager.loadKey(hash_value, False)
        
        decrypted_api_key = crypto_manager.decrypt(item.crypted_api_key)
        decrypted_api_secret = crypto_manager.decrypt(item.crypted_api_secret)
        
        item.api_key = decrypted_api_key
        item.api_secret = decrypted_api_secret
        item.is_locked = not (decrypted_api_key and decrypted_api_secret)

        self.dataChanged.emit(self.index(idx), self.index(idx), [self.IsLockedRole])

    def save_decryptedKeys(self, idx, account_pass, save_to_json=False):
        self.decryptKeys(idx, account_pass)
        if save_to_json:
            item = self.m_items[idx]
            hashed_text = HashManager.get_instance().hash(account_pass)
            # Assuming CryptoManager handles encryption
            item.saveAccountToJsonFile(item.account_name, hashed_text)
