import streamlit as st
from utils import get_db_conn
from pageutils.commons import *
from pageutils.plotter import *
from sql import *

st.set_page_config(page_title="Plot Data", page_icon="📈")

conn = get_db_conn()
races = get_names(conn, RACE_NAMES)
drivers = get_names(conn, DRIVER_NAMES)
constructors = get_names(conn, CONSTR_NAMES)
seasons = get_names(conn, SEASON_NAMES)

plot_selection = st.sidebar.selectbox("Select plot type", ["Lapstats", "Racestats"])


if plot_selection == "Lapstats":
    race_select = st.sidebar.selectbox(
        "Select race", options=[None] + races, format_func=race_formatter
    )
    race_id = race_identifier(race_select)
    driver_select = st.sidebar.selectbox(
        "Select driver", options=[None] + drivers, format_func=driver_formatter
    )
    driver_id = driver_identifier(driver_select)

    if race_id and driver_id:
        st.header(f"Lap statistics of {driver_formatter(driver_select)}")
        filtered_data = read_sql(
            conn, LAPTIME_STATS, raceId=race_id, driverId=driver_id
        )
        if filtered_data:
            st.line_chart(filtered_data, x="lap", y="seconds", use_container_width=True)
            st.line_chart(
                filtered_data, x="lap", y="position", use_container_width=True
            )
        else:
            st.error("Requested data not available")

elif plot_selection == "Racestats":
    season_select = st.sidebar.selectbox("Select season", options=seasons)
    driver_select = st.sidebar.selectbox(
        "Select driver", options=[None] + drivers, format_func=driver_formatter
    )
    driver_id = driver_identifier(driver_select)
    season_select = int(season_select)

    if season_select and driver_id:
        st.header(f"Race statistics of {driver_formatter(driver_select)}")
        filtered_data = read_sql(
            conn, RACE_STATS, seasonId=season_select, driverId=driver_id
        )
        st.subheader("Position across races")
        if filtered_data:
            st.altair_chart(
                rank_plot(filtered_data, x="raceId", y="positionOrder"),
                use_container_width=True,
                theme="streamlit",
            )

            st.subheader("Lap times across races")
            st.area_chart(
                filtered_data,
                x="raceId",
                y=[ "slowestLapTime", "avgLapTime", "fastestLapTime"],
            )
        else:
            st.error("Requested data not available")
