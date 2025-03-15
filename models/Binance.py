from PyQt6.QtCore import QObject
import logging
from datetime import datetime
from binance.client import Client


class Binance(QObject):

    def __init__(self):
        super().__init__()
        self.apiKey   :str     = None # "QMxrX7326ZliOtqUh4PmqkUhyC2Sx4qAcAfXsslkmK34htk2pljqrbhfLRmtC5iL"
        self.apiSecret:str     = None # "9yXrwLHFYZr5TSOBq7gEXu25RwUkOQISSAWNwvajtmGgTPRqnM3ndZBdeqpUPHSG"
        self.client    :Client = Client(self.apiKey, self.apiSecret)


    def fetchBinanceHistoricalData(self, symbol:str, interval:str, startTime:str, endTime:str, limit=750)->str:


        trialCount = 1


        while trialCount <= 3:

            try:
                return self.client.get_historical_klines(symbol, interval, start_str=startTime, end_str=endTime, limit=limit)

            except Exception as e:
                logging.info(e)

                if trialCount == 3:
                    raise 
            trialCount+=1




if __name__=="__main__":
    client = Binance()

    klines = client.fetchBinanceHistoricalData("BTCUSDT", Client.KLINE_INTERVAL_5MINUTE, 1741597200000, 1741600800000)
    print(klines)





'''
s-> seconds; m -> minutes; h -> hours; d -> days; w -> weeks; M -> months

1s
1m
3m
5m
15m
30m
1h
2h
4h
6h
8h
12h
1d
3d
1w
1M
'''