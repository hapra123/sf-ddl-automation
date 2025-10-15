-- DDL for table03 delta table
CREATE OR REPLACE TABLE stage.table03_delta (
    delta_id INT PRIMARY KEY,
    table03_id INT,
    change_type VARCHAR(20),
    change_date TIMESTAMP
);