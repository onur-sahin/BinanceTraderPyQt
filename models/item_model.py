from PyQt6.QtCore import QAbstractListModel, Qt, QVariant, QModelIndex

class ItemModel(QAbstractListModel):
    NameRole = Qt.ItemDataRole.UserRole + 1  # Özel bir role ekledik

    def __init__(self, items=None):
        super().__init__()
        self.items = items or []

    def rowCount(self, parent=QModelIndex()):
        return len(self.items)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or index.row() >= len(self.items):
            return QVariant()

        item = self.items[index.row()]

        if role in (Qt.ItemDataRole.DisplayRole, self.NameRole):
            return QVariant(item)

        return QVariant()

    def roleNames(self):
        """ QML tarafında model["name"] ile erişilebilmesi için """
        return {
            self.NameRole: b"name"
        }

    def addItem(self, item):
        """ Yeni bir öğe ekler """
        self.beginInsertRows(QModelIndex(), len(self.items), len(self.items))
        self.items.append(item)
        self.endInsertRows()

    def removeItem(self, row):
        """ Belirtilen satırdaki öğeyi siler """
        if 0 <= row < len(self.items):
            self.beginRemoveRows(QModelIndex(), row, row)
            del self.items[row]
            self.endRemoveRows()
