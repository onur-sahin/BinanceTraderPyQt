from PyQt6.QtCore import QObject, QDateTime, QFile, QIODevice, QTextStream, QTimeZone, qInstallMessageHandler, QtMsgType
from PyQt6.QtCore import qInfo, qDebug, qWarning
from pathlib import Path
import sys

class LogManager(QObject):
    _instance = None  # Singleton instance

    def __init__(self):
        super().__init__()

        current_path = Path.cwd()
        log_file_path = current_path / "share" / "logs.log"
        log_file_path_qstr = str(log_file_path)
        qInfo(f"log file path: {log_file_path}".encode('utf-8'))


        self.log_file = QFile(log_file_path_qstr)

        if self.log_file.open(QIODevice.OpenModeFlag.Append | QIODevice.OpenModeFlag.Text):
            qDebug(f"Yeni log dosyası oluşturuldu: {log_file_path_qstr}".encode('utf-8'))
            # self.log_file.close()
        else:
            qWarning(f"Log dosyası oluşturulamadı: {self.log_file.errorString()}".encode('utf-8'))


        qInstallMessageHandler(self.message_handler)

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = LogManager()
        return cls._instance

    @staticmethod
    def message_handler(mode: QtMsgType, context, message: str):
        instance = LogManager.instance()
        out = QTextStream(instance.log_file)

        log_levels = {
            QtMsgType.QtDebugMsg:    "Debug",
            QtMsgType.QtInfoMsg:     "Info",
            QtMsgType.QtWarningMsg:  "Warning",
            QtMsgType.QtCriticalMsg: "Critical",
            QtMsgType.QtFatalMsg:    "Fatal",
        }
        
        level = log_levels.get(mode, "Unknown").ljust(8)

        # Zaman dilimi İstanbul olarak ayarlanıyor
        time_zone = QTimeZone(b"Europe/Istanbul")
        datetime_string = QDateTime.currentDateTimeUtc().toTimeZone(time_zone).toString("HH:mm:ss dd-MM-yyyy")

        context_info = ""
        if context.file:
            if mode in (QtMsgType.QtCriticalMsg, QtMsgType.QtFatalMsg):
                context_info = f"({context.file}:{context.line}, {context.function})"
            else:
                context_info = f"({context.file})"

        formatted_message = f"[{datetime_string}] [{level}] {message} {context_info}"

        # Log'u konsola yazdır
        print(formatted_message, file=sys.stderr)

        # Log'u dosyaya yazdır
        out << formatted_message << "\n"
        out.flush()

        # Eğer bir log modeli varsa, yeni mesajı modele ekleyebiliriz
        if hasattr(instance, "log_model") and instance.log_model:
            instance.log_model.addItem(formatted_message)

    def set_log_model(self, log_model):
        """QML veya başka yerlerden log kayıtlarını görüntülemek için bir model atanabilir."""
        self.log_model = log_model
