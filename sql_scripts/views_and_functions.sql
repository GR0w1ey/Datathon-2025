CREATE FUNCTION convert_quali_time(quali_string STRING)
RETURNS FLOAT
AS
$$ 
    SPLIT_PART(quali_string, ':', 1)::FLOAT * 60 + 
    SPLIT_PART(quali_string, ':', 2)::FLOAT
$$;

create or replace view EVENT.DATATHON_2025_TEAM_ALPHA.VISUALISATION_ONE as (

    SELECT race.raceid, race.name as race_name, driver.driverid, CONCAT(driver.forename, ' ', driver.surname) AS driver_name, IFNULL(CASE WHEN quali.q3 = '' THEN NULL ELSE quali.q3 END, '0:00.000') as q3_with_null, CONVERT_QUALI_TIME(IFNULL(CASE WHEN quali.q3 = '' THEN NULL ELSE quali.q3 END, '0:00.000')) as q3_in_seconds
    FROM PLAYGROUND.DATATHON.RACES AS race
    JOIN PLAYGROUND.DATATHON.QUALIFYING quali ON quali.RACEID = race.RACEID
    JOIN PLAYGROUND.DATATHON.DRIVERS driver ON driver.driverid = quali.driverid
    WHERE quali.driverid in (846, 857, 830, 815)
    AND race.year = 2024
    ORDER BY race.raceid

);

create or replace view EVENT.DATATHON_2025_TEAM_ALPHA.VISUALISATION_ONE_VERSION_TWO as (

    WITH all_qualifying_times AS(
    
        SELECT race.raceid, race.name as race_name, quali.constructorid, const.name AS constructor_name, IFNULL(CASE WHEN quali.q1 = '' THEN NULL ELSE quali.q1 END, '0:00.000') as q1_with_null, CONVERT_QUALI_TIME(IFNULL(CASE WHEN quali.q1 = '' THEN NULL ELSE quali.q1 END, '0:00.000')) as q1_in_seconds, IFNULL(CASE WHEN quali.q2 = '' THEN NULL ELSE quali.q2 END, '0:00.000') as q3_with_null, CONVERT_QUALI_TIME(IFNULL(CASE WHEN quali.q2 = '' THEN NULL ELSE quali.q2 END, '0:00.000')) as q2_in_seconds, IFNULL(CASE WHEN quali.q3 = '' THEN NULL ELSE quali.q3 END, '0:00.000') as q3_with_null, CONVERT_QUALI_TIME(IFNULL(CASE WHEN quali.q3 = '' THEN NULL ELSE quali.q3 END, '0:00.000')) as q3_in_seconds 
        FROM PLAYGROUND.DATATHON.RACES AS race
        JOIN PLAYGROUND.DATATHON.QUALIFYING quali ON quali.RACEID = race.RACEID
        JOIN PLAYGROUND.DATATHON.DRIVERS driver ON driver.driverid = quali.driverid
        JOIN PLAYGROUND.DATATHON.CONSTRUCTORS const ON const.constructorid = quali.constructorid
        WHERE quali.driverid in (846, 857, 830, 815)
        AND race.year = 2024
        ORDER BY race.raceid
    
    )
    
    SELECT raceid, race_name, constructorid, constructor_name, ((AVG(q1_in_seconds) + AVG(q2_in_seconds) + AVG(q3_in_seconds)) / 3) AS average_qualifying_time
    FROM all_qualifying_times
    GROUP BY raceid, constructorid, race_name, constructor_name
    ORDER BY raceid

);

create or replace view EVENT.DATATHON_2025_TEAM_ALPHA.VISUALISATION_TWO as (

    SELECT res.constructorid, con.name, res.position, COUNT(res.positiontext) AS number_of_places_finished
    FROM PLAYGROUND.DATATHON.RACES AS race
    JOIN PLAYGROUND.DATATHON.RESULTS res ON res.RACEID = race.RACEID
    JOIN PLAYGROUND.DATATHON.DRIVERS driver ON driver.driverid = res.driverid
    JOIN PLAYGROUND.DATATHON.CONSTRUCTORS con ON con.constructorid = res.constructorid
    WHERE race.year = 2024
    AND res.driverid in (846, 857, 830, 815)
    AND res.positiontext != 'R'
    GROUP BY res.constructorid, con.name, res.positiontext, res.position
    ORDER BY res.constructorid, res.position

);

create or replace view EVENT.DATATHON_2025_TEAM_ALPHA.VISUALISATION_THREE as (

    SELECT race.year, race.round, constuct.name, con_results.points
    FROM PLAYGROUND.DATATHON.RACES AS race
    JOIN PLAYGROUND.DATATHON.CONSTRUCTOR_RESULTS con_results ON con_results.RACEID = race.RACEID
    JOIN PLAYGROUND.DATATHON.CONSTRUCTORS constuct ON constuct.constructorid = con_results.constructorid
    WHERE race.year IN (2022, 2023, 2024)
    AND con_results.constructorid IN (1, 6, 9, 131)
    ORDER BY con_results.raceid, con_results.points DESC

);

create or replace view EVENT.DATATHON_2025_TEAM_ALPHA.VISUALISATION_FOUR as (

    WITH constructor_success_score AS (
        SELECT res.raceid, res.constructorid, SUM(res.ml_success_score) as ml_success_score
        FROM EVENT.DATATHON_2025_TEAM_ALPHA.RACE_RESULTS_1999_2024_WITH_SUCCESS_SCORE as res
        WHERE res.raceid IN (SELECT raceid FROM PLAYGROUND.DATATHON.RACES WHERE YEAR IN (2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024))
        GROUP BY res.raceid, res.constructorid
        ORDER BY res.raceid
    )
    
    SELECT res.raceid, race.year, race.round, constructor.constructorid, constructor.name, res.ml_success_score
    FROM constructor_success_score as res
    JOIN PLAYGROUND.DATATHON.CONSTRUCTORS as constructor ON constructor.constructorid = res.constructorid
    JOIN PLAYGROUND.DATATHON.RACES as race ON race.raceid = res.raceid
    WHERE (res.raceid, res.ml_success_score) IN (SELECT raceid, MAX(ml_success_score) FROM constructor_success_score GROUP BY raceid)
    ORDER BY res.raceid

);

create or replace view EVENT.DATATHON_2025_TEAM_ALPHA.VISUALISATION_FIVE as (

    WITH mclaren_winning_season_comparison AS (
        SELECT res.raceid, SUM(res.ml_success_score) AS ml_success_score
        FROM EVENT.DATATHON_2025_TEAM_ALPHA.RACE_RESULTS_1999_2024_WITH_SUCCESS_SCORE as res
        WHERE res.raceid IN (SELECT raceid FROM PLAYGROUND.DATATHON.RACES WHERE YEAR IN (1999, 2024))
        AND res.constructorid = 1 -- McLaren
        GROUP BY res.raceid
        ORDER BY res.raceid
    )
    
    SELECT race.year, TO_DECIMAL(AVG(res.ml_success_score)) as average_success_across_the_season
    FROM mclaren_winning_season_comparison as res
    JOIN PLAYGROUND.DATATHON.RACES as race ON race.raceid = res.raceid
    GROUP BY race.year

);
