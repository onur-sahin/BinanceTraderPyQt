from PyQt6.QtCore import QObject, Qt
from PyQt6.QtCore import pyqtProperty, pyqtSlot, pyqtSignal


class InfoMdl(QObject):

    addPullDataProgressBar = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    @pyqtSlot()
    def emit_addPullDataProgressBar(self):
        self.addPullDataProgressBar.emit()


    @pyqtSlot(QObject)
    def deneme(self, item):
        mdl = item.findChild(QObject, "pullDataMdl", Qt.FindChildOption.FindChildrenRecursively)
        print("mmmm")
        self.find_pullDataMdl(item)
        # print(item.children()[0].children())
        # print(item.children()[1].children())


    @pyqtSlot(QObject)
    def find_pullDataMdl(self, item:QObject):
        
        for i in item.children():
            j = self.find_pullDataMdl(i)

            if j == None:
                print(i.property("objectName"))



