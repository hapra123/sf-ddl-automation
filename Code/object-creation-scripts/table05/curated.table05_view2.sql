-- DDL for table05 view2
CREATE OR REPLACE VIEW curated.table05_view2 AS
SELECT id, price FROM raw.table05_main WHERE product_name LIKE '%Pro%';