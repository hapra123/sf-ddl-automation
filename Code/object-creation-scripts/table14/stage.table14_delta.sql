-- DDL for table14 delta table
CREATE OR REPLACE TABLE stage.table14_delta (
    delta_id INT PRIMARY KEY,
    table14_id INT,
    change_type VARCHAR(20),
    change_date DATE
);