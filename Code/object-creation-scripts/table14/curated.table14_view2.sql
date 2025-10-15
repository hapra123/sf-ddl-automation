-- DDL for table14 view2
CREATE OR REPLACE VIEW curated.table14_view2 AS
SELECT id, contract_date FROM raw.table14_main WHERE vendor_name LIKE 'D%';