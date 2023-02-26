import streamlit as st


def col_layout_time(subject):
    st.caption(subject)
    c1, c2, c3 = st.columns(3)

    with c1:
        minute = st.number_input(
            "Minutes", min_value=0, max_value=59, key=subject + "_min"
        )
    with c2:
        second = st.number_input(
            "Seconds", min_value=0, max_value=59, key=subject + "_sec"
        )
    with c3:
        millisec = st.number_input(
            "Milli seconds", min_value=0, max_value=999, key=subject + "_ms"
        )

    # get formatted string
    time_str = "{:0>2d}:{:0>2d}:{:d}".format(minute, second, millisec)
    return time_str
