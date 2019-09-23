-- store 2011 matches data that now contains rain flag
CREATE TABLE matches_2011_weather
AS (
    SELECT match_id,
        div,
        season,
        weather.date,
        weather.rain,
        hometeam,
        awayteam,
        fthg,
        ftag,
        ftr
    FROM matches
    JOIN (
        -- join rain flag onto YYYY-MM-DD data for unique 2011 matches
        SELECT CAST(dates.date AS TEXT) AS date, 
            weather.rain
        FROM unique_2011_weather AS weather
        JOIN unique_2011_dates AS dates
            ON CAST(dates.epoch_date AS TEXT) = weather.epoch_date
    ) AS weather
        ON matches.date = weather.date
    ORDER BY match_id
);
