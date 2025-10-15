-- DDL for table07 delta table
CREATE OR REPLACE TABLE stage.table07_delta (
    delta_id INT PRIMARY KEY,
    table07_id INT,
    change_type VARCHAR(20),
    change_date DATE
);