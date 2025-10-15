-- DDL for table12 view1
CREATE OR REPLACE VIEW curated.table12_view1 AS
SELECT id, employee_name FROM raw.table12_main WHERE hire_date > '2025-03-01';