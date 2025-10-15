-- DDL for table03 view1
CREATE OR REPLACE VIEW curated.table03_view1 AS
SELECT id, value FROM raw.table03_main WHERE value > 100.00;