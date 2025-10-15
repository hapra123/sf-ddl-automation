-- DDL for table15 delta table
CREATE OR REPLACE TABLE stage.table15_delta (
    delta_id INT PRIMARY KEY,
    table15_id INT,
    change_type VARCHAR(20),
    change_date DATE
);