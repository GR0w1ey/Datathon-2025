-- Visualisation 1

-- query for line graph showing the 2024 average Lap times during the 3 qualifying sessions for the McLaren Mercedes drivers (Lando Norris and Oscar Piastri) and Red Bull drivers (Max Verstappen and Sergio Perez), what to do if a driver failed to make it into Q3? (i.e. Lando Norris for Azerbaijan Grand Prix

SELECT race.name as race_name, driver.driverid, quali.position, quali.q1, quali.q2, quali.q3
FROM PLAYGROUND.DATATHON.RACES AS race
JOIN PLAYGROUND.DATATHON.QUALIFYING quali ON quali.RACEID = race.RACEID
JOIN PLAYGROUND.DATATHON.DRIVERS driver ON driver.driverid = quali.driverid
WHERE quali.driverid in (846, 857, 830, 815)
AND race.year = 2024
ORDER BY race.raceid;

-- - can also do the same for the race lap times as well but I would argue qualifying is more insightful as qualifying sessions mean every team is pushing their car to get the fastest time possible whereas race lap times are not necessarily indicative of having the fastest car during the race due to multiple factors (tyre choices, time spent behind traffic, any damage to the car etc)

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

-- Visualisation 2

-- stacked bar graph indicating the number of 1st place finishes, 2nd place finishes, 3rd place finishes, 4th place finishes, 5th place finishes, 6th place finishes, 7th place finishes, 8th place finishes, 9th place finishes and 10th place finishes that McLaren Mercedes had and Red Bull had in the 2024 season

SELECT res.constructorid, res.positiontext, COUNT(res.positiontext) AS number_of_places_finished
FROM PLAYGROUND.DATATHON.RACES AS race
FULL JOIN PLAYGROUND.DATATHON.RESULTS res ON res.RACEID = race.RACEID
JOIN PLAYGROUND.DATATHON.DRIVERS driver ON driver.driverid = res.driverid
WHERE race.year = 2024
AND res.driverid in (846, 857, 830, 815)
GROUP BY res.constructorid, res.positiontext, res.position
ORDER BY res.constructorid, res.position;

-- stacked bar graph that drills down the drivers finishes specifically

SELECT res.driverid, res.positiontext, COUNT(res.positiontext) AS number_of_places_finished
FROM PLAYGROUND.DATATHON.RACES AS race
FULL JOIN PLAYGROUND.DATATHON.RESULTS res ON res.RACEID = race.RACEID
JOIN PLAYGROUND.DATATHON.DRIVERS driver ON driver.driverid = res.driverid
WHERE race.year = 2024
AND res.driverid in (846, 857, 830, 815)
GROUP BY res.driverid, res.positiontext, res.position
ORDER BY res.driverid, res.position;

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

-- Visualisation 3

-- line graph showing the best finish at each race every team who McLaren were competing against between 2022-2024 (this is because this was when the new regulations were introduced)

-- this will therefore show McLaren Mercedes, Red Bull Racing, Ferrari, Mercedes, Alpine Renault, Aston Martin

SELECT race.year, race.round, constuct.name, con_results.points
FROM PLAYGROUND.DATATHON.RACES AS race
JOIN PLAYGROUND.DATATHON.CONSTRUCTOR_RESULTS con_results ON con_results.RACEID = race.RACEID
JOIN PLAYGROUND.DATATHON.CONSTRUCTORS constuct ON constuct.constructorid = con_results.constructorid
WHERE race.year IN (2022, 2023, 2024)
AND con_results.constructorid IN (1, 6, 9, 117, 131, 214)
ORDER BY con_results.raceid, con_results.points DESC;

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

-- Visualisation 4

-- line graph to show the best performing team in each race between 2014-2024 using Mark's ML success score algorithm

WITH constructor_success_score AS (
    SELECT res.raceid, res.constructorid, SUM(res.ml_success_score) as ml_success_score
    FROM EVENT.DATATHON_2025_TEAM_ALPHA.RACE_RESULTS_1999_2024_WITH_SUCCESS_SCORE as res
    WHERE res.raceid IN (SELECT raceid FROM PLAYGROUND.DATATHON.RACES WHERE YEAR IN (2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024))
    GROUP BY res.raceid, res.constructorid
    ORDER BY res.raceid
)

SELECT res.raceid, race.year, race.round, constructor.name, res.ml_success_score
FROM constructor_success_score as res
JOIN PLAYGROUND.DATATHON.CONSTRUCTORS as constructor ON constructor.constructorid = res.constructorid
JOIN PLAYGROUND.DATATHON.RACES as race ON race.raceid = res.raceid
WHERE (res.raceid, res.ml_success_score) IN (SELECT raceid, MAX(ml_success_score) FROM constructor_success_score GROUP BY raceid);

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

-- Visualisation 5

-- bar graph comparing the success score average between McLaren's 1999 constructor winning season to 2024 constructor winning season

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
GROUP BY race.year;
