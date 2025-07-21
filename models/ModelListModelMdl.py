from PyQt6.QtCore import Qt, QAbstractListModel, QModelIndex, QByteArray, QObject
from PyQt6.QtCore import pyqtSlot, pyqtSignal, qCritical

from returns.result import Failure

from ModelMdl import ModelMdl
from DBManager import DBManager

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

        if role == self.ModelObjRole:
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
    def findIndexByModelName(self, model_name):
        """Find index of item with given accountName."""
        for idx, item in enumerate(self.m_items):
            if getattr(item, "modelName", None) == model_name:
                return idx
        return -1
    

    @pyqtSlot()
    def loadFromDatabaseRequested(self):

        db = DBManager.get_instance()
        query = "SELECT * FROM tbl_models"
        result = db.execute_select_return_dict(query)
        if isinstance(result, Failure):
            qCritical(f"Failed to load models from database: {str( result.failure() )}")
            return

        model_list = result.unwrap()

        for model in model_list:
            model_name = model.get("model_name")
            

            if self.findIndexByModelName(model_name) != -1:
                continue


            new_account = ModelMdl.create_modelMdl_from_data(model)

            self.addItem(new_account)
            # self.newAccountCreated.emit(new_account)




