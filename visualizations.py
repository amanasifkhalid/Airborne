import pandas as pd
import plotly.express as px

def air_quality_vs_cases(data, state, city, from_month, to_month):
    df = pd.DataFrame(data=data)
    title = f"{city} Daily Air Quality vs. New {state} COVID-19 Cases,\n{from_month}"
    if to_month != from_month:
        title = title + f"-{to_month}"
    
    title = title + " 2020"
    scatter = px.scatter(df, x="COVID-19 Cases", y="Air Quality (PM2.5)",
                         title=title, hover_name="Date", trendline="ols")
    scatter.show()

def new_cases_line_graph(cases, dates, state, from_month, to_month=None):
    pass