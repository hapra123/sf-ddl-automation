-- DDL for table04 view1
CREATE OR REPLACE VIEW curated.table04_view1 AS
SELECT id, title FROM raw.table04_main WHERE author = 'John Doe';