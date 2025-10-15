-- DDL for table01 delta table
CREATE OR REPLACE TABLE stage.table01_delta (
    delta_id INT PRIMARY KEY,
    table01_id INT,
    change_type VARCHAR(20),
    change_date DATE
);