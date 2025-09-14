CREATE OR REPLACE FUNCTION derive_columns_{table_name}(
    startts BIGINT, 
    endts BIGINT, 
    predeltams BIGINT
)
RETURNS VOID AS $$
BEGIN
    -- Tek UPDATE ile, sadece NULL olan sütunları güncelle
    UPDATE {table_name} t
    SET
        open_p            = CASE WHEN t.open_p IS NULL            THEN CASE WHEN s.open_1            = 0 THEN 1 ELSE t.open            / s.open_1            - 1 END END,
        high_p            = CASE WHEN t.high_p IS NULL            THEN CASE WHEN s.high_1            = 0 THEN 1 ELSE t.high            / s.high_1            - 1 END END,
        low_p             = CASE WHEN t.low_p IS NULL             THEN CASE WHEN s.low_1             = 0 THEN 1 ELSE t.low             / s.low_1             - 1 END END,
        close_p           = CASE WHEN t.close_p IS NULL           THEN CASE WHEN s.close_1           = 0 THEN 1 ELSE t.close           / s.close_1           - 1 END END,
        volume_p          = CASE WHEN t.volume_p IS NULL          THEN CASE WHEN s.volume_1          = 0 THEN 1 ELSE t.volume          / s.volume_1          - 1 END END,
        qav_p             = CASE WHEN t.qav_p IS NULL             THEN CASE WHEN s.qav_1             = 0 THEN 1 ELSE t.qav             / s.qav_1             - 1 END END,
        num_trades_p      = CASE WHEN t.num_trades_p IS NULL      THEN CASE WHEN s.num_trades_1      = 0 THEN 1 ELSE t.num_trades      / s.num_trades_1      - 1 END END,
        taker_base_vol_p  = CASE WHEN t.taker_base_vol_p IS NULL  THEN CASE WHEN s.taker_base_vol_1  = 0 THEN 1 ELSE t.taker_base_vol  / s.taker_base_vol_1  - 1 END END,
        taker_quoto_vol_p = CASE WHEN t.taker_quoto_vol_p IS NULL THEN CASE WHEN s.taker_quoto_vol_1 = 0 THEN 1 ELSE t.taker_quoto_vol / s.taker_quoto_vol_1 - 1 END END,
        price_p           = CASE WHEN t.price_p IS NULL           THEN CASE WHEN t.open              = 0 THEN 1 ELSE t.close           / t.open              - 1 END END,
        bigprice_p        = CASE WHEN t.bigprice_p IS NULL        THEN CASE WHEN s.open_1            = 0 THEN 1 ELSE t.close           / s.open_1            - 1 END END,
        closeopen_p       = CASE WHEN t.closeopen_p IS NULL       THEN CASE WHEN s.close_1           = 0 THEN 1 ELSE t.open            / s.close_1           - 1 END END,
        openclose_p       = CASE WHEN t.openclose_p IS NULL       THEN CASE WHEN s.open_1            = 0 THEN 1 ELSE t.close           / s.open_1            - 1 END END
    FROM (
        SELECT 
            open_time,
            LAG(open,           1) OVER (ORDER BY open_time) AS open_1,
            LAG(high,           1) OVER (ORDER BY open_time) AS high_1,
            LAG(low,            1) OVER (ORDER BY open_time) AS low_1,
            LAG(close,          1) OVER (ORDER BY open_time) AS close_1,
            LAG(volume,         1) OVER (ORDER BY open_time) AS volume_1,
            LAG(qav,            1) OVER (ORDER BY open_time) AS qav_1,
            LAG(num_trades,     1) OVER (ORDER BY open_time) AS num_trades_1,
            LAG(taker_base_vol, 1) OVER (ORDER BY open_time) AS taker_base_vol_1,
            LAG(taker_quoto_vol,1) OVER (ORDER BY open_time) AS taker_quoto_vol_1
        FROM {table_name}
        WHERE open_time BETWEEN startts - predeltams AND endts
    ) s
    WHERE t.open_time = s.open_time
      AND t.open_time >= startts;
END;
$$ LANGUAGE plpgsql;





------------------------------------------------------------------------------------------------


-- DO $$ 
-- BEGIN
--     PERFORM derive_columns(1641039000000, 1641042600000);
-- END;
-- $$;

-- -- select * FROM derive_columns( );
-- SELECT open, open_p, high_p FROM {table_name}  WHERE open_time > 1641039000000 AND open_time < 1641042600000
