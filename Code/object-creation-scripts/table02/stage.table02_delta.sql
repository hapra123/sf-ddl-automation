-- DDL for table02 delta table
CREATE OR REPLACE TABLE stage.table02_delta (
    delta_id INT PRIMARY KEY,
    table02_id INT,
    change_type VARCHAR(20),
    change_date DATE
);