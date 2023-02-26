import streamlit as st
from utils import get_db_conn
from sql import *
from pageutils.commons import *
from pageutils.create import *

st.set_page_config(page_title="Create Data", page_icon="📥")

conn = get_db_conn()

add_selection = st.sidebar.selectbox(
    "Select item to create", ["Race", "Result", "Qualifier"]
)


if add_selection == "Race":
    with st.form("Insert race", clear_on_submit=True):
        year = st.number_input("Year", value=2022)
        rnd = st.number_input("Round", value=1)
        circuit = st.number_input("Circuit ID", value=1)
        name = st.text_input("Name")
        time = st.time_input("Time")
        url = st.text_input("URL")
        submit_race = st.form_submit_button("Insert race")

        if submit_race:
            with SubmissionContext("Inserted race entry."):
                execute_sql(
                    conn,
                    INSERT_RACE,
                    year=year,
                    round=rnd,
                    circuitId=circuit,
                    name=name,
                    time=time,
                    url=url,
                )

elif add_selection == "Result":
    with st.form("Insert result", clear_on_submit=True):
        raceId = st.number_input("Race ID", value=1)
        driverId = st.number_input("Driver ID", value=1)
        constructorId = st.number_input("Constructor ID", value=1)
        number = st.number_input("Number", value=1)
        grid = st.number_input("Grid", value=1)
        position = st.number_input("Position", value=1)
        positionText = st.text_input("Position Text")
        positionOrder = st.number_input("Position Order", value=1)
        status = st.number_input("Status ID", value=1)
        laps = st.number_input("Laps", value=1)
        submit_result = st.form_submit_button("Insert result")

        if submit_result:
            with SubmissionContext("Inserted result entry."):
                execute_sql(
                    conn,
                    INSERT_RESULT,
                    raceId=raceId,
                    driverId=driverId,
                    constructorId=constructorId,
                    number=number,
                    grid=grid,
                    position=position,
                    positionText=positionText,
                    positionOrder=positionOrder,
                    statusId=status,
                    laps=laps
                )

elif add_selection == "Qualifier":
    with st.form("Insert qualifier", clear_on_submit=True):
        raceId = st.number_input("Race ID", value=1)
        driverId = st.number_input("Driver ID", value=1)
        constructorId = st.number_input("Constructor ID", value=1)
        number = st.number_input("Number", value=1)
        position = st.number_input("Position", value=1)

        q1 = col_layout_time("Q1")
        q2 = col_layout_time("Q2")
        q3 = col_layout_time("Q3")

        submit_qualifier = st.form_submit_button("Insert qualifier")
        if submit_qualifier:
            with SubmissionContext("Inserted qualifier entry."):
                execute_sql(
                    conn,
                    INSERT_QUALIFIER,
                    raceId=raceId,
                    driverId=driverId,
                    constructorId=constructorId,
                    number=number,
                    position=position,
                    q1=q1,
                    q2=q2,
                    q3=q3,
                )
