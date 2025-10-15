-- DDL for table10 delta table
CREATE OR REPLACE TABLE stage.table10_delta (
    delta_id INT PRIMARY KEY,
    table10_id INT,
    change_type VARCHAR(20),
    change_date DATE
);