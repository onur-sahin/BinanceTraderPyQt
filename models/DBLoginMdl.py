from PyQt6.QtCore import QObject, pyqtSignal, pyqtProperty, pyqtSlot, Qt
from PyQt6.QtGui import QGuiApplication
from DBManager import DBManager

class DBLoginMdl(QObject):
    databaseChanged             = pyqtSignal(str)
    userChanged                 = pyqtSignal(str)
    hostChanged                 = pyqtSignal(str)
    portChanged                 = pyqtSignal(str)
    passwordChanged             = pyqtSignal(str)
    rememberPasswordChanged     = pyqtSignal(Qt.CheckState)
    connectionTestResultChanged = pyqtSignal(str)
    connectedtoDatabase         = pyqtSignal()


    def __init__(self, parent=None):
        super().__init__(parent)
        self.dBManager = DBManager()
    

        # Initializing with default values
        self.m_database             = "binancedb"
        self.m_user                 = "postgres"
        self.m_host                 = "localhost"
        self.m_port                 = "5432"
        self.m_password             = "222222222"
        self.m_rememberPassword     = Qt.CheckState.Unchecked
        self.m_connectionTestResult = "Connection Test Result: None"

    # Properties for getter and setter
    @pyqtProperty(str, notify=databaseChanged)
    def database(self):
        return self.m_database

    @database.setter
    def database(self, database):
        if self.m_database != database:
            self.m_database = database
            print(self.m_database)
            self.databaseChanged.emit(self.m_database)

    @pyqtProperty(str, notify=userChanged)
    def user(self):
        return self.m_user

    @user.setter
    def user(self, user):
        if self.m_user != user:
            self.m_user = user
            print(self.m_user)
            self.userChanged.emit(self.m_user)

    @pyqtProperty(str, notify=hostChanged)
    def host(self):
        return self.m_host

    @host.setter
    def host(self, host):
        if self.m_host != host:
            self.m_host = host
            print(self.m_host)
            self.hostChanged.emit(self.m_host)

    @pyqtProperty(str, notify=portChanged)
    def port(self):
        return self.m_port

    @port.setter
    def port(self, port):
        if self.m_port != port:
            self.m_port = port
            print(self.m_port)
            self.portChanged.emit(self.m_port)

    @pyqtProperty(str, notify=passwordChanged)
    def password(self):
        return self.m_password

    @password.setter
    def password(self, password):
        if self.m_password != password:
            self.m_password = password
            print(self.m_password)
            self.passwordChanged.emit(self.m_password)

    @pyqtProperty(Qt.CheckState, notify=rememberPasswordChanged)
    def rememberPassword(self):
        return self.m_rememberPassword

    @rememberPassword.setter
    def rememberPassword(self, rememberPassword):
        if self.m_rememberPassword != rememberPassword:
            self.m_rememberPassword = rememberPassword
            if rememberPassword == Qt.CheckState.PartiallyChecked:
                self.m_rememberPassword = Qt.CheckState.Checked
            self.rememberPasswordChanged.emit(self.m_rememberPassword)
            print(self.m_rememberPassword)

    @pyqtProperty(str, notify=connectionTestResultChanged)
    def connectionTestResult(self):
        return self.m_connectionTestResult

    @connectionTestResult.setter
    def connectionTestResult(self, connectionTestResult):
        self.m_connectionTestResult = connectionTestResult
        self.connectionTestResultChanged.emit(str(self.m_connectionTestResult))
        print(self.m_connectionTestResult)
    
    @pyqtSlot(result=bool)
    def test_database_connection(self):
        print("QPA platform:", QGuiApplication.platformName())
        try:
            self.dBManager.test_database_connection(self.m_database, self.m_user, self.m_password,
                                                    self.m_host, self.m_port)
            self.update_connection_test_result("Connection Test Result: Successfully")
            return True

        except Exception as e:

            msg = f"Error in DBLoginMdl::test_database_connection(): {e}"
            self.update_connection_test_result(msg)
            return False



    def update_connection_test_result(self, msg):
        self.connectionTestResult = msg

    @pyqtSlot(result=bool)
    def initialize_database(self):
        return self.dBManager.initialize_database()


# Usage example
if __name__ == "__main__":
    db_login_model = DBLoginMdl()

    db_login_model.database = "new_database"
    db_login_model.test_database_connection()
    db_login_model.initialize_database()
