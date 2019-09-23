-- calculate win percentage in rain games for each club during the 2011 season
CREATE TABLE club_rain_win_pct_2011
AS (
    SELECT season,
        div,
        club,
        wins AS rain_wins,
        total_games AS total_rain_games,
        ROUND(CAST(wins AS NUMERIC)/ total_games, 2) AS rain_win_pct
    FROM club_rain_stats_2011
);
