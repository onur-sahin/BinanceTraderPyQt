from enum import Enum


class Q(str, Enum):
    SELECT_FUNCTION_NAMES       = "SELECT_FUNCTION_NAMES"       
    INSERT_ACCOUNT              = "INSERT_ACCOUNT"              
    UPDATE_ACCOUNT_NOTES        = "UPDATE_ACCOUNT_NOTES"                
    SELECT_OPEN_TIME            = "SELECT_OPEN_TIME"            
    SELECT_QUERY                = "SELECT_QUERY"                
    INSERT_MODEL                = "INSERT_MODEL"                
    DELETE_MODEL                = "DELETE_MODEL"                
    INSERT_NEUROL_MODEL         = "INSERT_NEUROL_MODEL"         
    UPDATE_NEUROL_MODEL         = "UPDATE_NEUROL_MODEL"         
    INSERT_KLINE                = "INSERT_KLINE"                
    CREATE_ACCOUNT_TABLE        = "CREATE_ACCOUNT_TABLE"        
    CREATE_MODEL_TABLE          = "CREATE_MODEL_TABLE"          
    CREATE_NEUROL_NETWORK_TABLE = "CREATE_NEUROL_NETWORK_TABLE" 
    CREATE_KLINE_TABLE          = "CREATE_KLINE_TABLE"          
    CREATE_TABLE_NAMES_TABLE    = "CREATE_TABLE_NAMES_TABLE"    
    INSERT_KLINE_TABLE_NAME     = "INSERT_KLINE_TABLE_NAME"     
    SELECT_KLINE_TABLE_NAMES    = "SELECT_KLINE_TABLE_NAMES"    
    DELETE_KLINE_TABLE_NAME     = "DELETE_KLINE_TABLE_NAME"     
    SELECT_RAW_ROWS             = "SELECT_RAW_ROWS"             
    SELECT_ALL_ROWS             = "SELECT_ALL_ROWS"             
    SELECT_MODEL_EXIST          = "SELECT_MODEL_EXIST"          
    SELECT_NETWORK_EXIST        = "SELECT_NETWORK_EXIST"        
    SELECT_COLUMN_NAMES         = "SELECT_COLUMN_NAMES"         
    ADD_NEW_COLUMN              = "ADD_NEW_COLUMN"              



class Queries:

    @classmethod
    def get(cls, query_name: Q) -> str:
        return cls._queries[query_name]


    _queries = {
        Q.SELECT_FUNCTION_NAMES: """
            SELECT p.proname
            FROM pg_catalog.pg_proc p
            JOIN pg_catalog.pg_namespace n ON p.pronamespace = n.oid
            WHERE n.nspname NOT IN ('pg_catalog', 'information_schema')
            AND pg_catalog.pg_function_is_visible(p.oid);
        """,

        Q.INSERT_ACCOUNT: """
            INSERT INTO tbl_accounts(account_name, real_account, account_type, api_key, api_secret, notes)
            VALUES (%(account_name)s, %(real_account)s, %(account_type)s, %(api_key)s, %(api_secret)s, %(notes)s);
        """,

        Q.UPDATE_ACCOUNT_NOTES: """
            UPDATE tbl_accounts
            SET notes = %(notes)s
            WHERE account_name=%(account_name)s
        """,

        Q.SELECT_OPEN_TIME: """
            SELECT open_time FROM {table}
            WHERE open_time BETWEEN %(startTs)s AND %(endTs)s
            ORDER BY open_time ASC;
        """,

        Q.SELECT_QUERY: """
            SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = %(table_name)s);
        """,

        Q.INSERT_MODEL: """
            INSERT INTO tbl_models (model_name, model_type, default_pair, default_interval, window_size)
            VALUES (%(model_name)s, %(model_type)s, %(default_pair)s, %(default_interval)s, %(window_size)s);
        """,

        Q.DELETE_MODEL: """
            DELETE FROM tbl_models WHERE model_name = %(model_name)s;
        """,

        Q.INSERT_NEUROL_MODEL: """
            INSERT INTO tbl_neurol_networks (model_name, network_name, bytea_object)
            VALUES (%(model_name)s, %(network_name)s, %(bytea_object)s);
        """,

        Q.UPDATE_NEUROL_MODEL: """
            UPDATE tbl_neurol_networks
            SET bytea_object = %(bytea_object)s
            WHERE model_name = %(model_name)s AND network_name = %(network_name)s;
        """,

        Q.INSERT_KLINE: """
            INSERT INTO {table} (
                open_time, open, high, low, close, volume, close_time, qav,
                num_trades, taker_base_vol, taker_quoto_vol, open_datetime
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (open_time) DO NOTHING;
        """,

        Q.CREATE_ACCOUNT_TABLE: """
            CREATE TABLE IF NOT EXISTS tbl_accounts (
                account_name VARCHAR PRIMARY KEY,
                real_account BOOLEAN NOT NULL,
                account_type VARCHAR NOT NULL,
                api_key      VARCHAR NOT NULL,
                api_secret   VARCHAR NOT NULL,
                notes        VARCHAR
            );
        """,

        Q.CREATE_MODEL_TABLE: """
            CREATE TABLE IF NOT EXISTS tbl_models (
                model_name VARCHAR PRIMARY KEY,
                model_type VARCHAR NOT NULL,
                default_pair VARCHAR NOT NULL,
                default_interval VARCHAR NOT NULL,
                window_size INTEGER NOT NULL
            );
        """,

        Q.CREATE_NEUROL_NETWORK_TABLE: """
            CREATE TABLE IF NOT EXISTS tbl_neurol_networks (
                model_name VARCHAR,
                network_name VARCHAR NOT NULL,
                bytea_object BYTEA NOT NULL,
                CONSTRAINT fk_model_name FOREIGN KEY (model_name)
                REFERENCES tbl_models (model_name)
                ON DELETE CASCADE
                ON UPDATE CASCADE
            );
        """,

        Q.CREATE_KLINE_TABLE: """
            CREATE TABLE IF NOT EXISTS {table_name} (
                open_time       BIGINT PRIMARY KEY,
                open            FLOAT4 NOT NULL,
                high            FLOAT4 NOT NULL,
                low             FLOAT4 NOT NULL,
                close           FLOAT4 NOT NULL,
                volume          FLOAT4 NOT NULL,
                close_time      BIGINT NOT NULL,
                qav             FLOAT4 NOT NULL,
                num_trades      FLOAT4 NOT NULL,
                taker_base_vol  FLOAT4 NOT NULL,
                taker_quoto_vol FLOAT4 NOT NULL,
                open_datetime   TIMESTAMPTZ NOT NULL,
                open_p            FLOAT4 DEFAULT NULL,
                high_p            FLOAT4 DEFAULT NULL,
                low_p             FLOAT4 DEFAULT NULL,
                close_p           FLOAT4 DEFAULT NULL,
                volume_p          FLOAT4 DEFAULT NULL,
                qav_p             FLOAT4 DEFAULT NULL,
                num_trades_p      FLOAT4 DEFAULT NULL,
                taker_base_vol_p  FLOAT4 DEFAULT NULL,
                taker_quoto_vol_p FLOAT4 DEFAULT NULL,
                price_p           FLOAT4 DEFAULT NULL,
                bigprice_p        FLOAT4 DEFAULT NULL,
                closeopen_p       FLOAT4 DEFAULT NULL,
                openclose_p       FLOAT4 DEFAULT NULL
            );
        """,

        Q.CREATE_TABLE_NAMES_TABLE: """
            CREATE TABLE IF NOT EXISTS tbl_kline_table_names (
                table_name VARCHAR PRIMARY KEY
            );
        """,

        Q.INSERT_KLINE_TABLE_NAME: """
            INSERT INTO tbl_kline_table_names (table_name)
            VALUES (%(table_name)s);
        """,

        Q.SELECT_KLINE_TABLE_NAMES: """
            SELECT table_name FROM tbl_kline_table_names;
        """,

        Q.DELETE_KLINE_TABLE_NAME: """
            DELETE FROM tbl_kline_table_names WHERE table_name = %(table_name)s;
        """,

        Q.SELECT_RAW_ROWS: """
            SELECT open_time, open, high, low, close, volume,
                   qav, num_trades, taker_base_vol, taker_quoto_vol
            FROM {table}
            WHERE open_time BETWEEN %(open_time_start)s AND %(open_time_end)s
            ORDER BY open_time ASC;
        """,

        Q.SELECT_ALL_ROWS: """
            SELECT open_time, open, high, low, close, volume,
                   qav, num_trades, taker_base_vol, taker_quoto_vol,
                   open_p, high_p, low_p, close_p, volume_p, qav_p,
                   num_trades_p, taker_base_vol_p, taker_quoto_vol_p,
                   price_p, bigprice_p, closeopen_p, openclose_p
            FROM {table}
            WHERE open_time BETWEEN %(open_time_start)s AND %(open_time_end)s
            ORDER BY open_time ASC;
        """,

        Q.SELECT_MODEL_EXIST: """
            SELECT EXISTS (
                SELECT 1 FROM tbl_models WHERE model_name = %(model_name)s
            );
        """,

        Q.SELECT_NETWORK_EXIST: """
            SELECT EXISTS (
                SELECT 1 FROM tbl_neurol_networks
                WHERE model_name = %(model_name)s AND network_name = %(network_name)s
            );
        """,

        Q.SELECT_COLUMN_NAMES: """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = %(table_name)s AND table_schema = 'public';
        """,

        Q.ADD_NEW_COLUMN: """
            ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type};
        """
    }


