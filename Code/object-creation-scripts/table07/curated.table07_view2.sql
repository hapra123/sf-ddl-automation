-- DDL for table07 view2
CREATE OR REPLACE VIEW curated.table07_view2 AS
SELECT id, manager FROM raw.table07_main WHERE department LIKE '%Sales%';