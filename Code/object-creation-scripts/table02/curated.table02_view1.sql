-- DDL for table02 view1
CREATE OR REPLACE VIEW curated.table02_view1 AS
SELECT id, description FROM raw.table02_main WHERE status = 'active';