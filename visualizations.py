import matplotlib.pyplot as plt
import numpy as np

def get_correlation_coefficient(cases, air_qualities):
    r = np.corrcoef(np.array(cases), np.array(air_qualities))
    return r[0, 1]

def air_quality_vs_cases(cases, air_qualities, state, city, from_month, to_month):
    plt.scatter(cases, air_qualities)
    trendline_eq = np.poly1d(np.polyfit(cases, air_qualities, 1))
    plt.plot(cases, trendline_eq(cases), "r")

    title = f"{city} Air Quality vs. New {state} COVID-19 Cases,\n{from_month}"
    if to_month != from_month:
        title = title + f"-{to_month}"
    
    title = title + " 2020"
    plt.title(title)
    plt.xlabel("New Daily COVID-19 Cases")
    plt.ylabel("Daily Air Quality (PM2.5)")

    corr_coef = get_correlation_coefficient(cases, air_qualities)
    coef_of_det = corr_coef ** 2
    plt.legend([f"R: {round(corr_coef, 2)}\nR^2: {round(coef_of_det, 2)}"])
    plt.show()

def new_cases_line_graph(cases, dates, state, from_month, to_month=None):
    plt.plot(dates, cases)
    plt.show()