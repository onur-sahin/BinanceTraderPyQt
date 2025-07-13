from __future__ import annotations
from typing import TYPE_CHECKING

from PyQt6.QtCore import QObject
import logging
from datetime import datetime
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException

from AccountTypes import AccountTypes

if TYPE_CHECKING:
    from AccountMdl import AccountMdl

class BinanceDriver(QObject):

    URL_SPOT_REAL           = "https://api.binance.com"          
    URL_SPOT_MOCK           = "https://testnet.binance.vision"   
    URL_FUTURES_USDT_M_REAL = "https://fapi.binance.com"         
    URL_FUTURES_USDT_M_MOCK = "https://testnet.binancefuture.com"
    URL_FUTURES_COIN_M_REAL = "https://dapi.binance.com"         
    URL_FUTURES_COIN_M_MOCK = "https://testnet.binancefuture.com"
    URL_VANILLA_REAL        = "https://vapi.binance.com"         
    URL_VANILLA_MOCK        = "NOT ABSENT"                       

    def __init__(self):
        super().__init__()

        self.accountMdl:AccountMdl = None
        self.client = Client()
       


    def update_driver(self, accountMdl:AccountMdl):

        self.accountMdl        = accountMdl
        self.client.API_KEY    = self.accountMdl.apiKey
        self.client.API_SECRET = self.accountMdl.apiSecret

        if self.accountMdl.accountType == AccountTypes.to_string(AccountMdl.BINANCE):
            if self.accountMdl.realAccount:
                self.client.API_URL = BinanceDriver.URL_SPOT_REAL
            else:
                self.client.API_URL = BinanceDriver.URL_SPOT_MOCK

        elif self.accountMdl.AccountTypes == AccountTypes.to_string(AccountTypes.CM_FUTURE):
            if self.accountMdl.realAccount:
                self.client.API_URL = BinanceDriver.URL_FUTURES_COIN_M_REAL
            else:
                self.client.API_URL = BinanceDriver.URL_FUTURES_COIN_M_MOCK

        elif self.accountMdl.accountType == AccountTypes.to_string(AccountTypes.UM_FUTURE):
            if self.accountMdl.realAccount:
                self.client.API_URL = BinanceDriver.URL_FUTURES_USDT_M_REAL
            else:
                self.client.API_URL = BinanceDriver.URL_FUTURES_USDT_M_MOCK

        else:
            raise f"invalid accountType for binance endpoint.\naccountType:{self.accountMdl.accountType}\nrealAccount:{self.accountMdl.realAccount}"

        # client.API_URL = "https://testnet.binance.vision/api"

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

    @staticmethod
    def test_binance_credentials(api_key: str, api_secret: str, base_endpoint:str= Client.BASE_ENDPOINT_DEFAULT, testnet=False) -> bool:

        if testnet:
            client = Client(api_key=api_key, api_secret=api_secret, testnet=True )

        else:
            client = Client(api_key      =api_key,
                            api_secret   =api_secret,
                            base_endpoint=base_endpoint,
                            )

        try:
        
            # Basit bir endpoint çağrısı: get_account
            client.get_account()
            print("✅ API anahtarları geçerli.")
            return True
        
        except BinanceAPIException as e:
            print(f"❌ Binance API hatası: {e}")
            return False
        
        except BinanceRequestException as e:
            print(f"❌ Bağlantı hatası: {e}")
            return False
        
        except Exception as e:
            print(f"❌ Diğer hata: {e}")
            return False




if __name__=="__main__":
    client = BinanceDriver()

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