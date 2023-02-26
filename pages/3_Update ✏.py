import streamlit as st
from utils import get_db_conn
from pageutils.commons import *
from sql import *

st.set_page_config(page_title="Update Data", page_icon="✏")

conn = get_db_conn()
statuses = get_names(conn, STATUS_NAMES)

update_selection = st.sidebar.selectbox(
    "Select item to update", ["Result status", "Constructor status", "Point table"]
)


if update_selection == "Result status":
    res_id = st.number_input("Result ID", value=1)
    result_selected = read_sql(conn, RESULT_WITH_STATUS_BY_ID, resultId=res_id)

    if result_selected:
        with st.form("Result status"):
            result_selected = result_selected[0]
            default = (
                str(result_selected["statusId"]) + "__" + result_selected["status"]
            )
            defaultidx = statuses.index(default)
            result_status = st.selectbox(
                "Status",
                index=defaultidx,
                options=statuses,
                format_func=status_formatter,
            )
            result_status = status_identifier(result_status)

            submit_result = st.form_submit_button("Update")
            if submit_result:
                with SubmissionContext("Updated status"):
                    execute_sql(
                        conn,
                        UPDATE_RESULT_STATUS,
                        statusId=result_status,
                        resultId=result_selected["resultId"],
                    )

    else:
        st.error("Requested data not available")

elif update_selection == "Constructor status":
    constructor_res_id = st.number_input("Constructor result ID", value=1)
    constructor_selected = read_sql(
        conn, CONSTRUCTOR_RESULT_BY_ID, constructorResultsId=constructor_res_id
    )

    if constructor_selected:
        with st.form("Constructor Status"):
            constructor_selected = constructor_selected[0]
            constructor_status = st.text_input(
                "Status", value=constructor_selected["status"]
            )

            submit_const = st.form_submit_button("Update")
            if submit_const:
                with SubmissionContext("Updated status"):
                    execute_sql(
                        conn,
                        UPDATE_CONSTRUCTOR_STATUS,
                        status=constructor_status,
                        constructorResultsId=constructor_selected[
                            "constructorResultsId"
                        ],
                    )

    else:
        st.error("Requested data not available")

elif update_selection == "Point table":
    year = st.number_input("Year", value=2016)
    position = st.number_input("Position", value=1, min_value=1, max_value=10)
    points_selected = read_sql(conn, POINTS_FILTER, year=year, position=position)

    if points_selected:
        with st.form("Points"):

            points_selected = points_selected[0]
            points = st.number_input("Points", value=points_selected["points"])
            fastestlap = st.checkbox("Fastest Lap", value=points_selected["fastestlap"])

            submit_pts = st.form_submit_button("Update")
            if submit_pts:
                with SubmissionContext("Updated points"):
                    execute_sql(
                        conn,
                        UPDATE_POINTS,
                        points=points,
                        fastestlap=fastestlap,
                        id=points_selected["id"],
                    )

    else:
        st.error("Requested data not available")
