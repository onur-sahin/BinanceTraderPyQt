from PyQt6.QtCore import QAbstractListModel, Qt, QModelIndex, QVariant


class PairListMdl(QAbstractListModel):

    ModelObjRole = Qt.ItemDataRole.UserRole + 1

    def __init__(self, parent=None, pairs=None):
        super().__init__(parent)

        self._pairs = pairs or []


    def data(self, index, role=Qt.ItemDataRole.DisplayRole):

        if role == Qt.ItemDataRole.DisplayRole and index.isValid():
            return self._pairs[index.row()]
        
        elif role == self.ModelObjRole:
            return QVariant()


        return QVariant()
    
    def rowCount(self, parent=QModelIndex()):
        return len(self._pairs)
    

    def roleNames(self):
        return  {
                Qt.ItemDataRole.DisplayRole: b"text",
                self.ModelObjRole          : b"modelObj"
                }
    

    def updatePairs(self, new_pairs):
        self.beginResetModel()
        self._pairs = new_pairs
        self.endResetModel()


    def addPair(self, pair:str):
        self.beginInsertRows(QModelIndex(), len(self._pairs), len(self._pairs))
        self._pairs.append(pair)
        self.endInsertRows()


    def removePair(self, index:int):
        if 0 <= index < len(self._pairs):
            self.beginRemoveRows(QModelIndex(), index, index)
            del self._pairs[index]
            self.endRemoveRows()


