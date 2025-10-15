-- DDL for table03 view2
CREATE OR REPLACE VIEW curated.table03_view2 AS
SELECT id, updated_at FROM raw.table03_main WHERE updated_at > '2025-01-01 00:00:00';