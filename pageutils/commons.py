import streamlit as st
from sql import IntegrityError
import time
import re


def nonify(func):
    def wrapper(inp):
        if inp is None:
            return None
        return func(inp)

    return wrapper


@nonify
def race_formatter(race):
    return race.split("__")[1] + " " + race.split("__")[2]


@nonify
def race_identifier(race):
    return int(race.split("__")[0])


@nonify
def driver_formatter(driver):
    return driver.split("__")[1]


@nonify
def driver_identifier(driver):
    return int(driver.split("__")[0])


@nonify
def constructor_formatter(constructor):
    return constructor.split("__")[1]


@nonify
def constructor_identifier(constructor):
    return int(constructor.split("__")[0])


@nonify
def status_formatter(status):
    return status.split("__")[1]


@nonify
def status_identifier(status):
    return int(status.split("__")[0])


class SubmissionContext:
    def __init__(self, success_msg="Success!"):
        self.success_msg = success_msg

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, exc_tb):
        if exc_type is None:
            st.success(self.success_msg)
            time.sleep(1)
            st.experimental_rerun()
            return True

        if isinstance(exc_value, IntegrityError):
            if "Cannot delete or update" in str(exc_value) and "FOREIGN KEY" in str(exc_value):
                pat = re.compile("FOREIGN KEY \((\S+)\)")
                attr = pat.search(str(exc_value)).group(1)
                st.error(f"Cannot modify {attr} when it has existing references")
                return True
            if "FOREIGN KEY" in str(exc_value):
                pat = re.compile("FOREIGN KEY \((\S+)\)")
                attr = pat.search(str(exc_value)).group(1)
                st.error(f"No existing references available for the value of {attr}")
                return True
            elif "Duplicate entry" in str(exc_value):
                st.error(str(exc_value).split(",")[1][:-1])
                return True
