-- DDL for table11 view2
CREATE OR REPLACE VIEW curated.table11_view2 AS
SELECT id, order_date FROM raw.table11_main WHERE order_number LIKE 'ORD%';