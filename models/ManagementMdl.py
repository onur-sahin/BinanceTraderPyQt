
from PyQt6.QtCore import QObject, Qt, QDateTime, QTimeZone
from PyQt6.QtCore import pyqtSignal, pyqtProperty, pyqtSlot

class ManagementMdl(QObject):

    # Signals
    pairChanged              = pyqtSignal()
    pairIndexChanged         = pyqtSignal()
    trainStartChanged        = pyqtSignal()
    trainEndChanged          = pyqtSignal()
    epochChanged             = pyqtSignal()
    intervalChanged          = pyqtSignal()
    testSpeedChanged         = pyqtSignal()
    maxChartCountChanged     = pyqtSignal()
    testStartChanged         = pyqtSignal()
    testEndChanged           = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self._pair               : str       = ""
        self._pairIndex          : int       = -1
        self._pairList           : list      = []
        self._epoch              : int       = 0
        self._interval           : str       = ""
        self._dt_trainStart      : QDateTime = QDateTime.fromString("2022-06-06T12:00:00+03:00", Qt.DateFormat.ISODate)
        self._dt_trainEnd        : QDateTime = QDateTime.fromString("2022-06-06T13:00:00+03:00", Qt.DateFormat.ISODate)
        self._trainStartDate     : str       = self._dt_trainStart.date().toString("dd/MM/yyyy")
        self._trainEndDate       : str       = self._dt_trainEnd  .date().toString("dd/MM/yyyy")
        self._trainStartTime     : str       = self._dt_trainStart.time().toString("HH:mm")     
        self._trainEndTime       : str       = self._dt_trainEnd  .time().toString("HH:mm")     
        self._ts_ms_trainStart   : int       = 0
        self._ts_ms_trainEnd     : int       = 0
        self._testSpeed          : int       = 0
        self._maxChartCount      : int       = 0
      
        self._dt_testStart       : QDateTime = QDateTime.fromString("2022-06-06T12:00:00+03:00", Qt.DateFormat.ISODate)
        self._dt_testEnd         : QDateTime = QDateTime.fromString("2022-06-06T13:00:00+03:00", Qt.DateFormat.ISODate)
        self._testStartDate      : str       = self._dt_testStart.date().toString("dd/MM/yyyy")
        self._testEndDate        : str       = self._dt_testEnd  .date().toString("dd/MM/yyyy")
        self._testStartTime      : str       = self._dt_testStart.time().toString("HH:mm")     
        self._testEndTime        : str       = self._dt_testEnd  .time().toString("HH:mm")     

        self._ts_ms_testStart    : int       = 0
        self._ts_ms_testEnd      : int       = 0

        self.update_trainStart()
        self.update_trainEnd()
        self.update_testStart()
        self.update_trainEnd()



    # pair
    @pyqtProperty(str, notify=pairChanged)
    def pair(self)->str:
        return self._pair

    @pair.setter
    def pair(self, val:str):
        if self._pair != val:
            self._pair = val
            self.pairChanged.emit()

    @pyqtProperty(int, notify=pairIndexChanged)
    def pairIndex(self):
        return self._pairIndex

    @pairIndex.setter
    def pairIndex(self, index:int):
        if self._pairIndex != index:
            self._pairIndex = index
            self.pairIndexChanged.emit()

    

    # trainStartDate
    @pyqtProperty(str, notify=trainStartChanged)
    def trainStartDate(self):
        return self._trainStartDate

    @trainStartDate.setter
    def trainStartDate(self, val:str):
        if self._trainStartDate != val:
            self._trainStartDate = val
            self.update_trainStart()
            self.trainStartChanged.emit()

    # trainEndDate
    @pyqtProperty(str, notify=trainEndChanged)
    def trainEndDate(self):
        return self._trainEndDate

    @trainEndDate.setter
    def trainEndDate(self, val:str):
        if self._trainEndDate != val:
            self._trainEndDate = val
            self.update_trainEnd()
            self.trainEndChanged.emit()

    # trainStartTime
    @pyqtProperty(str, notify=trainStartChanged)
    def trainStartTime(self):
        return self._trainStartTime

    @trainStartTime.setter
    def trainStartTime(self, val:str):
        if self._trainStartTime != val:
            self._trainStartTime = val
            self.update_trainStart()
            self.trainStartChanged.emit()

    # trainEndTime
    @pyqtProperty(str, notify=trainEndChanged)
    def trainEndTime(self):
        return self._trainEndTime

    @trainEndTime.setter
    def trainEndTime(self, val:str):
        if self._trainEndTime != val:
            self._trainEndTime = val
            self.update_trainEnd()
            self.trainEndChanged.emit()

    # epoch
    @pyqtProperty(int, notify=epochChanged)
    def epoch(self):
        return self._epoch

    @epoch.setter
    def epoch(self, val:int):
        if self._epoch != val:
            self._epoch = val
            self.epochChanged.emit()

    # interval
    @pyqtProperty(str, notify=intervalChanged)
    def interval(self):
        return self._interval

    @interval.setter
    def interval(self, val:str):
        if self._interval != val:
            self._interval = val
            self.intervalChanged.emit()

    # dt_trainStart
    @pyqtProperty(QDateTime, notify=trainStartChanged)
    def dt_trainStart(self):
        return self._dt_trainStart

    @dt_trainStart.setter
    def dt_trainStart(self, val:QDateTime):
        if self._dt_trainStart != val:
            self._dt_trainStart = val

    # dt_trainEnd
    @pyqtProperty(QDateTime, notify=trainEndChanged)
    def dt_trainEnd(self):
        return self._dt_trainEnd

    @dt_trainEnd.setter
    def dt_trainEnd(self, val:QDateTime):
        if self._dt_trainEnd != val:
            self._dt_trainEnd = val

    # ts_ms_trainStart
    @pyqtProperty("long long", notify=trainStartChanged)
    def ts_ms_trainStart(self): 
        return self._ts_ms_trainStart

    @ts_ms_trainStart.setter
    def ts_ms_trainStart(self, val:int):
        if self._ts_ms_trainStart != val:
            self._ts_ms_trainStart = val

    # ts_ms_trainEnd
    @pyqtProperty("long long", notify=trainEndChanged)
    def ts_ms_trainEnd(self):
        return self._ts_ms_trainEnd

    @ts_ms_trainEnd.setter
    def ts_ms_trainEnd(self, val:int):
        if self._ts_ms_trainEnd != val:
            self._ts_ms_trainEnd = val

    # testSpeed
    @pyqtProperty(int, notify=testSpeedChanged)
    def testSpeed(self):
        return self._testSpeed

    @testSpeed.setter
    def testSpeed(self, val:int):
        if self._testSpeed != val:
            self._testSpeed = val
            self.testSpeedChanged.emit()

    # maxChartCount
    @pyqtProperty(int, notify=maxChartCountChanged)
    def maxChartCount(self):
        return self._maxChartCount

    @maxChartCount.setter
    def maxChartCount(self, val:int):
        if self._maxChartCount != val:
            self._maxChartCount = val
            self.maxChartCountChanged.emit()

    # testStartDate
    @pyqtProperty(str, notify=testStartChanged)
    def testStartDate(self):
        return self._testStartDate

    @testStartDate.setter
    def testStartDate(self, val:str):
        if self._testStartDate != val:
            self._testStartDate = val
            self.update_testStart()
            self.testStartChanged.emit()

    # testEndDate
    @pyqtProperty(str, notify=testEndChanged)
    def testEndDate(self):
        return self._testEndDate

    @testEndDate.setter
    def testEndDate(self, val:str):
        if self._testEndDate != val:
            self._testEndDate = val
            self.update_testEnd()
            self.testEndChanged.emit()

    # testStartTime
    @pyqtProperty(str, notify=testStartChanged)
    def testStartTime(self):
        return self._testStartTime

    @testStartTime.setter
    def testStartTime(self, val:str):
        if self._testStartTime != val:
            self._testStartTime = val
            self.update_testStart()
            self.testStartChanged.emit()

    # testEndTime
    @pyqtProperty(str, notify=testEndChanged)
    def testEndTime(self):
        return self._testEndTime

    @testEndTime.setter
    def testEndTime(self, val:str):
        if self._testEndTime != val:
            self._testEndTime = val
            self.update_testEnd()
            self.testEndChanged.emit()

    # dt_testStart
    @pyqtProperty(QDateTime, notify=testStartChanged)
    def dt_testStart(self):
        return self._dt_testStart

    @dt_testStart.setter
    def dt_testStart(self, val:QDateTime):
        if self._dt_testStart != val:
            self._dt_testStart = val


    # dt_testEnd
    @pyqtProperty(QDateTime, notify=testEndChanged)
    def dt_testEnd(self):
        return self._dt_testEnd

    @dt_testEnd.setter
    def dt_testEnd(self, val:QDateTime):
        if self._dt_testEnd != val:
            self._dt_testEnd = val

    # ts_ms_testStart
    @pyqtProperty("long long", notify=testStartChanged)
    def ts_ms_testStart(self):
        return self._ts_ms_testStart

    @ts_ms_testStart.setter
    def ts_ms_testStart(self, val:int):
        if self._ts_ms_testStart != val:
            self._ts_ms_testStart = val

    # ts_ms_testEnd
    @pyqtProperty("long long", notify=testEndChanged)
    def ts_ms_testEnd(self):
        return self._ts_ms_testEnd

    @ts_ms_testEnd.setter
    def ts_ms_testEnd(self, val:int):
        if self._ts_ms_testEnd != val:
            self._ts_ms_testEnd = val


    def update_trainStart(self):
        date = QDateTime.fromString(f"{self.trainStartDate} {self.trainStartTime}", "dd/MM/yyyy HH:mm")
        date.setTimeSpec(Qt.TimeSpec.UTC)
        self.dt_trainStart = date
        self.ts_ms_trainStart = self.dt_trainStart.toMSecsSinceEpoch()

    def update_trainEnd(self):
        date = QDateTime.fromString(f"{self.trainEndDate} {self.trainEndTime}", "dd/MM/yyyy HH:mm")
        date.setTimeSpec(Qt.TimeSpec.UTC)
        self.dt_trainEnd = date
        self.ts_ms_trainEnd = self.dt_trainEnd.toMSecsSinceEpoch()

    def update_testStart(self):
        date = QDateTime.fromString(f"{self.testStartDate} {self.testStartTime}", "dd/MM/yyyy HH:mm")
        date.setTimeSpec(Qt.TimeSpec.UTC)
        self.dt_testStart = date
        self.ts_ms_testStart = self.dt_testStart.toMSecsSinceEpoch()

    def update_testEnd(self):
        date = QDateTime.fromString(f"{self.testEndDate} {self.testEndTime}", "dd/MM/yyyy HH:mm")
        date.setTimeSpec(Qt.TimeSpec.UTC)
        self.dt_testEnd = date
        self.ts_ms_testEnd = self.dt_testEnd.toMSecsSinceEpoch()




    @pyqtSlot()
    def print_managementMdl_values(self):
        print("Train Start Date:"           .ljust(25), self.trainStartDate)
        print("Train End Date:"             .ljust(25), self.trainEndDate)
        print("Train Start Time:"           .ljust(25), self.trainStartTime)
        print("Train End Time:"             .ljust(25), self.trainEndTime)
        print("Epoch:"                      .ljust(25), self.epoch)
        print("Interval:"                   .ljust(25), self.interval)
        print("Pair:"                       .ljust(25), self.pair)
        print("Train Start DateTime:"       .ljust(25), self.dt_trainStart.toString())
        print("Train End DateTime:"         .ljust(25), self.dt_trainEnd.toString())
        
        ts_str_start = QDateTime.fromMSecsSinceEpoch(self.ts_ms_trainStart, QTimeZone.utc()).toString()
        print("Train Start Timestamp (ms):" .ljust(25), f"{self.ts_ms_trainStart} - {ts_str_start}")

        ts_str_end = QDateTime.fromMSecsSinceEpoch(self.ts_ms_trainEnd, QTimeZone.utc()).toString()
        print("Train End Timestamp (ms):"   .ljust(25), f"{self.ts_ms_trainEnd} - {ts_str_end}")

        print("Test Speed:"                 .ljust(25), self.testSpeed)
        print("Max Chart Count:"            .ljust(25), self.maxChartCount)
        print("Test Start Date:"            .ljust(25), self.testStartDate)
        print("Test End Date:"              .ljust(25), self.testEndDate)
        print("Test Start Time:"            .ljust(25), self.testStartTime)
        print("Test End Time:"              .ljust(25), self.testEndTime)
        print("Test Start DateTime:"        .ljust(25), self.dt_testStart.toString())
        print("Test End DateTime:"          .ljust(25), self.dt_testEnd.toString())

        ts_str_test_start = QDateTime.fromMSecsSinceEpoch(self.ts_ms_testStart, QTimeZone.utc()).toString()
        print("Test Start Timestamp (ms):"  .ljust(25), f"{self.ts_ms_testStart} - {ts_str_test_start}")

        ts_str_test_end = QDateTime.fromMSecsSinceEpoch(self.ts_ms_testEnd, QTimeZone.utc()).toString()
        print("Test End Timestamp (ms):"    .ljust(25), f"{self.ts_ms_testEnd} - {ts_str_test_end}")
