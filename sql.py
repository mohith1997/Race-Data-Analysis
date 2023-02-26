import pymysql
import yaml
from pymysql import IntegrityError


def create_mysql_connection():
    with open("env.yaml") as f:
        env = yaml.load(f, yaml.BaseLoader)
    return pymysql.connect(
        host="localhost",
        user=env["user"],
        password=env["passwd"],
        database=env["db"],
        cursorclass=pymysql.cursors.DictCursor,
    )


def read_sql(conn, query, **kwargs):
    with conn.cursor() as cursor:
        cursor.execute(query, kwargs)
        result = cursor.fetchall()
        return result


def execute_sql(conn, query, **kwargs):
    with conn.cursor() as cursor:
        cursor.execute(query, kwargs)
    conn.commit()


def get_names(conn, query):
    """
    Get unique option names
    """
    with conn.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()

        res_list = []
        for res in result:
            vals = map(str, res.values())
            res_list.append("__".join(vals))

        return res_list


"""
List of queries
"""


DRIVER_NAMES = """
select driverId, driverRef from drivers
"""

CONSTR_NAMES = """
select constructorId, constructorRef from constructors
"""

RACE_NAMES = """
select raceId, name, year from races
order by year desc
"""

SEASON_NAMES = """
select year from seasons
order by year desc
"""

STATUS_NAMES = """
select statusId, status from status
"""


RESULT_FILTER = """
call filter_results(%(raceId)s, %(driverId)s, %(constructorId)s)
"""

QUALIFY_FILTER = """
call filter_qualifying(%(raceId)s, %(driverId)s, %(constructorId)s)
"""

CONSTRUCTOR_RESULT_FILTER = """
call filter_constructor_results(%(raceId)s, %(constructorId)s)
"""

CONSTRUCTOR_RESULT_BY_ID = """
select * from constructorresults where constructorResultsId = %(constructorResultsId)s
"""

RESULT_WITH_STATUS_BY_ID = """
select * from results
inner join status
    on results.statusId = status.statusId
where resultId = %(resultId)s
"""

POINTS_FILTER = """
select * from pointSystem
where year = %(year)s and position = %(position)s
"""


LAPTIME_STATS = """
call lap_stats(%(raceId)s, %(driverId)s)
"""

RACE_STATS = """
call race_stats(%(seasonId)s, %(driverId)s)
"""

DRIVER_STANDINGS = """
select concat(forename, " ", surname) as name, nationality, year,
    points, wins, podiums
from driver_standings
where year = %(year)s
order by points desc
"""

CONSTRUCTOR_STANDINGS = """
select name, nationality, year,
    points, wins, podiums
from constructor_standings
where year = %(year)s
order by points desc
"""


DEL_RESULT = """
delete from results where resultId = %(resultId)s
"""

DEL_QUALIFIER = """
delete from qualifying where qualifyId = %(qualifyId)s
"""

DEL_CONSTRUCTOR = """
delete from constructorresults where constructorResultsId = %(constructorResultsId)s
"""

DEL_SEASON = """
delete from seasons where year = %(year)s
"""


INSERT_RESULT = """
insert into results (raceId, driverId, constructorId, number, grid, position, positionText, positionOrder, statusId, laps)
values (%(raceId)s, %(driverId)s, %(constructorId)s, %(number)s, %(grid)s, %(position)s, %(positionText)s, %(positionOrder)s, %(statusId)s, %(laps)s)
"""

INSERT_QUALIFIER = """
insert into qualifying (raceId, driverId, constructorId, number, position, q1, q2, q3)
values (%(raceId)s, %(driverId)s, %(constructorId)s, %(number)s, %(position)s, %(q1)s, %(q2)s, %(q3)s)
"""

INSERT_RACE = """
insert into races (year, round, circuitId, name, time, url)
values (%(year)s, %(round)s, %(circuitId)s, %(name)s, %(time)s, %(url)s)
"""


UPDATE_POINTS = """
update pointSystem
set points = %(points)s, fastestlap = %(fastestlap)s
where id = %(id)s
"""

UPDATE_RESULT_STATUS = """
update results
set statusId = %(statusId)s
where resultId = %(resultId)s
"""

UPDATE_CONSTRUCTOR_STATUS = """
update constructorresults
set status = %(status)s
where constructorResultsId = %(constructorResultsId)s
"""
