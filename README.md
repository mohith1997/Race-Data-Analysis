# Formula 1 results analytics dashboard

Submission for CS5200 Database Management System

## Software requirement

* python3 (known bug with python3.9 in mac)
* MySQL (atleast version 6)

## Setting up the environment

* Run `pip install -r requirements.txt` to install the required dependencies. We recommend setting up a python virtual environment.
* Setup and run the mysql server locally.
* Import the data into MySQL using the dump provided.
* Specify your dbms credential in env.yaml. The application assumes that you are using a local sql server (localhost).

### Fixing weird mysql user privilege bug

There was a weird glitch with the latest version of MySQl which created some privilege issues.

Run the following commands before running the dashboard to ensure it works.

```sql
create user 'surya'@'%';
-- or if that fails in your version this:
create user 'surya'

grant all privileges on *.* to 'surya'@'%';
```

## Running the dashboard

```bash
streamlit run app.py
```

## Files

Description of modules and scripts

### Dashboard

**pages** - Sub-package contains the pages available for the multi-page dashboard application as scripts. Each script contains the interface code.

**pageutils** - Sub-package contains supporting python functions for the various pages.

**utils.py** - Module additional supporting python functions for the dashboard

**sql.py** - Module contains utilty functions for interfacing with the sql operations and sql queries used within the application.

**app.py** - Main driver code for the dashboard.

### SQL

**sql.py** - Contains queries required in the application which includes calls to procedures.

#### sqlscripts:

**procs_funcs.sql** - Contains procedures and functions used in the dashboard.

**triggers.sql** - Contains triggers used in the application.

**views.sql** Contains the views used in the application.


