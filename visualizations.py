import pandas as pd
import plotly.express as px

def air_quality_vs_cases(data, state, city, from_month, to_month):
    ''' Takes data, state, city, from_month, and to_month as inputs, where
    data is a dictionary of the COVID-19 cases, the air qualities, and the dates.
    Creates a Pandas DataFrame of the data, formats a title for the graph, and
    then creates a scatterplot with a trend line using plotly.'''
    df = pd.DataFrame(data=data)
    title = f"{city} Daily Air Quality vs. New {state} COVID-19 Cases,\n{from_month}"
    if to_month != from_month:
        title = title + f"-{to_month}"
    
    title = title + " 2020"
    scatter = px.scatter(df, x="COVID-19 Cases", y="Air Pollution (PM2.5)",
                         title=title, hover_name="Date", trendline="ols")
    scatter.show()

def new_cases_line_graph(data, state, from_month, to_month):
    ''' Takes data, state, from_month, and to_month as inputs, where
        data is a dictionary of the COVID-19 cases, the air qualities, and the dates.
        Creates a Pandas DataFrame of data, and plots the DataFrame's COVID-19 cases
        column and Dates column on a line graph using plotly. Formats the title with
        state, from_month, and to_month; if from_month and to_month are equal, meaning
        the data is from one month, only display one month in the title. Else, display
        the month range in the title.'''
    df =pd.DataFrame(data=data)
    # df = px.data.gapminder().query("state=='state'")
    title = f"{state} COVID-19 cases for {from_month}"
    if to_month !=from_month:
        title = title + f"- {to_month}"
        
    title = title + " 2020"
    line = px.line(df, x="Dates", y="COVID cases", title=title)
    line.show()
    
def air_quality_line_graph(data, city, from_month, to_month):
    ''' Takes data, city, from_month, and to_month as inputs, where
    data is a dictionary of the COVID-19 cases, the air qualities, and the dates.
    Creates a Pandas DataFrame of data, and plots the DataFrame's Air Quality
    column and Dates column on a line graph using plotly. Formats the title with
    city, from_month, and to_month; if from_month and to_month are equal, meaning
    the data is from one month, only display one month in the title. Else, display
    the month range in the title.'''
    df =pd.DataFrame(data=data)
    title = f"{city} Air Pollution (PM2.5) for {from_month}"
    if to_month !=from_month:
        title = title + f"- {to_month}"
        
    title = title + " 2020"
    line = px.line(df, x="Dates", y="Air Polution (PM2.5) ", title=title)
    line.show()
