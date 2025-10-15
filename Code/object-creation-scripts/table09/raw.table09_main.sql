-- DDL for table09 main table
CREATE OR REPLACE TABLE raw.table09_main (
    id INT PRIMARY KEY,
    asset_name VARCHAR(100),
    value DECIMAL(12,2)
);