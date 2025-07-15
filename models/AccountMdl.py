from PyQt6.QtCore import QObject, pyqtSignal, QVariant
from PyQt6.QtCore import pyqtProperty, pyqtSlot
from PyQt6.QtCore import qCritical, qInfo
from psycopg2.errors import UniqueViolation
import json
import os
from typing import List, Optional
from Binance import BinanceDriver
from DBManager import DBManager
from CryptoManager import CryptoManager
from HashManager import HashManager

from AccountTypes import AccountTypes
from Queries import Queries, Q
from returns.result import Success, Failure

from AccountListModelMdl import AccountListModelMdl


class AccountMdl(QObject):
    accountNameChanged          = pyqtSignal()
    apiKeyChanged               = pyqtSignal()
    apiSecretChanged            = pyqtSignal()
    realAccountChanged          = pyqtSignal()
    accountTypeChanged          = pyqtSignal()
    testResultChanged           = pyqtSignal()
    accountPassChanged          = pyqtSignal()
    rememberAccountPassChanged  = pyqtSignal()
    accountNotesChanged         = pyqtSignal()
    isLockedChanged             = pyqtSignal()
    cryptedApiKeyChanged        = pyqtSignal()
    cryptedApiSecretChanged     = pyqtSignal()
    updatedDecryptedKeys        = pyqtSignal()
    newAccountCreated           = pyqtSignal(QObject)  # Signal emitted when a new account is created

    _accountsList = []  # Static list to hold all accounts

    def __init__(self, parent=None):
        super().__init__(parent)
        self._accountName                   = ""
        self._apiKey                        = ""
        self._apiSecret                     = ""
        self._realAccount                   = True
        self._testResult                    = ""
        self._accountPass                   = ""
        self._rememberAccountPass           = False
        self._isLocked                      = True
        self._cryptedApiKey                 = ""
        self._cryptedApiSecret              = ""
        self._accountNotes                  = "a"
        self._accountType                   = 0
        self._cryptoManager                 = CryptoManager()
        self._binanceDriver                 = BinanceDriver() # Every model has individual object of BinanceDriver's Class

        self.updatedDecryptedKeys.connect(self.onUpdatedDecryptedKeys)

    @pyqtProperty(str, notify=accountNameChanged)
    def accountName(self):
        return self._accountName

    @accountName.setter
    def accountName(self, name: str):
        if self._accountName != name:
            self._accountName = name
            self.accountNameChanged.emit()

    @pyqtProperty(str, notify=apiKeyChanged)
    def apiKey(self):
        return self._apiKey

    @apiKey.setter
    def apiKey(self, key: str):
        if self._apiKey != key:
            self._apiKey = key
            self.apiKeyChanged.emit()
            self.updatedDecryptedKeys.emit()

    @pyqtProperty(str, notify=apiSecretChanged)
    def apiSecret(self):
        return self._apiSecret

    @apiSecret.setter
    def apiSecret(self, secret: str):
        if self._apiSecret != secret:
            self._apiSecret = secret
            self.apiSecretChanged.emit()
            self.updatedDecryptedKeys.emit()

    @pyqtProperty(bool, notify=realAccountChanged)
    def realAccount(self):
        return self._realAccount

    @realAccount.setter
    def realAccount(self, real: bool):
        if self._realAccount != real:
            self._realAccount = real
            self.realAccountChanged.emit()

    @pyqtProperty(str, notify=testResultChanged)
    def testResult(self):
        return self._testResult

    @testResult.setter
    def testResult(self, test_result: str):
        if self._testResult != test_result:
            self._testResult = test_result
            self.testResultChanged.emit()

    @pyqtProperty(str, notify=accountPassChanged)
    def accountPass(self):
        return self._accountPass

    @accountPass.setter
    def accountPass(self, account_pass: str):
        if self._accountPass != account_pass:
            self._accountPass = account_pass
            self.accountPassChanged.emit()
            self.updatedDecryptedKeys.emit()

    @pyqtProperty(bool, notify=rememberAccountPassChanged)
    def rememberAccountPass(self):
        return self._rememberAccountPass

    @rememberAccountPass.setter
    def rememberAccountPass(self, remember: bool):
        if self._rememberAccountPass != remember:
            self._rememberAccountPass = remember
            self.rememberAccountPassChanged.emit()

    @pyqtProperty(str, notify=accountNotesChanged)
    def accountNotes(self):
        return self._accountNotes

    @accountNotes.setter
    def accountNotes(self, notes: str):
        if self._accountNotes != notes:
            self._accountNotes = notes
            self.accountNotesChanged.emit()

    @pyqtProperty(bool, notify=isLockedChanged)
    def isLocked(self):
        return self._isLocked

    @isLocked.setter
    def isLocked(self, locked: bool):
        if self._isLocked != locked:
            self._isLocked = locked
            self.isLockedChanged.emit()

    @pyqtProperty(str, notify=cryptedApiKeyChanged)
    def cryptedApiKey(self):
        return self._cryptedApiKey

    @cryptedApiKey.setter
    def cryptedApiKey(self, hashed_api_key: str):
        if self._cryptedApiKey != hashed_api_key:
            self._cryptedApiKey = hashed_api_key
            self.cryptedApiKeyChanged.emit()

    @pyqtProperty(str, notify=cryptedApiSecretChanged)
    def cryptedApiSecret(self):
        return self._cryptedApiSecret

    @cryptedApiSecret.setter
    def cryptedApiSecret(self, hashed_api_secret: str):
        if self._cryptedApiSecret != hashed_api_secret:
            self._cryptedApiSecret = hashed_api_secret
            self.cryptedApiSecretChanged.emit()

    @pyqtProperty(int, notify=accountTypeChanged)
    def accountType(self):
        return self._accountType

    @accountType.setter
    def accountType(self, account_type:AccountTypes):
        if self._accountType != account_type:
            self._accountType = account_type
            self.accountTypeChanged.emit()

    @pyqtSlot(str)
    def update_account_notes(self, notes:str):

        db = DBManager.get_instance()

        query = Queries.get(Q.UPDATE_ACCOUNT_NOTES)

        result = db.execute(query, {"notes":notes, "account_name":self.accountName})

        if isinstance(result, Failure):
            qCritical(f"Failere in update_account_notes(): {str( result.failure() )}")


    @pyqtSlot()
    def update_account_from_database():
        db = DBManager.get_instance()

    @pyqtSlot()
    def save_account(self):
        db = DBManager.get_instance()
        hashed_text = HashManager.get_instance().hash(self.accountPass)
        self._cryptoManager.loadKey(hashed_text, False)

        bind_values = {}
        bind_values["account_name"] = self.accountName
        bind_values["real_account"] = self.realAccount
        bind_values["account_type"] = self.accountType
        bind_values["api_key"     ] = self._cryptoManager.encrypt(self.apiKey)
        bind_values["api_secret"  ] = self._cryptoManager.encrypt(self.apiSecret)
        bind_values["notes"       ] = ""


        insert_result = db.execute(Queries.get(Q.INSERT_ACCOUNT), bind_values)
        
        if isinstance(insert_result, Failure):

            if isinstance(insert_result.failure(), UniqueViolation):
                qInfo(f"account_name: {self.accountName} already exists in database, please select another name!")
                return
            
            qCritical(f"Failed to insert account into database: {str( insert_result.failure() )}")
            return

        query = f"SELECT * FROM tbl_accounts WHERE account_name='{self.accountName}'"
        result = db.execute_select_return_dict(query)
        if isinstance(result, Failure):
            qCritical(f"Failed to fetch account from database: {str( result.failure() )}")
            return

        added_account = result.unwrap()[0]

        if len(added_account) == 0:
            qCritical(f"account_name={self.accountName} : Account not found in database")
            return

        new_account = self.create_accountMdl_from_data(added_account)
        new_account.isLocked = True

        if self.rememberAccountPass:
            self._cryptoManager.loadKey("ZzAXPpV2K4k6e7mShY11gsyMK9EBV1ZzQv9rNp0M5roJ9j9kaml2M4Ax6M73ALmZ", False)
            self.saveAccountToJsonFile(self.accountName, self._cryptoManager.encrypt(hashed_text))
            new_account.isLocked = False

        self.accountPass = hashed_text
        self.newAccountCreated.emit(new_account)

    @pyqtSlot()
    def test_account(self):



        try:
            # Hesap bilgilerini getirerek API anahtarlarının geçerliliğini kontrol et
            account_info = Client(api_key=self.apiKey, api_secret=self.apiSecret, testnet=(not self.realAccount)).get_account()
            print("API Key geçerli! Hesap bilgileri alındı.")
        except BinanceAPIException as e:
            print(f"API Key hatalı veya izinler eksik: {e}")

        # respond = Binance.binance_api_request(
        #     self.apiKey,
        #     self.apiSecret,
        #     "api/v3/account",
        #     "",
        #     False
        # )
        # json_doc = json.loads(respond)
        # if "uid" not in json_doc:
        #     self.testResult = respond
        #     return False
        # self.testResult = "Account is valid"
        return True

    @staticmethod
    def get_account_keys_from_json():
        users_path = os.path.join(os.getcwd(), "..", "share", "users.json")

        if not os.path.exists(users_path)  :
            return []

        try:
            with open(users_path, "r") as file:
                data = json.load(file)
                return data
        except Exception as e:
            print(f"Failed to read users.json: {e}")
            return []

    @staticmethod
    def saveAccountToJsonFile(account_name: str, hash_value: str):
        users_path = os.path.join(os.getcwd(), "..", "share", "users.json")
        backup_path = users_path + ".bak"

        try:
            if os.path.exists(users_path):
                if os.path.exists(backup_path):
                    os.remove(backup_path)
                os.rename(users_path, backup_path)

            with open(users_path, "w") as file:
                json.dump({"accountName": account_name, "accountPass": hash_value}, file)
        except Exception as e:
            print(f"Failed to save account to JSON: {e}")

    @staticmethod
    def removeAccountFromJsonFile(account_name: str):
        users_path = os.path.join(os.getcwd(), "..", "share", "users.json")
        backup_path = users_path + ".bak"

        try:
            if os.path.exists(users_path):
                if os.path.exists(backup_path):
                    os.remove(backup_path)
                os.rename(users_path, backup_path)

            with open(users_path, "r") as file:
                data = json.load(file)

            if isinstance(data, list):
                data = [item for item in data if item.get("accountName") != account_name]

            with open(users_path, "w") as file:
                json.dump(data, file)
        except Exception as e:
            print(f"Failed to remove account from JSON: {e}")

    @pyqtSlot()
    def loadFromDatabaseRequested(self):

        db = DBManager.get_instance()
        query = "SELECT * FROM tbl_accounts"
        result = db.execute_select_return_dict(query)
        if isinstance(result, Failure):
            qCritical(f"Failed to load accounts from database: {str( result.failure() )}")
            return

        accounts_list = result.unwrap()
        account_key_list = self.get_account_keys_from_json()

        for account in accounts_list:
            account_name = account.get("account_name")

            if AccountListModelMdl.findIndexByAccountName(account_name) != -1:
                continue

            if any(acc.accountName == account_name for acc in self._accountsList):
                continue

            new_account = self.create_accountMdl_from_data(account)
            for key in account_key_list:
                if key.get("accountName") == account_name:
                    account_pass = key.get("accountPass")
                    new_account._cryptoManager.loadKey("ZzAXPpV2K4k6e7mShY11gsyMK9EBV1ZzQv9rNp0M5roJ9j9kaml2M4Ax6M73ALmZ", False)
                    hash_value = new_account._cryptoManager.decrypt(account_pass)
                    new_account._cryptoManager.loadKey(hash_value, False)
                    new_account.apiKey = new_account._cryptoManager.decrypt(new_account.cryptedApiKey)
                    new_account.apiSecret = new_account._cryptoManager.decrypt(new_account.cryptedApiSecret)
                    new_account.isLocked = False
                    break

            self.newAccountCreated.emit(new_account)

    @staticmethod
    def create_accountMdl_from_data(vm:dict):

        account = AccountMdl()
        account.accountName      = vm.get("account_name" , "")
        account.realAccount      = vm.get("real_account" , True)
        account.accountType      = vm.get("account_type" , "")
        account.cryptedApiKey    = vm.get("api_key"      , "")
        account.cryptedApiSecret = vm.get("api_secret"   , "")
        account.accountNotes     = vm.get("notes"        , "")
        account.isLocked         = True
        return account

    @pyqtSlot()
    def onUpdatedDecryptedKeys(self):
        pass