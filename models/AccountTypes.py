from enum import Enum
from PyQt6.QtCore import QObject, pyqtProperty, pyqtSlot


class AccountType(Enum):
    BINANCE = 0
    CM_FUTURE = 1
    UM_FUTURE = 2


class AccountTypes(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

    # Enum sabitlerini QML'e expose et
    @pyqtProperty(int, constant=True)
    def BINANCE(self): return AccountType.BINANCE.value

    @pyqtProperty(int, constant=True)
    def CM_FUTURE(self): return AccountType.CM_FUTURE.value

    @pyqtProperty(int, constant=True)
    def UM_FUTURE(self): return AccountType.UM_FUTURE.value

    # Enum int -> string
    @pyqtSlot(int, result=str)
    def to_string(self, value: int) -> str:
        try:
            return AccountType(value).name
        except ValueError:
            return "UNKNOWN"

    # Enum string -> int
    @pyqtSlot(str, result=int)
    def from_string(self, name: str) -> int:
        try:
            return AccountType[name].value
        except KeyError:
            return AccountType.BINANCE.value  # default

    # Enum tüm değerleri string liste olarak al
    @pyqtSlot(result="QVariantList")
    def all_values(self):
        return [e.name for e in AccountType]
