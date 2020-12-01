import matplotlib.pyplot as plt
import numpy as np

def air_quality_vs_cases(cases, air_qualities, city, state, from_month, to_month=None):
    plt.scatter(cases, air_qualities)
    trendline_eq = np.poly1d(np.polyfit(cases, air_qualities, 1))
    plt.plot(cases, trendline_eq(cases), "r")

    title = f"{city} Air Quality vs. New {state} COVID-19 Cases, {from_month}"
    if to_month:
        title = title + f"-{to_month}"
    
    title = title + " 2020"
    plt.title(title)
    plt.xlabel("New Daily COVID-19 Cases")
    plt.ylabel("Daily Air Quality (PM2.5)")
    plt.show()

def new_cases_line_graph(cases, dates, state, from_month, to_month=None):
    plt.plot(dates, cases)
    plt.show()