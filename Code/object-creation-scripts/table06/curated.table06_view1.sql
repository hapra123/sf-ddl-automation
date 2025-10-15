-- DDL for table06 view1
CREATE OR REPLACE VIEW curated.table06_view1 AS
SELECT id, city FROM raw.table06_main WHERE population > 1000000;