from PyQt6.QtCore import Qt, QAbstractListModel, QModelIndex, QByteArray, QObject
from PyQt6.QtCore import pyqtSlot, pyqtSignal

class ModelListModelMdl(QAbstractListModel):
    ModelObjRole = Qt.ItemDataRole.UserRole + 1

    def __init__(self, parent=None):
        super().__init__(parent)
        self.m_items = [] # Holds ModelMdl (QObject) instances

    def rowCount(self, parent=QModelIndex()):
        return len(self.m_items)

    def data(self, index, role):
        if not index.isValid() or index.row() >= len(self.m_items):
            return None

        if role == self.ModelNameRole:
            return self.m_items[index.row()]
        else:
            return None

    def roleNames(self):
        return {
            self.ModelObjRole: QByteArray(b"modelObj")
        }

    @pyqtSlot(QObject)
    def addItem(self, item):
        row = len(self.m_items)
        self.beginInsertRows(QModelIndex(), row, row)
        self.m_items.append(item)
        self.endInsertRows()

    @pyqtSlot(str, result=int)
    def findIndexByModelName(self, model_name):
        """Find index of item with given accountName."""
        for idx, item in enumerate(self.m_items):
            if getattr(item, "modelName", None) == model_name:
                return idx
        return -1




