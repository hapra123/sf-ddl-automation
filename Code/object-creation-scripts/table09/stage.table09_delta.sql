-- DDL for table09 delta table
CREATE OR REPLACE TABLE stage.table09_delta (
    delta_id INT PRIMARY KEY,
    table09_id INT,
    change_type VARCHAR(20),
    change_date DATE
);