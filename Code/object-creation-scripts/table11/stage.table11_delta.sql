-- DDL for table11 delta table
CREATE OR REPLACE TABLE stage.table11_delta (
    delta_id INT PRIMARY KEY,
    table11_id INT,
    change_type VARCHAR(20),
    change_date DATE
);