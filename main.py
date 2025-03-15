from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine
from RootCoord   import RootCoord
from PyQt6.QtCore import qInfo, qDebug, qWarning, QIODevice, QFile
from pathlib import Path
import sys


from PyQt6.QtCore import QUrl
from PyQt6.QtQuick import QQuickView

from LogManager import LogManager

import os, sys

if __name__ == "__main__":

    current_path = Path.cwd()
    qInfo(f"current path: {current_path}".encode('utf-8'))

    LogManager.instance()

    qml_dir = os.path.join(os.path.dirname(__file__), 'qml')  # QML dosyalarının bulunduğu klasör
    os.environ['QT_QML_IMPORT_PATH'] = qml_dir

    app        = QGuiApplication([])  # QCoreApplication yerine QGuiApplication KULLANILIYOR
    engine     = QQmlApplicationEngine()
    controller = RootCoord(engine)
    controller.load_qml()

    app.exec()