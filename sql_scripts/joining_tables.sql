SELECT *
FROM PLAYGROUND.DATATHON.RACES AS race
FULL JOIN PLAYGROUND.DATATHON.RESULTS res ON res.RACEID = race.RACEID -- full join as we want ALL the races, even with no results? do we?
JOIN PLAYGROUND.DATATHON.DRIVERS driver ON driver.driverid = res.driverid
WHERE race.year = 2024
ORDER BY race.raceid, res.position;
