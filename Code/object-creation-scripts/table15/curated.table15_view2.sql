-- DDL for table15 view2
CREATE OR REPLACE VIEW curated.table15_view2 AS
SELECT id, quantity FROM raw.table15_main WHERE item_name LIKE '%Box%';