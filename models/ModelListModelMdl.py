from PyQt6.QtCore import Qt, QAbstractListModel, QModelIndex, QByteArray
from PyQt6.QtCore import pyqtSlot, pyqtSignal

class ModelListModelMdl(QAbstractListModel):
    ModelNameRole = Qt.ItemDataRole.UserRole + 1
    # ApiKeyRole = Qt.ItemDataRole.UserRole + 2
    # ApiSecretRole = Qt.ItemDataRole.UserRole + 3
    # RealAccountRole = Qt.ItemDataRole.UserRole + 4
    # TestResultRole = Qt.ItemDataRole.UserRole + 5
    # AccountPassRole = Qt.ItemDataRole.UserRole + 6
    # RememberAccountPassRole = Qt.ItemDataRole.UserRole + 7
    # IsLockedRole = Qt.ItemDataRole.UserRole + 8
    # CryptedApiKeyRole = Qt.ItemDataRole.UserRole + 9
    # CryptedApiSecretRole = Qt.ItemDataRole.UserRole + 10
    # AccountNotesRole = Qt.ItemDataRole.UserRole + 11
    # AccountTypeStringRole = Qt.ItemDataRole.UserRole + 12

    def __init__(self, parent=None):
        super().__init__(parent)
        self.m_items = []

    def rowCount(self, parent=QModelIndex()):
        return len(self.m_items)

    def data(self, index, role):
        if not index.isValid() or index.row() >= len(self.m_items):
            return None

        item = self.m_items[index.row()]

        if role == self.ModelNameRole:
            return item.getModelName()
        # elif role == self.ApiKeyRole:
        #     return item.getApiKey()
        # elif role == self.ApiSecretRole:
        #     return item.getApiSecret()
        # elif role == self.RealAccountRole:
        #     return item.getRealAccount()
        # elif role == self.TestResultRole:
        #     return item.getTestResult()
        # elif role == self.AccountPassRole:
        #     return item.getAccountPass()
        # elif role == self.RememberAccountPassRole:
        #     return item.getRememberAccountPass()
        # elif role == self.IsLockedRole:
        #     return item.getIsLocked()
        # elif role == self.CryptedApiKeyRole:
        #     return item.getCryptedApiKey()
        # elif role == self.CryptedApiSecretRole:
        #     return item.getCryptedApiSecret()
        # elif role == self.AccountNotesRole:
        #     return item.getAccountNotes()
        # elif role == self.AccountTypeStringRole:
        #     return item.getAccountTypeString()
        else:
            return None

def roleNames(self):
    return {
        self.ModelNameRole: QByteArray(b"modelName"),
        self.ApiKeyRole: QByteArray(b"apiKey"),
        self.ApiSecretRole: QByteArray(b"apiSecret"),
        self.RealAccountRole: QByteArray(b"realAccount"),
        self.TestResultRole: QByteArray(b"testResult"),
        self.AccountPassRole: QByteArray(b"accountPass"),
        self.RememberAccountPassRole: QByteArray(b"rememberAccountPass"),
        self.IsLockedRole: QByteArray(b"isLocked"),
        self.CryptedApiKeyRole: QByteArray(b"cryptedApiKey"),
        self.CryptedApiSecretRole: QByteArray(b"cryptedApiSecret"),
        self.AccountNotesRole: QByteArray(b"accountNotes"),
        self.AccountTypeStringRole: QByteArray(b"accountTypeString"),
    }

    @pyqtSlot()
    def addItem(self, item):
        row = len(self.m_items)
        self.beginInsertRows(QModelIndex(), row, row)
        self.m_items.append(item)
        self.endInsertRows()

    @pyqtSlot()
    def removeRow(self, row, parent=QModelIndex()):
        if row < 0 or row >= len(self.m_items):
            return False
        self.beginRemoveRows(QModelIndex(), row, row)
        self.m_items.pop(row)
        self.endRemoveRows()
        return True
