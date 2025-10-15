-- DDL for table05 main table
CREATE OR REPLACE TABLE raw.table05_main (
    id INT PRIMARY KEY,
    product_name VARCHAR(120),
    price DECIMAL(8,2)
);