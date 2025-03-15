from PyQt6.QtCore import QAbstractListModel, Qt, QVariant, QModelIndex, QStringListModel

class LogListModelMdl(QAbstractListModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.m_logList = []  # QStringList yerine Python listesi kullanıyoruz

    def rowCount(self, parent=QModelIndex()):
        return len(self.m_logList)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or index.row() >= len(self.m_logList):
            return QVariant()

        if role == Qt.ItemDataRole.DisplayRole:  # DisplayRole kontrolü
            return self.m_logList[index.row()]

        return QVariant()

    def addItem(self, item: str):
        self.beginInsertRows(QModelIndex(), len(self.m_logList), len(self.m_logList))
        self.m_logList.append(item)
        self.endInsertRows()

    def roleNames(self):
        return {Qt.ItemDataRole.DisplayRole: b"logText"}  # Qt::DisplayRole'a karşılık gelen tanım

