use f1db;

CREATE VIEW driver_standings AS
    SELECT 
        driver_results.driverId,
        forename,
        surname,
        nationality,
        year,
        total_points AS points,
        wins,
        podiums
    FROM
        (SELECT 
            driverId,
                year,
                IFNULL(CAST(SUM(points) AS UNSIGNED), 0) AS total_points,
                IFNULL(CAST(SUM(position = 1) AS UNSIGNED), 0) AS wins,
                IFNULL(CAST(SUM(position <= 3) AS UNSIGNED), 0) AS podiums
        FROM
            results AS re
        INNER JOIN races AS ra ON re.raceId = ra.raceId
        GROUP BY driverId , year) driver_results
            INNER JOIN
        drivers ON driver_results.driverId = drivers.driverId;
    


CREATE VIEW constructor_standings AS
select constructor_results.constructorId, name, nationality, year,
	total_points as points, wins, podiums
from (
	select constructorId, year, 
		ifnull(cast(sum(points) as unsigned), 0) as total_points,  
		ifnull(cast(sum(position = 1) as unsigned), 0) as wins, 
		ifnull(cast(sum(position <= 3) as unsigned), 0) as podiums
	from (
		select *,
		rank() over (partition by raceId order by points desc) as position
		from constructorresults
	) as cr
	inner join races as ra
		on cr.raceId = ra.raceId
	group by constructorId, year
) as constructor_results
inner join constructors
	on constructor_results.constructorId = constructors.constructorId;
