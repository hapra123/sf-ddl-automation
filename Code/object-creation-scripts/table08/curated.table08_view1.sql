-- DDL for table08 view1
CREATE OR REPLACE VIEW curated.table08_view1 AS
SELECT id, event_name FROM raw.table08_main WHERE event_date > '2025-10-01';