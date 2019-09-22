# SQL

This directory will store `.sql` files related to the project.

## Note

While `get_unique_dates.sql` uses the absolute path to copy a query to a CSV file, the follow command takes advantage of relative paths via `psql`:

```bash
\copy (SELECT DISTINCT(date) FROM matches) TO 'write_data/unique_match_dates.csv' WITH DELIMITER ',' HEADER CSV;
```
