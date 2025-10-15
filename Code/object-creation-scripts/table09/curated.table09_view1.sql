-- DDL for table09 view1
CREATE OR REPLACE VIEW curated.table09_view1 AS
SELECT id, asset_name FROM raw.table09_main WHERE value > 10000.00;