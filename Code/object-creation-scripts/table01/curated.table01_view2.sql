-- DDL for table01 view2
CREATE OR REPLACE VIEW curated.table01_view2 AS
SELECT id, created_at FROM raw.table01_main WHERE name LIKE 'A%';