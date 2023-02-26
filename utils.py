import streamlit as st
from sql import create_mysql_connection, get_names
from pymysql import Connection


@st.cache(allow_output_mutation=True)
def get_db_conn():
    return create_mysql_connection()


@st.cache(hash_funcs={Connection: id})
def get_names_cached(conn, query):
    return get_names(conn, query)
