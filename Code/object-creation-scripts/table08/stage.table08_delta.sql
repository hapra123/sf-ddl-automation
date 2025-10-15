-- DDL for table08 delta table
CREATE OR REPLACE TABLE stage.table08_delta (
    delta_id INT PRIMARY KEY,
    table08_id INT,
    change_type VARCHAR(20),
    change_date DATE
);