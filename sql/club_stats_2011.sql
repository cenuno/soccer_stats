/*
Calculate club, home_goals, away_goals, goals, wins, losses,
ties, total games, and season for 2011 
*/
CREATE TABLE club_stats_2011 
AS (
    SELECT home.season AS season,
        home.div,
        hometeam AS club,
        home_goals_for, 
        away_goals_for,
        (home_goals_for + away_goals_for) AS goals_for,
        home_goals_against,
        away_goals_against,
        (home_goals_against + away_goals_against) AS goals_against,
        (home_wins + away_wins) AS wins,
        (home_losses + away_losses) AS losses,
        (home_ties + away_ties) AS ties,
        (home_wins + away_wins + home_losses +
            away_losses + home_ties + away_ties) AS total_games
    FROM (
        SELECT season,
                hometeam, 
                div,
                SUM(fthg) AS home_goals_for,
                SUM(ftag) AS home_goals_against,
                SUM(CASE WHEN ftr='H' THEN 1 ELSE 0 END) AS home_wins,
                SUM(CASE WHEN ftr='A' THEN 1 ELSE 0 END) AS home_losses,
                SUM(CASE WHEN ftr='D' THEN 1 ELSE 0 END) AS home_ties
        FROM matches
        WHERE season = '2011'
        GROUP BY season, div, hometeam
        ) AS home
    JOIN (
        SELECT season,
                div,
                awayteam,
                SUM(ftag) AS away_goals_for,
                SUM(fthg) AS away_goals_against,
                SUM(CASE WHEN ftr='H' THEN 1 ELSE 0 END) AS away_losses,
                SUM(CASE WHEN ftr='A' THEN 1 ELSE 0 END) AS away_wins,
                SUM(CASE WHEN ftr='D' THEN 1 ELSE 0 END) AS away_ties
        FROM matches
        WHERE season = '2011'
        GROUP BY season, div, awayteam
        ) AS away
        ON home.hometeam = away.awayteam
    ORDER BY club
);
