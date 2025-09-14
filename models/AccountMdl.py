from PyQt6.QtCore import QObject, pyqtSignal, QVariant
from PyQt6.QtCore import pyqtProperty, pyqtSlot
from PyQt6.QtCore import qCritical, qInfo, qWarning
from psycopg2.errors import UniqueViolation
import threading
import json
import os
from typing import List, Optional
from Binance import BinanceDriver
from DBManager import DBManager
from CryptoManager import CryptoManager
from HashManager import HashManager

from AccountTypes import AccountTypes
from Queries import Queries, Q
from returns.result import Result, Success, Failure


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
    _lock = threading.Lock()  # Thread-safe için Lock


    def __init__(self, parent=None):
        super().__init__(parent)
        self._accountName                   = ""
        self._apiKey                        = ""
        self._apiSecret                     = ""
        self._realAccount                   = True
        self._testResult                    = ""
        self._accountPass                   = ""
        self._hashedAccountPass             = ""
        self._cryptedHashedAccountPass      = ""
        self._rememberAccountPass           = False
        self._isLocked                      = True
        self._cryptedApiKey                 = ""
        self._cryptedApiSecret              = ""
        self._accountNotes                  = ""
        self._accountType                   = 0
        self._cryptoManager                 = CryptoManager()
        self._binanceDriver                 = BinanceDriver() # Every model has individual object of BinanceDriver's Class
        self._accountPassKey                = "ZzAXPpV2K4k6e7mShY11gsyMK9EBV1ZzQv9rNp0M5roJ9j9kaml2M4Ax6M73ALmZ"

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
        self._hashedAccountPass = HashManager.get_instance().hash(self.accountPass)
        self._cryptoManager.loadKey(self._hashedAccountPass, False)

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

        new_account           = self.create_accountMdl_from_data(added_account)
        new_account.isLocked  = False
        new_account.apiKey    = self.apiKey
        new_account.apiSecret = self.apiSecret


        self.newAccountCreated.emit(new_account)

        if self.rememberAccountPass:

            self._cryptoManager.loadKey("ZzAXPpV2K4k6e7mShY11gsyMK9EBV1ZzQv9rNp0M5roJ9j9kaml2M4Ax6M73ALmZ", False)

            result2 = self.saveAccountToJsonFile(self.accountName, self._cryptoManager.encrypt(self._hashedAccountPass))

            if isinstance(result2, Failure):
                qCritical(f"{self.accountName} couldn't save to json file: {str(result2.failure())}")
                return

            new_account.isLocked = False

    @pyqtSlot()
    def test_account(self):



            # Hesap bilgilerini getirerek API anahtarlarının geçerliliğini kontrol et
            binanceDriver = BinanceDriver(self)
            return BinanceDriver.test_binance_credentials(self.apiKey, self.apiSecret, )

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

    @staticmethod
    def saveAccountToJsonFile(account_name: str, hash_value: str) -> Result[None, Exception]:
        
        base_dir = os.path.join(os.getcwd(), "share")
        os.makedirs(base_dir, exist_ok=True)

        users_path = os.path.join(base_dir, "users.json")
        backup_path = users_path + ".bak"

        try:
            with AccountMdl._lock:
                data = []

                # Mevcut dosyayı oku
                if os.path.exists(users_path):
                    with open(users_path, "r", encoding="utf-8") as file:
                        existing_data = json.load(file)
                        if isinstance(existing_data, dict):
                            data.append(existing_data)
                        elif isinstance(existing_data, list):
                            data.extend(existing_data)

                # Aynı accountName varsa güncelle, yoksa ekle
                updated = False
                for acc in data:
                    if acc.get("accountName") == account_name:
                        acc["accountPass"] = hash_value
                        updated = True
                        break

                if not updated:
                    data.append({"accountName": account_name, "accountPass": hash_value})

                # Eski dosyayı yedekle
                if os.path.exists(users_path):
                    if os.path.exists(backup_path):
                        os.remove(backup_path)
                    os.rename(users_path, backup_path)

                # Yeni dosyayı yaz
                with open(users_path, "w", encoding="utf-8") as file:
                    json.dump(data, file, ensure_ascii=False, indent=4)

                # Yazma başarılı olduysa yedeği sil
                if os.path.exists(backup_path):
                    os.remove(backup_path)

            return Success(None)

        except Exception as e:
            return Failure(e)

    @staticmethod
    def removeAccountFromJsonFile(account_name: str) -> Result[None, Exception]:
        base_dir = os.path.join(os.getcwd(), "share")
        os.makedirs(base_dir, exist_ok=True)
        users_path = os.path.join(base_dir, "users.json")

        try:
            if not os.path.exists(users_path):
                return Failure(FileNotFoundError(f"File not found: {users_path}"))

            # Dosyayı oku
            with open(users_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            # Tek kayıt varsa ve eşleşiyorsa dosyayı tamamen sil
            if isinstance(data, dict):
                if data.get("accountName") == account_name:
                    os.remove(users_path)  # Dosyayı tamamen kaldır
                    return Success(None)
                else:
                    return Failure(ValueError(f"Account '{account_name}' not found"))

            # Liste ise filtrele
            elif isinstance(data, list):
                original_length = len(data)
                data = [acc for acc in data if acc.get("accountName") != account_name]

                if len(data) == original_length:
                    return Failure(ValueError(f"Account '{account_name}' not found"))

                # Yeni liste boşsa dosyayı tamamen kaldır
                if not data:
                    os.remove(users_path)
                else:
                    with open(users_path, "w", encoding="utf-8") as file:
                        json.dump(data, file, ensure_ascii=False, indent=4)

            return Success(None)

        except Exception as e:
            return Failure(e)

    def decrypt_cryptedHashedAccountPass(self):
        self._cryptoManager.loadKey(self._accountPassKey)
        self._hashedAccountPass = self._cryptoManager.decrypt(self._cryptedHashedAccountPass)

    @pyqtSlot(str)
    def decryptKeys(self, accountPass:str=None):

        if accountPass != None:
            self._accountPass = accountPass
            self._hashedAccountPass = HashManager.get_instance().hash(self._accountPass)

        self._cryptoManager.loadKey(self._hashedAccountPass)

        self.apiKey    = self._cryptoManager.decrypt(self.cryptedApiKey)
        self.apiSecret = self._cryptoManager.decrypt(self.cryptedApiSecret)
        self.isLocked  = (self.apiKey=="") or (self.apiSecret=="")


        # self.dataChanged.emit(self.index(idx), self.index(idx), [self.IsLockedRole])

    @pyqtSlot(str, str, result=bool)
    def testAccount(self, api_key, api_secret):
        return BinanceDriver.test_binance_credentials(api_key, api_secret)

    @pyqtSlot(str, bool)
    def save_decryptedKeys(self, save_to_json=False) :

        self.decryptKeys(self.accountPass)

        if save_to_json:
            hashed_text = HashManager.get_instance().hash(self.accountPass)
            self._cryptoManager.loadKey(self._accountPassKey)
            self.saveAccountToJsonFile( self.accountName, self._cryptoManager.encrypt(hashed_text) )

    @pyqtSlot(result=bool)
    def deleteAccount(self):

        result2 = self.removeAccountFromJsonFile(self.accountName)

        if isinstance(result2, Failure):
            if isinstance(result2, ValueError):
                qWarning(f"{str(result2.failure())}")
            elif isinstance(result2, FileNotFoundError):
                qWarning(f"str({result2.failure()})")
            else:
                qCritical(f"{self.accountName} deleted from database but couldn't remove json file: {str(result2.failure())}")

        result1 = self.deleteAccountFromDatabase()

        if not result1:
            return False

        return True

    def deleteAccountFromDatabase(self):
        db = DBManager.get_instance()
        result = db.execute(Queries.get(Q.DELETE_ACCOUNT), {"account_name":self.accountName})

        if isinstance(result, Failure):
            qCritical(f"FAILURE! {self.accountName} couldn't delete from database. ERROR: {str(result.failure())}")
            return False
        
        return True

    @staticmethod
    def   create_accountMdl_from_data(vm:dict):

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