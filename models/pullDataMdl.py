from PyQt6.QtCore import QObject, pyqtSignal, pyqtProperty, pyqtSlot
from PyQt6.QtCore import QDateTime, QTimeZone, Qt, QThread
from PyQt6.QtCore import qCritical, qInfo, qWarning
from concurrent.futures import ThreadPoolExecutor
from Queries import Queries, Q

import threading
import time
from returns.result import Failure

from DBManager import DBManager
from Binance   import BinanceDriver

class PullDataWorker(QObject):

    finished                = pyqtSignal()
    valueChanged            = pyqtSignal(float)
    valueChanged2           = pyqtSignal(float)
    maxValueChanged         = pyqtSignal(float)
    maxValueChanged2        = pyqtSignal(float)



    def __init__(self, parent=None):
        super().__init__(parent)

        self._startTs             = 0
        self._endTs               = 0
        self._table_name          = ""
        self._pair                = ""
        self._interval            = ""
        
        self._deltaMs             = 0
        self._500deltaMs          = 0
        self._preDeltaCount       = 50
        self._preDeltaMs          = 0
        self._account             = None

        self._maxFetchedCount     = 500

        self._db                  = DBManager.get_instance()

        self._ts_inDatabase       = []

        self._pair_ts             = []



    def run(self):

        self._deltaMs    = self.intervalToMs(self._interval)
        self._500deltaMs = self._deltaMs * 500
        self._preDeltaMs = self._preDeltaCount * self._deltaMs

        if self._startTs > self._endTs:
            qWarning(f"start time stamp couldn't be greater than end time stamp!")
            self.finished.emit()
            return


        startTs = ((self._startTs + self._deltaMs - 1) // self._deltaMs) * self._deltaMs
        startTs = startTs - self._preDeltaMs
        endTs = (self._endTs // self._deltaMs) * self._deltaMs

        self.query_table_exist = Queries.get(Q.SELECT_TABLE_EXISTS)

        result = self._db.execute_select_return_list(self.query_table_exist,  {"table_name":self._table_name})

        if isinstance(result, Failure):
            qCritical(f"error while getting exists kline table, error:\n {result.failure()}")
            self.finished.emit()
            return

        if not result.unwrap():

            self.query_createTable = Queries.get(Q.CREATE_KLINE_TABLE, table_name=self._table_name)
            result = self._db.execute(self.query_createTable)

            if isinstance(result, Failure):

                qCritical(f"error while creating kline table, error:\n{result.failure()}")
                self.finished.emit()
                return

        self._query = Queries.get(Q.SELECT_TIMESTAMPS, table_name=self._table_name)

        #result is asc order  
        result = self._db.execute_select_return_list( self._query,
                                                     {"start_ts"      :startTs,
                                                      "end_ts"        :endTs
                                                     }
                                                    )

        if isinstance(result, Failure):
            self.finished.emit()
            qCritical(f"error while getting timestamps saved on database.\nError:\n{result.failure()}")
            return


        self._ts_inDatabase = result.unwrap()


        temp_ts   = startTs
        absent_ts = []

        while temp_ts <= endTs:

            if temp_ts not in self._ts_inDatabase:

                absent_ts.append(temp_ts)

            temp_ts += self._deltaMs


        if len(absent_ts):
            temp_startTs = absent_ts[0]
            self.maxValueChanged.emit( len( absent_ts ) )

        else:
            self.maxValueChanged.emit(1)
            self.valueChanged   .emit(1)

        count   = 0
        max_idx = len  (absent_ts) - 1
        idxs    = range( max_idx )

        for idx in idxs:
            count+=1
            ts    = absent_ts[idx]
            next_ts    = ts + self._deltaMs

            if max_idx != idx:

                if next_ts != absent_ts[idx+1] or count >= self._maxFetchedCount:

                    self._pair_ts.append( [temp_startTs, ts] )
                    temp_startTs = next_ts
                    count        = 0

            else:
                self._pair_ts.append([ts, ts])
                count = 0



        for i in self._pair_ts:
            print(f"{QDateTime.fromMSecsSinceEpoch(i[0]).toString('dd/MM HH:mm')}  -  {QDateTime.fromMSecsSinceEpoch(i[1]).toString('dd/MM HH:mm')}")

        binanceDriver = BinanceDriver(self._account)

        result = binanceDriver.fetchHistoricalData(self._pair, self._interval, self._startTs, self._endTs)

        print(result)

        self.finished.emit()
        print("run() function finished")


    def intervalToMs(self, interval: str) -> int:
        if interval.endswith("m"):
            return 5 * 60 * 1000
        return 5 * 60 * 1000


    def get_last_ts(self)->int:
        pass
        

    def pull_data(self, start_ts:int, end_ts:int)->list:
        pass

        

        

class PullDataMdl(QObject):
    # Signals
    valueChanged            = pyqtSignal()
    maxValueChanged         = pyqtSignal()
    maxValue2Changed        = pyqtSignal()
    value2Changed           = pyqtSignal()
    pairChanged             = pyqtSignal()
    intervalChanged         = pyqtSignal()
    startChanged            = pyqtSignal()
    endChanged              = pyqtSignal()
    accountChanged          = pyqtSignal()
    dataFetched             = pyqtSignal()
    dataDerived             = pyqtSignal()
    finished                = pyqtSignal()
    errorOccurred           = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        # Private variables
        self._maxValue            = 100.0
        self._value               = 0.0
        self._maxValue2           = 100.0
        self._value2              = 0.0
        self._pair                = "BTCUSDT"
        self._interval            = "5m"
        self._startTs             = 0
        self._endTs               = 0
        self._startDt             = ""
        self._endDt               = ""
        self._account             = None

        self._cancelFlag          = False
        self._errorFlag           = False

        self._maxFetchedCount     = 500
        self._pulledLastTimestamp = -1

        self._thread               = QThread()
        self._pullDataWorker       = PullDataWorker()

        self._pullDataWorker.moveToThread(self._thread)

        self._pullDataWorker.valueChanged       .connect(lambda value: self.value(value))
        # self._pullDataWorker.maxValueChanged    .connect(lambda value: self.maxValue(value))

        self._thread        .started .connect(self._pullDataWorker.run)
        self._pullDataWorker.finished.connect(self.cleanup)


    # --- Properties ---
    @pyqtProperty(float, notify=maxValueChanged)
    def maxValue(self):
        return self._maxValue

    @maxValue.setter
    def maxValue(self, val):
        if self._maxValue != val:
            self._maxValue = val
            self.maxValueChanged.emit()

    @pyqtProperty(float, notify=valueChanged)
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        if self._value != val:
            self._value = val
            self.valueChanged.emit()

    @pyqtProperty(float, notify=maxValue2Changed)
    def maxValue2(self):
        return self._maxValue2

    @maxValue2.setter
    def maxValue2(self, val):
        if self._maxValue2 != val:
            self._maxValue2 = val
            self.maxValue2Changed.emit()

    @pyqtProperty(float, notify=value2Changed)
    def value2(self):
        return self._value2

    @value2.setter
    def value2(self, val):
        if self._value2 != val:
            self._value2 = val
            self.value2Changed.emit()

    @pyqtProperty(str, notify=pairChanged)
    def pair(self):
        return self._pair

    @pair.setter
    def pair(self, val):
        if self._pair != val:
            self._pair = val
            self.pairChanged.emit()

    @pyqtProperty(str, notify=intervalChanged)
    def interval(self):
        return self._interval

    @interval.setter
    def interval(self, val):
        if self._interval != val:
            self._interval = val
            self.intervalChanged.emit()

    @pyqtProperty("long long", notify=startChanged)
    def startTs(self):
        return self._startTs

    @startTs.setter
    def startTs(self, val):
        if self._startTs != val:
            self._startTs = val
            self.startDt = QDateTime.fromMSecsSinceEpoch(self.startTs, Qt.TimeSpec.UTC).toString("dd/MM/yyyy HH:mm")
            self.startChanged.emit()

    @pyqtProperty("long long", notify=endChanged)
    def endTs(self):
        return self._endTs

    @endTs.setter
    def endTs(self, val):
        if self._endTs != val:
            self._endTs = val
            self._endDt = QDateTime.fromMSecsSinceEpoch(self._endTs, Qt.TimeSpec.UTC).toString("dd/MM/yyyy HH:mm")
            self.endChanged.emit()

    @pyqtProperty(str, notify=startChanged)
    def startDt(self):
        return self._startDt
    
    @startDt.setter
    def startDt(self, val):
        if self._startDt != val:
            self._startDt = val

    @pyqtProperty(str, notify=endChanged)
    def endDt(self):
        return self._endDt
    
    @endDt.setter
    def endDt(self, val):
        if self._endDt != val:
            self._endDt = val


    @pyqtProperty(QObject, notify=accountChanged)
    def account(self):
        return self._account

    @account.setter
    def account(self, val):
        self._account = val
        self.accountChanged.emit()

    # --- Methods ---
    def intervalToMs(self, interval: str) -> int:
        if interval.endswith("m"):
            return 5 * 60 * 1000
        return 5 * 60 * 1000


    @pyqtSlot()

    @pyqtSlot()
    def pull_data(self):

        self._pullDataWorker._startTs    = self.startTs
        self._pullDataWorker._endTs      = self.endTs
        self._pullDataWorker._interval   = self._interval
        self._pullDataWorker._table_name = f"tbl_{self._pair.lower()}_{self._interval}"
        self._pullDataWorker._pair       = self.pair
        self._pullDataWorker._account    = self.account

        # self._pullDataWorker.

        self._thread.start()

    def cleanup(self):
        print("pull data ended")
        self._thread.quit()
        self._thread.wait()
        self._pullDataWorker.deleteLater()
        self._thread.deleteLater()


    # Cancel ve error flag
    def set_cancel_flag(self):
        self._cancelFlag = True

    def set_error_flag(self):
        self._errorFlag = True

    @pyqtSlot(QObject)
    def startPullData(self, item:QObject):

        # mdl:PullDataMdl = item.findChild(QObject, "pullDataMdl", Qt.FindChildOption.FindChildrenRecursively)

        pass

    @pyqtSlot()
    def print_values(self):
        print(f"_maxValue:            {self._maxValue}")
        print(f"_value:               {self._value}")
        print(f"_maxValue2:           {self._maxValue2}")
        print(f"_value2:              {self._value2}")
        print(f"_pair:                {self._pair}")
        print(f"_interval:            {self._interval}")
        print(f"_startTs:             {self._startTs}")
        print(f"_endTs:               {self._endTs}")
        print(f"_startDt:             {self._startDt}")
        print(f"_endDt:               {self._endDt}")
        print(f"_cancelFlag:          {self._cancelFlag}")
        print(f"_errorFlag:           {self._errorFlag}")
        print(f"_table_name:          {self._table_name}")
        print(f"_deltaMs:             {self._deltaMs}")
        print(f"_500deltaMs:          {self._500deltaMs}")
        print(f"_preDeltaCount:       {self._preDeltaCount}")
        print(f"_preDeltaMs:          {self._preDeltaMs}")
        print(f"_maxFetchedCount:     {self._maxFetchedCount}")
        print(f"_pulledLastTimestamp: {self._pulledLastTimestamp}")