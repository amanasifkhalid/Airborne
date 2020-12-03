from scipy.stats import linregress

def linear_regression(cases, air_qualities):
    return linregress(cases, air_qualities)

def check_if_entry_exists(state, city, from_date, to_date):
    location = f"Location: {city}, {state}\n"
    start_date = f"Start Date: {from_date}\n"
    end_date = f"End Date: {to_date}\n"
    try:
        results_file = open("results.txt", "r")
    except:
        return False
    
    lines = results_file.readlines()
    return location in lines and start_date in lines and end_date in lines

def write_stats_to_file(data, state, city):
    from_date = data["Date"][0]
    to_date = data["Date"][-1]
    if check_if_entry_exists(state, city, from_date, to_date):
        return
    
    with open("results.txt", "a") as results_file:
        slope, y_intercept, corr_coef, p_value, std_error = \
            linear_regression(data["COVID-19 Cases"], data["Air Quality (PM2.5)"])
        coef_of_det = corr_coef ** 2

        results_file.write("==========================\n")
        results_file.write("Linear Regression Analysis\n")
        results_file.write(f"Location: {city}, {state}\n")
        results_file.write(f"Start Date: {from_date}\n")
        results_file.write(f"End Date: {to_date}\n")
        results_file.write(
            f"Equation: Air Quality = {slope} * COVID-19 Cases + {y_intercept}\n"
        )
        results_file.write(f"Pearson's Correlation Coefficient (R): {corr_coef}\n")
        results_file.write(f"Coefficient of Determination (R^2): {coef_of_det}\n")
        results_file.write(f"P-Value: {p_value}\n")
        results_file.write(f"Standard Error: {std_error}\n")

        results_file.write("==========================\n")
        results_file.write("\n")
