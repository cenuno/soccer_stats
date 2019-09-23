/*
convert string to date and then date to epoch integer date format
for the 2011 season
and store it in a new table
*/

CREATE TABLE unique_2011_dates 
AS (
    SELECT dates.season,
           dates.actual_date AS date, 
           date_part('epoch', dates.actual_date) AS epoch_date
    FROM (
        SELECT season,
                date, 
                to_date(date, 'YYYY-MM-DD') AS actual_date
                FROM matches
                WHERE season = '2011'
                GROUP BY date, season
                ORDER BY date, season
        ) AS dates
);
