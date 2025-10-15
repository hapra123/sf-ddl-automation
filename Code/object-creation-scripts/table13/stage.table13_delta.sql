-- DDL for table13 delta table
CREATE OR REPLACE TABLE stage.table13_delta (
    delta_id INT PRIMARY KEY,
    table13_id INT,
    change_type VARCHAR(20),
    change_date DATE
);