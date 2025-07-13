from PyQt6.QtCore import QAbstractListModel, Qt, QModelIndex
from PyQt6.QtCore import QVariant, QObject, QByteArray, pyqtSlot
from CryptoManager import CryptoManager
from HashManager import HashManager
from binance.client import Client

from Binance import BinanceDriver

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
            return item.accountName
        elif role == self.ApiKeyRole:
            return item.apiKey
        elif role == self.ApiSecretRole:
            return item.apiSecret
        elif role == self.RealAccountRole:
            return item.realAccount
        elif role == self.TestResultRole:
            return item.testResult
        elif role == self.AccountPassRole:
            return item.accountPass
        elif role == self.RememberAccountPassRole:
            return item.rememberAccountPass
        elif role == self.IsLockedRole:
            return item.isLocked
        elif role == self.CryptedApiKeyRole:
            return item.cryptedApiKey
        elif role == self.CryptedApiSecretRole:
            return item.cryptedApiSecret
        elif role == self.AccountNotesRole:
            return item.accountNotes
        elif role == self.AccountTypeStringRole:
            return item.accountType
        else:
            return QVariant()

    def roleNames(self):
        roles = {
            self.AccountNameRole:          QByteArray(b"accountName"),         
            self.ApiKeyRole:               QByteArray(b"apiKey"),              
            self.ApiSecretRole:            QByteArray(b"apiSecret"),           
            self.RealAccountRole:          QByteArray(b"realAccount"),         
            self.TestResultRole:           QByteArray(b"testResult"),          
            self.AccountPassRole:          QByteArray(b"accountPass"),          
            self.RememberAccountPassRole:  QByteArray(b"rememberAccountPass"), 
            self.IsLockedRole:             QByteArray(b"isLocked"),            
            self.CryptedApiKeyRole:        QByteArray(b"cryptedApiKey"),       
            self.CryptedApiSecretRole:     QByteArray(b"cryptedApiSecret"),    
            self.AccountNotesRole:         QByteArray(b"accountNotes"),        
            self.AccountTypeStringRole:    QByteArray(b"accountTypeString")    
        }
        return roles
    @pyqtSlot(QObject)
    def addItem(self, item):                
        self.beginInsertRows(QModelIndex(), len(self.m_items), len(self.m_items))
        self.m_items.append(item)
        self.endInsertRows()

    @pyqtSlot(int, result=QObject)
    def getItem(self, index):
        if index < 0 or index >= len(self.m_items):
            return {}

        item = self.m_items[index]
        return item

        # account_data = {
        #     "accountName":          item.accountName        ,
        #     "apiKey":               item.apiKey             ,
        #     "apiSecret":            item.apiSecret          ,
        #     "realAccount":          item.realAccount        ,
        #     "testResult":           item.testResult         ,
        #     "accountPass":          item.accountPass        ,
        #     "rememberAccountPass":  item.rememberAccountPass,
        #     "isLocked":             item.isLocked           ,
        #     "cryptedApiKey":        item.cryptedApiKey      ,
        #     "cryptedApiSecret":     item.cryptedApiSecret   ,
        #     "accountNotes":         item.accountNotes       ,
        #     "accountTypeString":    item.accountType  
        # }
        # return account_data

    def removeRow(self, row, parent=QModelIndex()):
        if row < 0 or row >= len(self.m_items):
            return False

        item = self.m_items.pop(row)
        self.beginRemoveRows(QModelIndex(), row, row)
        self.endRemoveRows()
        
        # Custom deletion logic, similar to the C++ version
        return True
    @pyqtSlot(str, str, result=bool)
    def testAccount(self, api_key, api_secret):
        return BinanceDriver.test_binance_credentials(api_key, api_secret)


    @pyqtSlot(int, str)
    def decryptKeys(self, idx, account_pass):
        item = self.m_items[idx]
        # Use a CryptoManager or similar approach
        crypto_manager = CryptoManager()
        hash_value = HashManager.get_instance().hash(account_pass)
        crypto_manager.loadKey(hash_value, False)
        
        decrypted_api_key = crypto_manager.decrypt(item.cryptedApiKey)
        decrypted_api_secret = crypto_manager.decrypt(item.cryptedApiSecret)
        
        item.apiKey    = decrypted_api_key
        item.apiSecret = decrypted_api_secret
        item.isLocked  = not (decrypted_api_key and decrypted_api_secret)

        self.dataChanged.emit(self.index(idx), self.index(idx), [self.IsLockedRole])

    def save_decryptedKeys(self, idx, account_pass, save_to_json=False):
        self.decryptKeys(idx, account_pass)
        if save_to_json:
            item = self.m_items[idx]
            hashed_text = HashManager.get_instance().hash(account_pass)
            # Assuming CryptoManager handles encryption
            item.saveAccountToJsonFile(item.account_name, hashed_text)
