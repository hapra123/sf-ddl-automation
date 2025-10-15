-- DDL for table14 view1
CREATE OR REPLACE VIEW curated.table14_view1 AS
SELECT id, vendor_name FROM raw.table14_main WHERE contract_date > '2025-05-01';