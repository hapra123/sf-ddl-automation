-- DDL for table01 view1
CREATE OR REPLACE VIEW curated.table01_view1 AS
SELECT id, name FROM raw.table01_main WHERE created_at > '2025-01-01';