-- DDL for table08 view2
CREATE OR REPLACE VIEW curated.table08_view2 AS
SELECT id, event_date FROM raw.table08_main WHERE event_name LIKE '%Annual%';