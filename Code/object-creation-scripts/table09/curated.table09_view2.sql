-- DDL for table09 view2
CREATE OR REPLACE VIEW curated.table09_view2 AS
SELECT id, value FROM raw.table09_main WHERE asset_name LIKE '%Car%';