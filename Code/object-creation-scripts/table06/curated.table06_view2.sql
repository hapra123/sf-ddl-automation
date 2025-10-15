-- DDL for table06 view2
CREATE OR REPLACE VIEW curated.table06_view2 AS
SELECT id, population FROM raw.table06_main WHERE city LIKE 'New%';