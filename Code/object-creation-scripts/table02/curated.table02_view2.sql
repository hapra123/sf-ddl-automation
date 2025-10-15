-- DDL for table02 view2
CREATE OR REPLACE VIEW curated.table02_view2 AS
SELECT id, status FROM raw.table02_main WHERE description LIKE '%test%';