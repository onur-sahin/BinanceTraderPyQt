

from PyQt6.QtCore import (
    QAbstractListModel, Qt, QModelIndex, QObject, QByteArray, pyqtSlot,
    qCritical
)

import os, json

from returns.result import Failure

from DBManager import DBManager
from AccountMdl import AccountMdl


class AccountListModelMdl(QAbstractListModel):

    AccountObjRole = Qt.ItemDataRole.UserRole + 1

    def __init__(self, parent=None):
        super().__init__(parent)
        self.m_items       = []  # Holds AccountMdl (QObject) instances
        self.selectedIndex = -1

    # Required by QAbstractListModel
    def rowCount(self, parent=QModelIndex()):
        return len(self.m_items)

    def data(self, index, role):
        if not index.isValid() or index.row() >= len(self.m_items):
            return None

        if role == self.AccountObjRole:
            return self.m_items[index.row()]
        return None

    def roleNames(self):

        return {
            self.AccountObjRole: QByteArray(b"accountObj")
        }

    # --- Public Slots for QML ---
    @pyqtSlot(QObject)
    def addItem(self, item):
        """Add new AccountMdl object to the model."""
        self.beginInsertRows(QModelIndex(), len(self.m_items), len(self.m_items))
        self.m_items.append(item)
        self.endInsertRows()

    @pyqtSlot(int, result=QObject)
    def getItem(self, index):
        """Return item by index."""
        if 0 <= index < len(self.m_items):
            return self.m_items[index]
        return None

    @pyqtSlot(int, result=bool)
    def removeRow(self, row, parent=QModelIndex()):
        """Remove item by index."""
        if 0 <= row < len(self.m_items):
            self.beginRemoveRows(QModelIndex(), row, row)
            self.m_items.pop(row)
            self.endRemoveRows()
            return True
        return False

    @pyqtSlot(str, result=int)
    def findIndexByAccountName(self, account_name):
        """Find index of item with given accountName."""
        for idx, item in enumerate(self.m_items):
            if getattr(item, "accountName", None) == account_name:
                return idx
        return -1


    @staticmethod
    def get_account_keys_from_json():
        users_path = os.path.join(os.getcwd(), "share", "users.json")

        if not os.path.exists(users_path)  :
            return []

        try:
            with open(users_path, "r") as file:
                data = json.load(file)
                return data
        except Exception as e:
            print(f"Failed to read users.json: {e}")
            return []

    @pyqtSlot()
    def loadFromDatabaseRequested(self):

        db = DBManager.get_instance()
        query = "SELECT * FROM tbl_accounts"
        result = db.execute_select_return_dict(query)
        if isinstance(result, Failure):
            qCritical(f"Failed to load accounts from database: {str( result.failure() )}")
            return

        accounts_list = result.unwrap()
        account_key_list = self.get_account_keys_from_json()

        for account in accounts_list:
            account_name = account.get("account_name")
            

            if self.findIndexByAccountName(account_name) != -1:
                continue


            new_account = AccountMdl.create_accountMdl_from_data(account)

            for accountDataFromJSON in account_key_list:
                if accountDataFromJSON.get("accountName") == account_name:
                    new_account._cryptedHashedAccountPass = accountDataFromJSON.get("accountPass")

                    new_account.decrypt_cryptedHashedAccountPass()
                    new_account.decryptKeys()

                    break 

            self.addItem(new_account)
            # self.newAccountCreated.emit(new_account)


















# from PyQt6.QtCore import QAbstractListModel, Qt, QModelIndex
# from PyQt6.QtCore import QVariant, QObject, QByteArray, pyqtSlot
# from CryptoManager import CryptoManager
# from HashManager import HashManager
# from binance.client import Client

# from Binance import BinanceDriver

# class AccountListModelMdl(QAbstractListModel):
#     AccountObjRole          = Qt.ItemDataRole.UserRole +  1
#     AccountNameRole         = Qt.ItemDataRole.UserRole +  2
#     ApiKeyRole              = Qt.ItemDataRole.UserRole +  3
#     ApiSecretRole           = Qt.ItemDataRole.UserRole +  4
#     RealAccountRole         = Qt.ItemDataRole.UserRole +  5
#     TestResultRole          = Qt.ItemDataRole.UserRole +  6
#     AccountPassRole         = Qt.ItemDataRole.UserRole +  7
#     RememberAccountPassRole = Qt.ItemDataRole.UserRole +  8
#     IsLockedRole            = Qt.ItemDataRole.UserRole +  9
#     CryptedApiKeyRole       = Qt.ItemDataRole.UserRole + 10
#     CryptedApiSecretRole    = Qt.ItemDataRole.UserRole + 11
#     AccountNotesRole        = Qt.ItemDataRole.UserRole + 12
#     AccountTypeStringRole   = Qt.ItemDataRole.UserRole + 13

#     m_items = []  # This would hold your AccountMdl objects or their equivalent

    

#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.m_items = AccountListModelMdl.m_items

        

#     def rowCount(self, parent=QModelIndex()):
#         return len(self.m_items)

#     def data(self, index, role):
#         if not index.isValid() or index.row() >= len(self.m_items):
#             return QVariant()

#         item = self.m_items[index.row()]

#         if   role == self.AccountObjRole:
#             return item
#         elif role == self.AccountNameRole:
#             return item.accountName
#         elif role == self.ApiKeyRole:
#             return item.apiKey
#         elif role == self.ApiSecretRole:
#             return item.apiSecret
#         elif role == self.RealAccountRole:
#             return item.realAccount
#         elif role == self.TestResultRole:
#             return item.testResult
#         elif role == self.AccountPassRole:
#             return item.accountPass
#         elif role == self.RememberAccountPassRole:
#             return item.rememberAccountPass
#         elif role == self.IsLockedRole:
#             return item.isLocked
#         elif role == self.CryptedApiKeyRole:
#             return item.cryptedApiKey
#         elif role == self.CryptedApiSecretRole:
#             return item.cryptedApiSecret
#         elif role == self.AccountNotesRole:
#             return item.accountNotes
#         elif role == self.AccountTypeStringRole:
#             return item.accountType
#         else:
#             return QVariant()

#     def roleNames(self):
#         roles = {
#             self.AccountObjRole:           QByteArray(b"accountObj"),
#             self.AccountNameRole:          QByteArray(b"accountName"),         
#             self.ApiKeyRole:               QByteArray(b"apiKey"),              
#             self.ApiSecretRole:            QByteArray(b"apiSecret"),           
#             self.RealAccountRole:          QByteArray(b"realAccount"),         
#             self.TestResultRole:           QByteArray(b"testResult"),          
#             self.AccountPassRole:          QByteArray(b"accountPass"),         
#             self.RememberAccountPassRole:  QByteArray(b"rememberAccountPass"), 
#             self.IsLockedRole:             QByteArray(b"isLocked"),            
#             self.CryptedApiKeyRole:        QByteArray(b"cryptedApiKey"),       
#             self.CryptedApiSecretRole:     QByteArray(b"cryptedApiSecret"),    
#             self.AccountNotesRole:         QByteArray(b"accountNotes"),        
#             self.AccountTypeStringRole:    QByteArray(b"accountTypeString")    
#         }
#         return roles
#     @pyqtSlot(QObject)
#     def addItem(self, item):                
#         self.beginInsertRows(QModelIndex(), len(self.m_items), len(self.m_items))
#         self.m_items.append(item)
#         self.endInsertRows()

#     @pyqtSlot(int, result=QObject)
#     def getItem(self, index):
#         if index < 0 or index >= len(self.m_items):
#             return {}

#         item = self.m_items[index]
#         return item

#     @classmethod
#     @pyqtSlot(str, result=int)
#     def findIndexByAccountName(cls, account_name: str) -> int:
#         """
#         Verilen account_name'e sahip item'ın index'ini döndürür.
#         Yoksa -1 döndürür.
#         """
#         for idx, item in enumerate(cls.m_items):
#             if getattr(item, "accountName", None) == account_name:
#                 return idx
#         return -1

#     @pyqtSlot(int)
#     def removeRow(self, row:int, parent=QModelIndex()):

#         if row < 0 or row >= len(self.m_items):
#             return False

#         item = self.m_items.pop(row)
#         self.beginRemoveRows(QModelIndex(), row, row)
#         self.endRemoveRows()
        
#         # Custom deletion logic, similar to the C++ version
#         return True

