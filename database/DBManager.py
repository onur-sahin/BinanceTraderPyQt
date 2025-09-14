import psycopg2
import threading
from psycopg2.extensions import connection
import traceback
import subprocess
import os
from returns.result import Result, Success, Failure
from Queries import Queries, Q
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
            self.dbname       = dbname
            self.user         = user
            self.password     = password
            self.host         = host
            self.port         = port

    def connect(self, dbname: str, user: str, password: str, host: str, port: str) -> None:
        """Veritabanına bağlanır."""

        self.dbname   = dbname
        self.user     = user
        self.password = password
        self.host     = host
        self.port     = port

        try:
            psycopg2.connect( dbname   = self.dbname,
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
    
    def commit_connection(self, conn) -> str:
        """Verilen bağlantıda commit yapar. 
        Başarılı olursa boş string döner, hata varsa açıklama mesajı döner."""

        try:
            conn.commit()
            return ""  # Başarılı
        except Exception as commit_error:
            # Commit başarısız, rollback deneyelim
            try:
                conn.rollback()
            except Exception as rollback_error:
                return f"Commit failed: {commit_error}. Additionally, rollback failed: {rollback_error}"
            return f"Commit failed: {commit_error}"

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

        installation_expected = self.check_postgresql_installation()
        
        if installation_expected != "":  # hata mesajı döndü
            msg =f"Error in check_postgresql_installation(): {installation_expected}"
            print( msg )
            raise RuntimeError(msg)
        
        self.connect(dbname, user,password, host, port)

    def execute_select_return_list( self, query: str, bindValues:dict|None = None ) -> Result[list, Exception]:

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

        except psycopg2.Error as e:

            if conn:
                conn.rollback()
            return Failure(e)

        except Exception as e:
            return Failure(e)
        
        finally:
            if cursor:
                cursor.close()

        return Success(result)
    
    def execute_select_return_dict( self, query: str, bindValues:dict|None = None ) -> Result[list, Exception]:

        result = list()

        try:
            conn   = self.get_connection()
            cursor = conn.cursor()

            if(bindValues is None):
                cursor.execute(query)
            else:
                cursor.execute(query, bindValues)

            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()

            for row in rows:
                result.append(dict(zip(columns, row)))

            cursor.close()

        except psycopg2.Error as e:

            if conn:
                conn.rollback()
                return Failure(e)
        
            return Failure(e)

        except Exception as e:
            return Failure(e)
        
        finally:
            if cursor:
                cursor.close()

        return Success(result)

    def execute(self, query:str, bindValues:dict|None = None, conn:connection=None, commit:bool=True) -> Result[None, Exception]:

        try:
            if conn == None:
                conn  = self.get_connection()
            cursor = conn.cursor()

            if(bindValues is None):
                cursor.execute(query)
            else:
                cursor.execute(query, bindValues)

            if commit:
                conn.commit()

            cursor.close()

            return Success(None)

        except psycopg2.Error as e:

            if conn:
                conn.rollback()
                return Failure(e)
        
            return Failure(e)

        except Exception as e:
            return Failure(e)
        
        finally:
            if cursor:
                cursor.close()

    def initialize_database(self) -> bool:

        ensure_tables_expected = self.ensure_tables_exists()
        if ensure_tables_expected != "":
            print(f"Error in ensure_tables_exists(): {ensure_tables_expected}")
            return False

        update_functions_expected = self.update_tbl_functions(None)
        if update_functions_expected != "":
            print(f"Error in update_tbl_functions(): {update_functions_expected}")
            return False

        print("Database successfully initialized")
        return True

    def check_postgresql_installation(self)->str:
        # Çalışma dizininden bash script çalıştırılıyor

        script_path = "./share/check_postgresql_installation.sh"
        try:
            result = subprocess.run([script_path], check=False)
        except Exception as e:
            return f"Exception running script: {e}"

        exit_code = result.returncode

        if exit_code == 0:
            print("Postgresql is available")
            return ""  # Başarılı, hata yok
        elif exit_code == 127:
            return f"File not found: {script_path} Error Code: {exit_code}"
        else:
            return f"Error executing bash script. Error Code: {exit_code} from: {script_path}"

    def ensure_tables_exists(self)->str:
        # Burada execute_dml_dql_query ve execute_ddl_dcl_tcl_query fonksiyonları
        # DB sorguları çalıştıran fonksiyonlar olarak kabul ediliyor.
        # Bunlar hata durumunda string, başarılı durumda None döndürüyor.

        db = DBManager.get_instance()

        table_names = {"tbl_accounts"         :Queries.get(Q.CREATE_ACCOUNT_TABLE       ),
                       "tbl_models"           :Queries.get(Q.CREATE_MODEL_TABLE         ),
                       "tbl_neurol_networks"  :Queries.get(Q.CREATE_NEUROL_NETWORK_TABLE),
                       "tbl_kline_table_names":Queries.get(Q.CREATE_TABLE_NAMES_TABLE   )           
                      }


        for table_name, createQueryStr in table_names.items():
            query_result = db.execute_select_return_list(Queries.get(Q.SELECT_TABLE_EXISTS), {"table_name": table_name})

            if isinstance(query_result, Failure):
                return f"Error in ensure_tables_exists() for {table_name}: {query_result},\n{self.format_error(query_result.failure())}"
            
            if len ( query_result.unwrap() ) < 1:
                result = db.execute(createQueryStr)

                if isinstance(result, Failure):
                    msg = db.format_error(result)
                    print(msg)
                    return msg


        return ""  # Başarı

    def update_tbl_functions(self, name):
        if name is None:
            table_names_result = self.execute_select_return_list(Queries.get(Q.SELECT_KLINE_TABLE_NAMES))
            if isinstance(table_names_result, Failure):
                return f"Error getting kline table names in update_tbl_functions(): {table_names_result.failure()}"
            table_names = table_names_result.unwrap()
        else:
            table_names = [{"table_name": name}]

        count = 0
        create_function_query_result = self.read_fnc_derive_columns()
        if isinstance(create_function_query_result, Failure):
            return f"Error getting query from sql file in update_tbl_functions(): {create_function_query_result.failure()}"
        
        for table_name in table_names:
            table_name = table_name[0]
            create_function_query = create_function_query_result.unwrap().format(table_name=table_name)


            create_result = self.execute(create_function_query)
            if isinstance(create_result, Failure):
                return f"Error creating function on database in update_tbl_functions():\n{self.format_error(create_result.failure())}"

        return ""

    def read_fnc_derive_columns(self)->Result[str, Exception]:
        file_path = os.path.join(os.getcwd(), "./share/derive_columns.sql")
        
        if not os.path.exists(file_path):
            return Failure( FileNotFoundError(f"File not found: {file_path}") )

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                sql_query = file.read()
            return Success( sql_query)
        except Exception as e:
            return Failure(e)

    def drive_columns(self, table_name, startTs, endTs, preDeltaMs):
        result = self.execute(  Queries.get(Q.SELECT_DRIVE_COLUMNS),
                                {"table_name": table_name,
                                "startTs"   : startTs,
                                "endTs"     : endTs,
                                "preDeltaMs": preDeltaMs}
                             )
        
        if isinstance(result, Failure):
            return result.failure()

    def format_error(error: Exception) -> str:
        """
        Hata tipine göre en kapsamlı detayları string olarak döndürür.
        - psycopg2.Error için: pgerror, pgcode, diag detayları
        - Diğer Exception için: args, message, cause, context
        - Her durumda traceback eklenir
        """
        details = []

        # Hata tipi
        details.append(f"[TYPE] {type(error).__name__}")

        if isinstance(error, psycopg2.Error):
            # PostgreSQL hata mesajı
            if getattr(error, 'pgerror', None):
                details.append(f"[PGERROR] {error.pgerror.strip()}")
            if getattr(error, 'pgcode', None):
                details.append(f"[PGCODE] {error.pgcode}")

            # Diagnostic detayları
            if hasattr(error, 'diag'):
                diag = error.diag
                diag_details = {
                    "Primary": getattr(diag, 'message_primary', None),
                    "Detail": getattr(diag, 'message_detail', None),
                    "Hint": getattr(diag, 'message_hint', None),
                    "Schema": getattr(diag, 'schema_name', None),
                    "Table": getattr(diag, 'table_name', None),
                    "Constraint": getattr(diag, 'constraint_name', None),
                    "Position": getattr(diag, 'statement_position', None),
                }
                for key, value in diag_details.items():
                    if value:
                        details.append(f"[{key}] {value}")
        else:
            # Genel Python Exception
            if error.args:
                details.append(f"[ARGS] {error.args}")
            details.append(f"[MESSAGE] {str(error)}")

        # Zincirleme hata bilgileri
        if getattr(error, '__cause__', None):
            details.append(f"[CAUSE] {repr(error.__cause__)}")
        if getattr(error, '__context__', None):
            details.append(f"[CONTEXT] {repr(error.__context__)}")

        # Traceback
        tb = ''.join(traceback.format_exception(type(error), error, error.__traceback__))
        if tb:
            details.append("[TRACEBACK]\n" + tb.strip())

        return "\n".join(details)





if __name__ == "__main__":
    pass
