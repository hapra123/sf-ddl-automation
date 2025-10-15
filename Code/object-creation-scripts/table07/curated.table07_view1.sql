-- DDL for table07 view1
CREATE OR REPLACE VIEW curated.table07_view1 AS
SELECT id, department FROM raw.table07_main WHERE manager = 'Alice';