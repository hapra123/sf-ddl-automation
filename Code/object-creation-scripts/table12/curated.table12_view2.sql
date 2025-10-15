-- DDL for table12 view2
CREATE OR REPLACE VIEW curated.table12_view2 AS
SELECT id, hire_date FROM raw.table12_main WHERE employee_name LIKE 'C%';