-- DDL for table12 delta table
CREATE OR REPLACE TABLE stage.table12_delta (
    delta_id INT PRIMARY KEY,
    table12_id INT,
    change_type VARCHAR(20),
    change_date DATE
);