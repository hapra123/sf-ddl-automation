-- DDL for table04 delta table
CREATE OR REPLACE TABLE stage.table04_delta (
    delta_id INT PRIMARY KEY,
    table04_id INT,
    change_type VARCHAR(20),
    change_date DATE
);