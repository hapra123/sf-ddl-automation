-- DDL for table05 delta table
CREATE OR REPLACE TABLE stage.table05_delta (
    delta_id INT PRIMARY KEY,
    table05_id INT,
    change_type VARCHAR(20),
    change_date DATE
);