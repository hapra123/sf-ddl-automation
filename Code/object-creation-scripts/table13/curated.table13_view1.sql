-- DDL for table13 view1
CREATE OR REPLACE VIEW curated.table13_view1 AS
SELECT id, project_name FROM raw.table13_main WHERE start_date > '2025-09-01';