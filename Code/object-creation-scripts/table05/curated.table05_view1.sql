-- DDL for table05 view1
CREATE OR REPLACE VIEW curated.table05_view1 AS
SELECT id, product_name FROM raw.table05_main WHERE price < 50.00;