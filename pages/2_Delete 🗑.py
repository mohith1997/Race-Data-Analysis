import streamlit as st
from utils import get_db_conn
from pageutils.commons import *
from sql import *

st.set_page_config(page_title="Delete Data", page_icon="🗑")

conn = get_db_conn()
races = get_names(conn, RACE_NAMES)
drivers = get_names(conn, DRIVER_NAMES)
constructors = get_names(conn, CONSTR_NAMES)

delete_selection = st.sidebar.selectbox(
    "Select data", ["Results", "Qualifier", "Constructor Results", "Season"]
)

if delete_selection == "Results":
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
    result_ids = map(lambda x: x["resultId"], filtered_data)

    with st.form("Result delete", clear_on_submit=True):
        result_id = st.selectbox("Select ID from above to delete", result_ids)
        submit = st.form_submit_button("Delete")
        if submit:
            with SubmissionContext("Deleted result"):
                execute_sql(conn, DEL_RESULT, resultId=result_id)

elif delete_selection == "Qualifier":
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

    qualify_ids = map(lambda x: x["qualifyId"], filtered_data)

    with st.form("Qualifier delete", clear_on_submit=True):
        qualify_id = st.selectbox("Select ID from above to delete", qualify_ids)
        submit = st.form_submit_button("Delete")
        if submit:
            with SubmissionContext("Deleted qualifier"):
                execute_sql(conn, DEL_QUALIFIER, qualifyId=qualify_id)

elif delete_selection == "Constructor Results":
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
        conn, CONSTRUCTOR_RESULT_FILTER, raceId=race_id, constructorId=constructor_id
    )
    st.dataframe(filtered_data, use_container_width=True)

    constructor_res_ids = map(lambda x: x["constructorResultsId"], filtered_data)
    with st.form("Constructor delete", clear_on_submit=True):
        constructor_res_id = st.selectbox(
            "Select ID from above to delete", constructor_res_ids
        )
        submit = st.form_submit_button("Delete")
        if submit:
            with SubmissionContext("Deleted constructor"):
                execute_sql(
                    conn, DEL_CONSTRUCTOR, constructorResultsId=constructor_res_id
                )

elif delete_selection == "Season":
    filtered_data = read_sql(conn, "select * from seasons")

    st.dataframe(filtered_data, use_container_width=True)

    years = map(lambda x: x["year"], filtered_data)

    with st.form("Season delete", clear_on_submit=True):
        year = st.selectbox("Select year from above to delete", years)
        submit = st.form_submit_button("Delete")
        if submit:
            with SubmissionContext("Deleted session"):
                execute_sql(conn, DEL_SEASON, year=year)
