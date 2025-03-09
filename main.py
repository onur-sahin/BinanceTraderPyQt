from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine
from main_controller import MainController
import os

if __name__ == "__main__":

    qml_dir = os.path.join(os.path.dirname(__file__), 'views')  # QML dosyalarının bulunduğu klasör
    os.environ['QT_QML_IMPORT_PATH'] = qml_dir

    app = QGuiApplication([])  # QCoreApplication yerine QGuiApplication KULLANILIYOR

    engine = QQmlApplicationEngine()
    controller = MainController(engine)
    controller.load_qml()

    app.exec()