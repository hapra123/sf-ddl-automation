-- DDL for table10 view2
CREATE OR REPLACE VIEW curated.table10_view2 AS
SELECT id, join_date FROM raw.table10_main WHERE customer_name LIKE 'B%';