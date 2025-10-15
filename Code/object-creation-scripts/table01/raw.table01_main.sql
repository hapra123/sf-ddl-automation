-- DDL for table01 main table
CREATE OR REPLACE TABLE raw.table01_main (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    created_at DATE
);

create or replace view curated.hardik_view as
select * from raw.table01_main;