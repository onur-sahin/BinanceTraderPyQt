import psycopg2
import threading
from psycopg2.extensions import connection

class DBManager:
    _instance = None
    _lock = threading.Lock()
    _thread_local = threading.local()  # Thread-local storage (her thread için bağımsız veriler)

    @classmethod
    def get_instance(cls) -> 'DBManager':

        if cls._instance is None:
            raise Exception("DBManager instance has not been created yet.")
        return cls._instance


    def __new__(cls, dbname: str=None, user: str=None, password: str=None, host: str=None, port: str=None):

        with cls._lock:
            if cls._instance is None:
                cls._instance = super(DBManager, cls).__new__(cls)
                # cls._instance.__init__(dbname, user, password, host, port) // __init__ is called automatically after __new__ completes, provided that __new__ returns an instance of cls.
        return cls._instance


    def __init__(self, dbname: str=None, user: str=None, password: str=None, host: str=None, port: str=None):

        """Initialize sadece bir kez yapılmalı"""
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self.dbname   = dbname
            self.user     = user
            self.password = password
            self.host     = host
            self.port     = port
            self.conn     = None


    def connect(self, dbname: str, user: str, password: str, host: str, port: str) -> None:
        """Veritabanına bağlanır."""

        self.dbname   = dbname
        self.user     = user
        self.password = password
        self.host     = host
        self.port     = port

        try:
            self.conn = psycopg2.connect( dbname   = self.dbname,
                                          user     = self.user,
                                          password = self.password,
                                          host     = self.host,
                                          port     = self.port)
            
        except Exception as e:
            raise psycopg2.DatabaseError(f"Failed to connect to database: {e} ") from e


    def get_connection(self) -> connection:
        """Thread-local verileri kullanarak her thread için bağımsız bağlantı sağlar."""

        if not hasattr(self._thread_local, 'conn') or self._thread_local.conn.closed:
            # Eğer thread-local storage'da bağlantı yoksa ya da bağlantı kapalıysa, yeni bir bağlantı kur
            self._thread_local.conn = psycopg2.connect(dbname  = self.dbname,
                                                      user     = self.user,
                                                      password = self.password,
                                                      host     = self.host,
                                                      port     = self.port)
        return self._thread_local.conn


    def cleanup(self):
        """Tüm kaynakları serbest bırakır ve bağlantıyı kapatır."""
        if hasattr(self._thread_local, 'conn'):
            try:
                if self._thread_local.conn is not None and not self._thread_local.conn.closed:
                    self._thread_local.conn.close()
            except Exception as e:
                print(f"Error while closing the connection: {e}")
        # Herhangi bir ekstra kaynak serbest bırakma işlemleri burada yapılabilir.


    def test_database_connection(self, dbname: str, user: str, password: str, host: str, port: str):
        
        self.connect(dbname, user,password, host, port)


    def execute_select( self, query: str, bindValues:dict|None = None ) -> list:

        result = list()

        try:
            conn   = self.get_connection()
            cursor = conn.cursor()

            if(bindValues is None):
                cursor.execute(query)
            else:
                cursor.execute(query, bindValues)
            
            result = cursor.fetchall()
            cursor.close()

        except Exception as e:
            raise psycopg2.DatabaseError("Failed to execute select query: ") from e

        return result


    def execute(self, query:str, bindValues:dict|None) -> None:

        try:
            conn   = self.get_connection()
            cursor = conn.cursor()

            if(bindValues is None):
                cursor.execute(query)
            else:
                cursor.execute(query, bindValues)

            cursor.close()

        except Exception as e:
            raise psycopg2.DatabaseError("Failed to execute query") from e




if __name__ == "__main__":
    pass
