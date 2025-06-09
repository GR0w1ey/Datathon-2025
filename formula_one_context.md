# Formula 1 Context document

The objective for this document is to help easily explain Formula 1 on a high level as well as provide context to the tables and data we will be using.

This markdown document has been split into 2 parts:

- F1 Overview (designed to give a high level explanation on various aspects of Formula 1 which is relevant to our dataset)
- Table Explanation (designed to break down each table provided to us and explain what data it has)

It is also worth pointing out that for the purpose of clarity, I refer to a race as "standard race" to clearly distinguish it from a "sprint race".

## F1 Overview

### Traditional race format

In Formula 1, a season happens every year (typically starting around March and ending in November)

A Formula 1 season consists of a number "race weekends"

A traditional race weekend takes place over Friday, Saturday and Sunday consisting of practice sessions, qualifying sessions and the standard race itself

Formula 1 has 10 teams which are called constructors

Each team has 2 drivers that compete during a race weekend in their own separate cars

The drivers compete for the drivers championship (awarded to the individual driver with the most points at the end of the season) and the constructors championship (awarded to the team who's drivers have the most points when combined together)

### Qualifying

Qualifying takes place on Saturday and has 3 parts: Qualifying 1, Qualifying 2 and Qualifying 3 (more commonly referred to Q1, Q2 and Q3)

The aim for qualifying is to determine each driver's starting grid position for the race by setting the fastest lap time 

In Qualifying 1, all 20 drivers participate to set the fastest lap they can within an 18 minute period

The slowest 5 drivers at the end of Qualifying 1 do not advance to Qualifying 2 and where they finished Qualifying 1 is where they will start the race

- i.e. this sets up the starting grid positions for positions 16, 17, 18, 19, 20

In Qualifying 2, the 15 drivers that progressed from Qualifying 1 try to set the fastest lap within a 15 minute period

Once again, the slowest 5 drivers at the end of Qualifying 2 do not advance to Qualifying 3 and where they finished Qualifying 2 is where they will start the race

- i.e. this sets up the starting grid positions for 11, 12, 13, 14, 15

In Qualifying 3, the top 10 drivers have 12 minutes to set the fastest lap to determine the starting grid positions for the top 10

### Standard Race (typically just referred to as "race")

A race takes place on Sunday and runs for a specified number of laps (typically lasting for around 2 hours)

In a standard race points are determined based on which position a driver finishes the race

Since 2010, the top 10 receive points:

1st = 25 points <br>
2nd = 18 points <br>
3rd = 15 points <br>
4th = 12 points <br>
5th = 10 points <br>
6th = 8 points <br>
7th = 6 points <br>
8th = 4 points <br>
9th = 2 points <br>
10th = 1 point <br>

When looking at the Results table, you may notice a driver being awarded 26 points instead of 25 points (as an example), this is because between 2019 - 2024, the driver who had the fastest lap in the race earns 1 additional point

- contextually, this meant that sometimes, drivers who were outside of the top 10 would pit for new tyres towards the end of a race and try to get the fastest lap
- for example, in the 2024 Singapore race, Daniel Riccardo got the fastest lap which meant he still earned 1 point despite finishing 18th and being lapped (+ 1 lap)

The overall goal for a race from a team's point of view is to have their 2 drivers finish 1st and 2nd so that they can get the most amount of points for the constructors championship

During a race, drivers will make pit stops

Pit stops are made to change tyres (which they have to do at least once) or to replace a damaged component that can be replaced

- I point this out because while pit stops themselves only typically take 2-3 seconds, the time spent in the pit lane (where a driver travels through to get to their garage for a pit stop and back out to the race track) is typically around 20 seconds
- So, when analysing the lap times in the Lap_Times table, if a drivers lap time fluctuate by 20 seconds on a particular lap, this is the most likely cause for this

### Sprint Races

Sprint races are a shorter version of a standard race (typically lasting only 30 minutes)

Sprint races only occur at a few race weekends during a season and does not replace the standard race when it does occur

As of 2024, the sprint race occurs on a Saturday before regular qualifying 

- Note: the sprint race grid is determined by a separate sprint qualifying but since sprint qualifying is not tracked in any of our tables I will not go into details about how this works

Due to the short length of the race, pit stops for a tyre change are not required to be made at all

Sprint races also award points:

1st = 8 points <br>
2nd = 7 points <br>
3rd = 6 points <br>
4th = 5 points <br>
5th = 4 points <br>
6th = 3 points <br>
7th = 2 points <br>
8th = 1 point <br>

### Miscellaneous

When a status say + number of laps (as seen in the Status table) refers to the number of times a driver has been lapped by the leader

- (for example: if Alex and Ben are in a 50 lap race, Alex is leading the race and Ben is last. At some point before the final lap Alex manages to overtake Ben while Ben is last, we would say that Ben has been lapped by the leader so when Alex finishes the race on lap 50, Ben has to finish the race at lap 49 as the chequered flag to finish the race is now being waved)
- simply put, once the leader finishes the race causing the chequered flag to wave, all drivers must finish the race regardless of what lap they are on

## Tables Explanation

### Circuits 

- shows all the race tracks that have been raced on in Formula 1 history

### Constructors 

- shows every Formula 1 team to have competed in Formula 1 history

### Constructor_Results 

- shows the total number of points that both drivers for their associated team got at an individual race 
- i.e. if McLaren got 43 points at the 2025 British Grand Prix, it would be because Oscar Piastri got 25 points and Lando Norris got 18 points

### Constructor_Standings 

- shows the cumulative points that each team gets throughout each season and each team's position

### Drivers 

- shows a list of all the drivers to have competed in Formula 1 history

### Lap_Times 

- shows each lap time from each driver during the course of a race as well as showing which position the driver ended each lap on

### Pit_Stops 

- shows all the pit stops that take place in each race for each driver, indicating if it was a driver's 1st, 2nd, 3rd or 4th stop etc and the time it took for the pit stop to occur

### Qualifying 

- shows each driver's fastest lap in Qualifying session 1, Qualifying session 2 and Qualifying session 3 
- if a driver didn't proceed to Qualifying session 2 or Qualifying session 3 then the lap time will be null

### Races 

- shows every race that has taken place in Formula 1 history with the name of the race and which round this race took place 
- i.e. in 2024, the British Grand Prix was the 12th race

### Results 

This includes the following:

- each driver's starting position for an individual standard race (GRID column) 
- the position each driver finished the race (POSITION column)
- the number of laps the driver completed
- the number points the driver achieved at an individual race
- how far away on the track each driver that wasn't lapped by the leader was from 1st place when the race finished (TIME column, 1st place has their total time on track, anyone with + 1 lap, + 2 lap, DNF etc have a null time)
- FASTESTLAPTIME column shows the fastest lap a driver achieved during the race
- FASTESTLAP column indicates the specific lap the driver set their fastest lap (i.e. if it was 40 for a driver then their fastest lap in the FASTESTLAPTIME column was set on lap 40)
- STATUSID (*see Status table explanation*)

### Seasons 

- shows the year of each Formula 1 season with an associated Wikipedia link

### Sprint_Results 

- essentially the same type of data as the results table but instead has data for only the sprint races unlike the Results table which only has data for the standard races

### Status 

Used to indicate the following:

- whether a driver finished the race and wasn't lapped (STATUSID = 1)
- whether a driver finished the race but was lapped (e.g. STATUSID = 11 which is + 1 lap)
- whether the driver did not finish
- whether the driver had a specific reason for not starting or finishing the race
