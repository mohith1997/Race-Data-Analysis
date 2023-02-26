use f1db;

/*
Drop columns - redundant columns for our purposes
*/

alter table results
drop `rank`,
drop fastestLap,
drop fastestLapTime,
drop fastestLapSpeed;

/*
Drop rows - only keep seasons that we are working on
Note: The results table already only has data from 2016-2017. 
*/

DELETE FROM drivers 
WHERE
    driverId NOT IN (SELECT DISTINCT
        driverId
    FROM
        results);

DELETE FROM constructors 
WHERE
    constructorId NOT IN (SELECT DISTINCT
        constructorId
    FROM
        results);

DELETE FROM races 
WHERE
    year NOT IN (2016 , 2017);

DELETE FROM seasons 
WHERE
    year NOT IN (2016 , 2017);
