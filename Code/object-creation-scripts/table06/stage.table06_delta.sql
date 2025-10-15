-- DDL for table06 delta table
CREATE OR REPLACE TABLE stage.table06_delta (
    delta_id INT PRIMARY KEY,
    table06_id INT,
    change_type VARCHAR(20),
    change_date DATE
);