from PyQt6.QtCore import QCoreApplication
from PyQt6.QtQml import QQmlApplicationEngine
from item_model import ItemModel

class MainController:
    def __init__(self, engine: QQmlApplicationEngine):
        self.engine = engine
        self.model = ItemModel(["Item 1", "Item 2", "Item 3"])

    def load_qml(self):
        context = self.engine.rootContext()
        context.setContextProperty("itemModel", self.model)
        self.engine.load('views/main.qml')

if __name__ == "__main__":
    app = QCoreApplication([])
    engine = QQmlApplicationEngine()
    
    controller = MainController(engine)
    controller.load_qml()
    
    app.exec()
