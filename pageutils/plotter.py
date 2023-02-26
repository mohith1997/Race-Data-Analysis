import altair as alt
import pandas as pd


def rank_plot(data, x, y):
    data = pd.DataFrame.from_dict(data)
    c = (
        alt.Chart(data)
        .mark_line(point=True)
        .encode(x="raceId", y=alt.Y("positionOrder", sort="descending"))
    )
    return c
