

CREATE OR REPLACE FUNCTION derive_columns_{table_name}(
    startts BIGINT, 
    endts BIGINT, 
    predeltams BIGINT
)
RETURNS VOID AS $$
BEGIN
    -- Tek sorguda tüm _p sütunlarını güncelle
    UPDATE {table_name} t
    SET
        open_p           = CASE WHEN s.open_1           = 0 THEN 1 ELSE t.open / s.open_1           - 1 END,
        high_p           = CASE WHEN s.high_1           = 0 THEN 1 ELSE t.high / s.high_1           - 1 END,
        low_p            = CASE WHEN s.low_1            = 0 THEN 1 ELSE t.low / s.low_1             - 1 END,
        close_p          = CASE WHEN s.close_1          = 0 THEN 1 ELSE t.close / s.close_1         - 1 END,
        volume_p         = CASE WHEN s.volume_1         = 0 THEN 1 ELSE t.volume / s.volume_1       - 1 END,
        qav_p            = CASE WHEN s.qav_1            = 0 THEN 1 ELSE t.qav / s.qav_1             - 1 END,
        num_trades_p     = CASE WHEN s.num_trades_1     = 0 THEN 1 ELSE t.num_trades / s.num_trades_1 - 1 END,
        taker_base_vol_p = CASE WHEN s.taker_base_vol_1 = 0 THEN 1 ELSE t.taker_base_vol / s.taker_base_vol_1 - 1 END,
        taker_quoto_vol_p= CASE WHEN s.taker_quoto_vol_1= 0 THEN 1 ELSE t.taker_quoto_vol / s.taker_quoto_vol_1 - 1 END,
        price_p          = CASE WHEN t.open            = 0 THEN 1 ELSE t.close / t.open                  - 1 END,
        bigprice_p       = CASE WHEN s.open_1          = 0 THEN 1 ELSE t.close / s.open_1               - 1 END,
        closeopen_p      = CASE WHEN s.close_1         = 0 THEN 1 ELSE t.open / s.close_1              - 1 END,
        openclose_p      = CASE WHEN s.open_1          = 0 THEN 1 ELSE t.close / s.open_1              - 1 END
    FROM (
        SELECT 
            open_time,
            LAG(open, 1)           OVER (ORDER BY open_time) AS open_1,
            LAG(high, 1)           OVER (ORDER BY open_time) AS high_1,
            LAG(low, 1)            OVER (ORDER BY open_time) AS low_1,
            LAG(close, 1)          OVER (ORDER BY open_time) AS close_1,
            LAG(volume, 1)         OVER (ORDER BY open_time) AS volume_1,
            LAG(qav, 1)            OVER (ORDER BY open_time) AS qav_1,
            LAG(num_trades, 1)     OVER (ORDER BY open_time) AS num_trades_1,
            LAG(taker_base_vol,1)  OVER (ORDER BY open_time) AS taker_base_vol_1,
            LAG(taker_quoto_vol,1) OVER (ORDER BY open_time) AS taker_quoto_vol_1
        FROM {table_name}
        WHERE open_time BETWEEN startts - predeltams AND endts
    ) s
    WHERE t.open_time = s.open_time
      AND t.open_time >= startts
      AND (
          t.open_p IS NULL OR t.high_p IS NULL OR t.low_p IS NULL OR t.close_p IS NULL OR
          t.volume_p IS NULL OR t.qav_p IS NULL OR t.num_trades_p IS NULL OR
          t.taker_base_vol_p IS NULL OR t.taker_quoto_vol_p IS NULL OR
          t.price_p IS NULL OR t.bigprice_p IS NULL OR t.closeopen_p IS NULL OR t.openclose_p IS NULL
      );
END;
$$ LANGUAGE plpgsql;







CREATE OR REPLACE FUNCTION derive_columns_{table_name}(startts BIGINT, endts BIGINT, predeltams BIGINT)
RETURNS VOID AS $$ 
BEGIN

-- LAG fonksiyonuyla önceki satırın B değerini alıp C sütununu güncelle
-- WITH tmp_table AS (
--     SELECT 
--         open_time,
--         LAG(open           , 0) OVER (ORDER BY open_time) AS open_0           ,
--         LAG(open           , 1) OVER (ORDER BY open_time) AS open_1           
--     FROM {table_name}
--     WHERE open_time >= startts-predeltams AND open_time <= endts
--     )
--     UPDATE {table_name}
--     SET open_p =           
--             CASE WHEN tmp_table.open_1 = 0 THEN 1
--                 ELSE tmp_table.open_0 / tmp_table.open_1 - 1
--             END
--     FROM tmp_table
--     WHERE {table_name}.open_time = tmp_table.open_time
--         AND {table_name}.open_p IS NULL
--         AND tmp_table.open_1 IS NOT NULL
--         AND {table_name}.open_time>=startts;

UPDATE {table_name} t
SET open_p = CASE 
                WHEN s.open_1 = 0 THEN 1
                ELSE t.open / s.open_1 - 1
             END
FROM (
    SELECT 
        open_time,
        LAG(open, 1) OVER (ORDER BY open_time) AS open_1
    FROM {table_name}
    WHERE open_time BETWEEN startts - predeltams AND endts
) s
WHERE t.open_time = s.open_time
  AND t.open_p IS NULL
  AND s.open_1 IS NOT NULL
  AND t.open_time >= startts;

------------------------------------------------------------------------------------------

-- WITH tmp_table AS (
--     SELECT 
--         open_time,
--         LAG(high           , 0) OVER (ORDER BY open_time) AS high_0           ,
--         LAG(high           , 1) OVER (ORDER BY open_time) AS high_1           
--     FROM {table_name}
--     WHERE open_time >= startts-predeltams AND open_time <= endts
--     )
--     UPDATE {table_name}
--     SET high_p =      CASE WHEN tmp_table.high_1 = 0 THEN 1
--                         ELSE tmp_table.high_0 / tmp_table.high_1 - 1
--                     END
--     FROM tmp_table
--     WHERE {table_name}.open_time = tmp_table.open_time
--         AND {table_name}.high_p IS NULL
--         AND tmp_table.high_1 IS NOT NULL
--         AND {table_name}.open_time>=startts;

UPDATE {table_name} t
SET high_p = CASE 
                WHEN s.high_1 = 0 THEN 1
                ELSE t.high / s.high_1 - 1
             END
FROM (
    SELECT 
        open_time,
        LAG(high, 1) OVER (ORDER BY open_time) AS high_1
    FROM {table_name}
    WHERE open_time BETWEEN startts - predeltams AND endts
) s
WHERE t.open_time = s.open_time
  AND t.high_p IS NULL
  AND s.high_1 IS NOT NULL
  AND t.open_time >= startts;


------------------------------------------------------------------------------------------

-- WITH tmp_table AS (
--     SELECT 
--         open_time,
--         LAG(low            , 0) OVER (ORDER BY open_time) AS low_0            ,
--         LAG(low            , 1) OVER (ORDER BY open_time) AS low_1            
--     FROM {table_name}
--     WHERE open_time >= startts-predeltams AND open_time <= endts
--     )
--     UPDATE {table_name}
--     SET low_p =         CASE WHEN tmp_table.low_1 = 0 THEN 1
--                               ELSE tmp_table.low_0 / tmp_table.low_1 - 1
--                         END
--     FROM tmp_table
--     WHERE {table_name}.open_time = tmp_table.open_time
--         AND {table_name}.low_p IS NULL
--         AND tmp_table.low_1 IS NOT NULL
--         AND {table_name}.open_time>=startts;

UPDATE {table_name} t
SET low_p = CASE 
                WHEN s.low_1 = 0 THEN 1
                ELSE t.low / s.low_1 - 1
            END
FROM (
    SELECT 
        open_time,
        LAG(low, 1) OVER (ORDER BY open_time) AS low_1
    FROM {table_name}
    WHERE open_time BETWEEN startts - predeltams AND endts
) s
WHERE t.open_time = s.open_time
  AND t.low_p IS NULL
  AND s.low_1 IS NOT NULL
  AND t.open_time >= startts;


------------------------------------------------------------------------------------------

-- WITH tmp_table AS (
--     SELECT 
--         open_time,
--         LAG(close          , 0) OVER (ORDER BY open_time) AS close_0          ,
--         LAG(close          , 1) OVER (ORDER BY open_time) AS close_1          
--     FROM {table_name}
--     WHERE open_time >= startts-predeltams AND open_time <= endts
--     )
--     UPDATE {table_name}
--     SET close_p =       CASE WHEN tmp_table.close_1 = 0 THEN 1
--                             ELSE tmp_table.close_0 / tmp_table.close_1 - 1
--                         END
--     FROM tmp_table
--     WHERE {table_name}.open_time = tmp_table.open_time
--         AND {table_name}.close_p IS NULL
--         AND tmp_table.close_1 IS NOT NULL
--         AND {table_name}.open_time>=startts;

UPDATE {table_name} t
SET close_p = CASE 
                 WHEN s.close_1 = 0 THEN 1
                 ELSE t.close / s.close_1 - 1
              END
FROM (
    SELECT 
        open_time,
        LAG(close, 1) OVER (ORDER BY open_time) AS close_1
    FROM {table_name}
    WHERE open_time BETWEEN startts - predeltams AND endts
) s
WHERE t.open_time = s.open_time
  AND t.close_p IS NULL
  AND s.close_1 IS NOT NULL
  AND t.open_time >= startts;


------------------------------------------------------------------------------------------

-- WITH tmp_table AS (
--     SELECT 
--         open_time,
--         LAG(volume         , 0) OVER (ORDER BY open_time) AS volume_0         ,
--         LAG(volume         , 1) OVER (ORDER BY open_time) AS volume_1         
    
--     FROM {table_name}
--     WHERE open_time >= startts-predeltams AND open_time <= endts
--     )
--     UPDATE {table_name}
--     SET volume_p =      CASE WHEN tmp_table.volume_1 = 0 THEN 1
--                             ELSE tmp_table.volume_0 / tmp_table.volume_1 - 1
--                         END
--     FROM tmp_table
--     WHERE {table_name}.open_time = tmp_table.open_time
--         AND {table_name}.volume_p IS NULL
--         AND tmp_table.volume_1 IS NOT NULL
--         AND {table_name}.open_time>=startts;

UPDATE {table_name} t
SET volume_p = CASE 
                  WHEN s.volume_1 = 0 THEN 1
                  ELSE t.volume / s.volume_1 - 1
               END
FROM (
    SELECT 
        open_time,
        LAG(volume, 1) OVER (ORDER BY open_time) AS volume_1
    FROM {table_name}
    WHERE open_time BETWEEN startts - predeltams AND endts
) s
WHERE t.open_time = s.open_time
  AND t.volume_p IS NULL
  AND s.volume_1 IS NOT NULL
  AND t.open_time >= startts;


------------------------------------------------------------------------------------------

-- WITH tmp_table AS (
--     SELECT 
--         open_time,
--         LAG(qav            , 0) OVER (ORDER BY open_time) AS qav_0            ,
--         LAG(qav            , 1) OVER (ORDER BY open_time) AS qav_1            
--     FROM {table_name}
--     WHERE open_time >= startts-predeltams AND open_time <= endts
--     )
--     UPDATE {table_name}
--     SET qav_p =         CASE WHEN tmp_table.qav_1 = 0 THEN 1
--                             ELSE tmp_table.qav_0 / tmp_table.qav_1 - 1
--                         END
--     FROM tmp_table
--     WHERE {table_name}.open_time = tmp_table.open_time
--         AND {table_name}.qav_p IS NULL
--         AND tmp_table.qav_1 IS NOT NULL
--         AND {table_name}.open_time>=startts;

UPDATE {table_name} t
SET qav_p = CASE 
                WHEN s.qav_1 = 0 THEN 1
                ELSE t.qav / s.qav_1 - 1
            END
FROM (
    SELECT 
        open_time,
        LAG(qav, 1) OVER (ORDER BY open_time) AS qav_1
    FROM {table_name}
    WHERE open_time BETWEEN startts - predeltams AND endts
) s
WHERE t.open_time = s.open_time
  AND t.qav_p IS NULL
  AND s.qav_1 IS NOT NULL
  AND t.open_time >= startts;


------------------------------------------------------------------------------------------

WITH tmp_table AS (
    SELECT 
        open_time,
        LAG(num_trades     , 0) OVER (ORDER BY open_time) AS num_trades_0     ,
        LAG(num_trades     , 1) OVER (ORDER BY open_time) AS num_trades_1     
    FROM {table_name}
    WHERE open_time >= startts-predeltams AND open_time <= endts
    )
    UPDATE {table_name}
    SET num_trades_p =      CASE WHEN tmp_table.num_trades_1 = 0 THEN 1
                                ELSE tmp_table.num_trades_0 / tmp_table.num_trades_1 - 1
                            END
    FROM tmp_table
    WHERE {table_name}.open_time = tmp_table.open_time
        AND {table_name}.num_trades_p IS NULL
        AND tmp_table.num_trades_1 IS NOT NULL
        AND {table_name}.open_time>=startts;

------------------------------------------------------------------------------------------

WITH tmp_table AS (
    SELECT 
        open_time,
        LAG(taker_base_vol , 0) OVER (ORDER BY open_time) AS taker_base_vol_0 ,
        LAG(taker_base_vol , 1) OVER (ORDER BY open_time) AS taker_base_vol_1 
    FROM {table_name}
    WHERE open_time >= startts-predeltams AND open_time <= endts
    )
    UPDATE {table_name}
    SET taker_base_vol_p =  CASE WHEN tmp_table.taker_base_vol_1 = 0 THEN 1
                                ELSE tmp_table.taker_base_vol_0 / tmp_table.taker_base_vol_1 - 1
                            END
    FROM tmp_table
    WHERE {table_name}.open_time = tmp_table.open_time
        AND {table_name}.taker_base_vol_p IS NULL
        AND tmp_table.taker_base_vol_1 IS NOT NULL
        AND {table_name}.open_time>=startts;

------------------------------------------------------------------------------------------

WITH tmp_table AS (
    SELECT 
        open_time,
        LAG(taker_quoto_vol, 0) OVER (ORDER BY open_time) AS taker_quoto_vol_0,
        LAG(taker_quoto_vol, 1) OVER (ORDER BY open_time) AS taker_quoto_vol_1
    FROM {table_name}
    WHERE open_time >= startts-predeltams AND open_time <= endts
    )
    UPDATE {table_name}
    SET taker_quoto_vol_p = CASE WHEN tmp_table.taker_quoto_vol_1 = 0 THEN 1
                                ELSE tmp_table.taker_quoto_vol_0 / tmp_table.taker_quoto_vol_1 - 1
                            END
    FROM tmp_table
    WHERE {table_name}.open_time = tmp_table.open_time
        AND {table_name}.taker_quoto_vol_p IS NULL
        AND tmp_table.taker_quoto_vol_1 IS NOT NULL
        AND {table_name}.open_time>=startts;

------------------------------------------------------------------------------------------

WITH tmp_table AS (
    SELECT 
        open_time,
        LAG(open           , 0) OVER (ORDER BY open_time) AS open_0           ,
        LAG(close          , 0) OVER (ORDER BY open_time) AS close_0          
    FROM {table_name}
    WHERE open_time >= startts-predeltams AND open_time <= endts
    )
    UPDATE {table_name}
    SET price_p  =      CASE WHEN tmp_table.open_0 = 0  THEN 1
                            ELSE tmp_table.close_0 / tmp_table.open_0 - 1
                        END
    FROM tmp_table
    WHERE {table_name}.open_time = tmp_table.open_time
        AND {table_name}.price_p IS NULL
        AND tmp_table.open_0 IS NOT NULL
        AND {table_name}.open_time>=startts;

------------------------------------------------------------------------------------------

WITH tmp_table AS (
    SELECT 
        open_time,
        LAG(close          , 0) OVER (ORDER BY open_time) AS close_0          ,
        LAG(open           , 1) OVER (ORDER BY open_time) AS open_1           
    FROM {table_name}
    WHERE open_time >= startts-predeltams AND open_time <= endts
    )
    UPDATE {table_name}
    SET bigprice_p =        CASE WHEN tmp_table.open_1 = 0 THEN 1
                                ELSE tmp_table.close_0 / tmp_table.open_1 - 1
                            END
    FROM tmp_table
    WHERE {table_name}.open_time = tmp_table.open_time
        AND {table_name}.bigprice_p IS NULL
        AND tmp_table.open_1 IS NOT NULL
        AND {table_name}.open_time>=startts;

------------------------------------------------------------------------------------------

WITH tmp_table AS (
    SELECT 
        open_time,
        LAG(open           , 0) OVER (ORDER BY open_time) AS open_0           ,
        LAG(close          , 1) OVER (ORDER BY open_time) AS close_1          
    FROM {table_name}
    WHERE open_time >= startts-predeltams AND open_time <= endts
    )
    UPDATE {table_name}
    SET closeopen_p =       CASE WHEN tmp_table.close_1 = 0     THEN 1
                                ELSE tmp_table.open_0 / tmp_table.close_1 - 1
                            END
    FROM tmp_table
    WHERE {table_name}.open_time = tmp_table.open_time
        AND {table_name}.closeopen_p IS NULL
        AND tmp_table.close_1 IS NOT NULL
        AND {table_name}.open_time>=startts;

------------------------------------------------------------------------------------------

WITH tmp_table AS (
    SELECT 
        open_time,
        LAG(open           , 1) OVER (ORDER BY open_time) AS open_1           ,
        LAG(close          , 0) OVER (ORDER BY open_time) AS close_0          
    FROM {table_name}
    WHERE open_time >= startts-predeltams AND open_time <= endts
    )
    UPDATE {table_name}
    SET openclose_p =       CASE WHEN tmp_table.close_0 = 0 THEN 1
                                ELSE tmp_table.close_0 / tmp_table.open_1 - 1
                            END
    FROM tmp_table
    WHERE {table_name}.open_time = tmp_table.open_time
        AND {table_name}.openclose_p IS NULL
        AND tmp_table.open_1 IS NOT NULL
        AND {table_name}.open_time>=startts;


------------------------------------------------------------------------------------------

END;


$$ LANGUAGE plpgsql;

-- DO $$ 
-- BEGIN
--     PERFORM derive_columns(1641039000000, 1641042600000);
-- END;
-- $$;

-- -- select * FROM derive_columns( );
-- SELECT open, open_p, high_p FROM {table_name}  WHERE open_time > 1641039000000 AND open_time < 1641042600000
