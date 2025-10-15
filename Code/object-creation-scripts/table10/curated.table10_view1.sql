-- DDL for table10 view1
CREATE OR REPLACE VIEW curated.table10_view1 AS
SELECT id, customer_name FROM raw.table10_main WHERE join_date > '2025-01-01';