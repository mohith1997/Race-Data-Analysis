import streamlit as st
from utils import get_db_conn
from pageutils.commons import *
from sql import *

st.set_page_config(page_title="Result Viewer", page_icon="🔍")

conn = get_db_conn()
races = get_names(conn, RACE_NAMES)
drivers = get_names(conn, DRIVER_NAMES)
constructors = get_names(conn, CONSTR_NAMES)
seasons = get_names(conn, SEASON_NAMES)

view_selection = st.sidebar.selectbox("Select data to view", ["Results", "Standings"])


if view_selection == "Results":
    res_selection = st.sidebar.selectbox(
        "Select results", ["Race", "Qualifier", "Constructor"]
    )

    if res_selection == "Race":
        race_select = st.sidebar.selectbox(
            "Select race", options=[None] + races, format_func=race_formatter
        )
        race_id = race_identifier(race_select)
        driver_select = st.sidebar.selectbox(
            "Select driver", options=[None] + drivers, format_func=driver_formatter
        )
        driver_id = driver_identifier(driver_select)
        constructor_select = st.sidebar.selectbox(
            "Select constructor",
            options=[None] + constructors,
            format_func=constructor_formatter,
        )
        constructor_id = constructor_identifier(constructor_select)

        filtered_data = read_sql(
            conn,
            RESULT_FILTER,
            raceId=race_id,
            driverId=driver_id,
            constructorId=constructor_id,
        )
        st.dataframe(filtered_data, use_container_width=True)

    elif res_selection == "Qualifier":
        race_select = st.sidebar.selectbox(
            "Select race", options=[None] + races, format_func=race_formatter
        )
        race_id = race_identifier(race_select)
        driver_select = st.sidebar.selectbox(
            "Select driver", options=[None] + drivers, format_func=driver_formatter
        )
        driver_id = driver_identifier(driver_select)
        constructor_select = st.sidebar.selectbox(
            "Select constructor",
            options=[None] + constructors,
            format_func=constructor_formatter,
        )
        constructor_id = constructor_identifier(constructor_select)

        filtered_data = read_sql(
            conn,
            QUALIFY_FILTER,
            raceId=race_id,
            driverId=driver_id,
            constructorId=constructor_id,
        )
        st.dataframe(filtered_data, use_container_width=True)

    elif res_selection == "Constructor":
        race_select = st.sidebar.selectbox(
            "Select race", options=[None] + races, format_func=race_formatter
        )
        race_id = race_identifier(race_select)
        constructor_select = st.sidebar.selectbox(
            "Select constructor",
            options=[None] + constructors,
            format_func=constructor_formatter,
        )
        constructor_id = constructor_identifier(constructor_select)

        filtered_data = read_sql(
            conn,
            CONSTRUCTOR_RESULT_FILTER,
            raceId=race_id,
            constructorId=constructor_id,
        )
        st.dataframe(filtered_data, use_container_width=True)

elif view_selection == "Standings":
    stand_selection = st.sidebar.selectbox(
        "Select standings", ["Driver", "Constructor"]
    )
    if stand_selection == "Driver":
        season_select = st.sidebar.selectbox("Select season", options=seasons)
        filtered_data = read_sql(conn, DRIVER_STANDINGS, year=season_select)
        st.dataframe(filtered_data, use_container_width=True)

    elif stand_selection == "Constructor":
        season_select = st.sidebar.selectbox("Select season", options=seasons)
        filtered_data = read_sql(conn, CONSTRUCTOR_STANDINGS, year=season_select)
        st.dataframe(filtered_data, use_container_width=True)
