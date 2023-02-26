use f1db;


delimiter //
create function constructorPoints(constructorId int, raceId int) returns int deterministic
begin
declare point_total int;

select sum(points) into point_total from results
where results.constructorId = constructorId and results.raceId = raceID;

return point_total;

end//

delimiter ;

delimiter //

create trigger updateConstructorResultsInsert after insert on results for each row
begin
insert into constructorresults (raceId, constructorId, points, status) values
(new.raceId, new.constructorId, constructorPoints(new.constructorId, new.raceId), new.statusId);
end //

delimiter ;

delimiter //

create trigger updateConstructorResultsDelete after delete on results for each row
begin
update constructorresults set points = constructorPoints(old.constructorId, old.raceId)
where raceId = old.raceId and constructorId = old.constructorId;
end //

delimiter ;

delimiter //

create trigger updateConstructorResultsUpdate after update on results for each row
begin
update constructorresults set points = constructorPoints(new.constructorId, new.raceId)
where raceId = old.raceId and constructorId = old.constructorId;
end //

delimiter ;

CREATE TABLE pointSystem (
    id INT PRIMARY KEY AUTO_INCREMENT,
    year INT,
    position INT,
    points INT,
    fastestlap BOOL,
    CONSTRAINT FOREIGN KEY (year)
        REFERENCES seasons (year)
        ON DELETE RESTRICT ON UPDATE RESTRICT
);

insert into pointSystem (year, position, points, fastestlap)
values
(2017, 1, 25, false),
(2017, 2, 18, false),
(2017, 3, 15, false),
(2017, 4, 12, false),
(2017, 5, 10, false),
(2017, 6, 8, false),
(2017, 7, 6, false),
(2017, 8, 4, false),
(2017, 9, 2, false),
(2017, 10, 1, false),
(2016, 1, 25, false),
(2016, 2, 18, false),
(2016, 3, 15, false),
(2016, 4, 12, false),
(2016, 5, 10, false),
(2016, 6, 8, false),
(2016, 7, 6, false),
(2016, 8, 4, false),
(2016, 9, 2, false),
(2016, 10, 1, false);

delimiter //

create trigger pointsUpdate after insert on results for each row
begin
update results set points = (select points from pointSystem where pointSystem.position = new.positionOrder
and pointSystem.year = (select year from races where races.raceId = new.raceId))
where new.resultId = results.resultId;
end //

delimiter ;


delimiter //

create trigger pointsUpdate before insert on results for each row
begin
set new.points = ifnull(
	(
    select points from pointSystem where pointSystem.position = new.positionOrder
	and pointSystem.year = (select year from races where races.raceId = new.raceId)
    ), 0);
end //

delimiter ;
