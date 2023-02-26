use f1db;

delimiter //

create procedure filter_results(in raceIdIn int, in driverIdIn int, in constructorIdIn int)
begin
	select resultId,
		races.name as race, races.year as race_year, 
		concat(drivers.forename, " ", drivers.surname) as driver,  
		constructors.name as constructor,
		results.number, `grid`, `position`, `positionText`, `positionOrder`, `points`, `laps`, results.`time`, `milliseconds`,
    status
    from results
    inner join races 
		on results.raceId = races.raceId
	inner join drivers
		on results.driverId = drivers.driverId
	inner join constructors
		on results.constructorId = constructors.constructorId
	inner join status
		on results.statusId = status.statusId
    where 
		(raceIdIn is NULL or results.raceId = raceIdIn)
        and (driverIdIn is NULL or results.driverId = driverIdIn)
        and (constructorIdIn is NULL or results.constructorId = constructorIdIn);

end
//
delimiter ;


delimiter //

create procedure filter_qualifying(in raceIdIn int, in driverIdIn int, in constructorIdIn int)
begin
	select qualifyId,
		qualifying.raceId,
		races.name as race, races.year as race_year, 
		concat(drivers.forename, drivers.surname) as driver,  
		constructors.name as constructor,
        qualifying.number, position, q1, q2, q3
    from qualifying
    inner join races 
		on qualifying.raceId = races.raceId
	inner join drivers
		on qualifying.driverId = drivers.driverId
	inner join constructors
		on qualifying.constructorId = constructors.constructorId
    where 
		(raceIdIn is NULL or qualifying.raceId = raceIdIn)
        and (driverIdIn is NULL or qualifying.driverId = driverIdIn)
        and (constructorIdIn is NULL or qualifying.constructorId = constructorIdIn);

end
//
delimiter ;

delimiter //

create procedure filter_constructor_results(in raceIdIn int, in constructorIdIn int)
begin
	select constructorResultsId,
		races.name as race, races.year as race_year, 
		constructors.name as constructor,
        points, status
    from constructorresults as results
    inner join races 
		on results.raceId = races.raceId
	inner join constructors
		on results.constructorId = constructors.constructorId
    where 
		(raceIdIn is NULL or results.raceId = raceIdIn)
        and (constructorIdIn is NULL or results.constructorId = constructorIdIn);
end
//
delimiter ;


delimiter //

create function ms_to_s(timeinms decimal)
returns float
deterministic
begin
	declare timeins float;
    set timeins = cast(timeinms / 1000 as float);
    return timeins;
end

//
delimiter ;

delimiter //

create procedure lap_stats(in raceIdIn int, in driverIdIn int)
begin
	select lap, position, ms_to_s(milliseconds) as seconds
    from laptimes
    where 
		laptimes.raceId = raceIdIn
        and laptimes.driverId = driverIdIn;
end
//
delimiter ;


delimiter //

create procedure race_stats(in seasonIn int, in driverIdIn int)
begin
	select results.raceId, points, positionOrder, laptimes.fastestLapTime, slowestLapTime, avgLapTime
    from results
    inner join (select races.raceId, year from races where year = seasonIn) as races
		on results.raceId = races.raceId 
	inner join (
			select raceId, max(ms_to_s(milliseconds)) as slowestLapTime, min(ms_to_s(milliseconds)) as fastestLapTime,
            avg(ms_to_s(milliseconds)) as avgLapTime
            from laptimes            
            group by raceId
		) as laptimes
		on results.raceId = laptimes.raceId 
    where results.driverId = driverIdIn
    order by raceId;
end
//
delimiter ;