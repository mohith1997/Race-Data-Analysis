use f1db;

-- test update of constructor points based on delete in results
select * from constructorresults
natural join races
where constructorId = 6
and name = "British Grand Prix" and year = 2017;


-- test update of points on insert in results
select * from pointSystem;

select * from results
where positionText = 'eee';
