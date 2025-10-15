-- DDL for table15 view1
CREATE OR REPLACE VIEW curated.table15_view1 AS
SELECT id, item_name FROM raw.table15_main WHERE quantity > 10;