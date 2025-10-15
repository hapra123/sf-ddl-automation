-- DDL for table11 view1
CREATE OR REPLACE VIEW curated.table11_view1 AS
SELECT id, order_number FROM raw.table11_main WHERE order_date > '2025-06-01';