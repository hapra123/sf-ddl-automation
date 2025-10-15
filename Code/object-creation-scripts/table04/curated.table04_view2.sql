-- DDL for table04 view2
CREATE OR REPLACE VIEW curated.table04_view2 AS
SELECT id, author FROM raw.table04_main WHERE title LIKE '%Guide%';