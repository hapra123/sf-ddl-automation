-- DDL for table13 view2
CREATE OR REPLACE VIEW curated.table13_view2 AS
SELECT id, start_date FROM raw.table13_main WHERE project_name LIKE '%Alpha%';