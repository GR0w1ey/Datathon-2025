-- Visualisation 1

-- query for line graph showing the 2024 average Lap times during the 3 qualifying sessions for the McLaren Mercedes drivers (Lando Norris and Oscar Piastri) and Red Bull drivers (Max Verstappen and Sergio Perez), what to do if a driver failed to make it into Q3? (i.e. Lando Norris for Azerbaijan Grand Prix

SELECT race.name as race_name, driver.driverid, quali.position, quali.q1, quali.q2, quali.q3
FROM PLAYGROUND.DATATHON.RACES AS race
JOIN PLAYGROUND.DATATHON.QUALIFYING quali ON quali.RACEID = race.RACEID
JOIN PLAYGROUND.DATATHON.DRIVERS driver ON driver.driverid = quali.driverid
WHERE quali.driverid in (846, 857, 830, 815)
AND race.year = 2024
ORDER BY race.raceid;

-- Alternatively tried this but TO_TIME only produces '00:01:30' instead of expected '01:30.438':

-- SELECT race.name as race_name, driver.driverid, quali.position, quali.q1 AS original_q1, TRY_TO_TIME(quali.q1, 'MI:SS.FF3') as q1, quali.q2 as original_q2, TRY_TO_TIME(quali.q2, 'MI:SS.FF3') as q2, quali.q3 as original_q3, TRY_TO_TIME(quali.q3, 'MI:SS.FF3') as q3
-- FROM PLAYGROUND.DATATHON.RACES AS race
-- JOIN PLAYGROUND.DATATHON.QUALIFYING quali ON quali.RACEID = race.RACEID
-- JOIN PLAYGROUND.DATATHON.DRIVERS driver ON driver.driverid = quali.driverid
-- WHERE quali.driverid in (846, 857, 830, 815)
-- AND race.year = 2024
-- ORDER BY race.raceid;

-- - RESULTS table has a milliseconds column but that refers to the overall race time (TIME column) rather than FASTESTLAPTIME column which would be more insightful

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

SELECT race.year, race.round, constuct.name, con_stand.constructorid, con_stand.points, con_stand.position
FROM PLAYGROUND.DATATHON.RACES AS race
JOIN PLAYGROUND.DATATHON.CONSTRUCTOR_STANDINGS con_stand ON con_stand.RACEID = race.RACEID
JOIN PLAYGROUND.DATATHON.CONSTRUCTORS constuct ON constuct.constructorid = con_stand.constructorid
WHERE race.year IN (2022, 2023, 2024)
AND con_stand.constructorid IN (1, 6, 9, 117, 131, 214)
ORDER BY con_stand.raceid, con_stand.position, con_stand.constructorid;
