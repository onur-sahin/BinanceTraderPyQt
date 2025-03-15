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

    log_file_path = current_path / "share" / "logs.log"
    log_file_path_qstr = str(log_file_path)
    qInfo(f"log file path: {log_file_path}".encode('utf-8'))

    if not log_file_path.exists():
        new_log_file = QFile(log_file_path_qstr)

        if new_log_file.open(QIODevice.OpenModeFlag.WriteOnly):
            qDebug(f"Yeni log dosyası oluşturuldu: {log_file_path_qstr}".encode('utf-8'))
            new_log_file.close()
        else:
            qWarning(f"Log dosyası oluşturulamadı: {new_log_file.errorString()}".encode('utf-8'))

    LogManager()

    qml_dir = os.path.join(os.path.dirname(__file__), 'qml')  # QML dosyalarının bulunduğu klasör
    os.environ['QT_QML_IMPORT_PATH'] = qml_dir

    app        = QGuiApplication([])  # QCoreApplication yerine QGuiApplication KULLANILIYOR
    engine     = QQmlApplicationEngine()
    controller = RootCoord(engine)
    controller.load_qml()

    app.exec()