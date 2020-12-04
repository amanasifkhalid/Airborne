airborne.py
def data_collection_driver(cur, conn):
    ''' Driver method for collecting data from COVID19 and Air Quality APIs. Takes the database cursor and connector as input. First runs the GUI for chosing the location
    and month. Formats month correctly so if smaller than 10, month would lead with a 0.  Calls methods for getting API data for 
    COIVD cases and Air Quality. If there is an error, than the GUI will display an error message. Then adds the data to airborne_database. 
    Lastly, GUI displays finished message.
    '''
def data_visualization_driver(cur):
    ''' Driver method for creating data visualizations. Takes in database cursor as input. First runs GUI for selecting the state.  IF there is no location_id available, the method returns
    Selects timeframe for the visualization. Gets data for selected location and month from airborne_database. Creates visualizations for the data and outputs linear regression results to a file'''
def main():
    '''Driver method for Airborne. First, connects to airborne_database and sets up the tables
    Starts welcome GUI, either collects data or creates data depending on users choice'''
    
covid_api.py
def get_daily_cases(state, date):
    '''Takes in state and date as inputs. Puts arguments into url. Try to make a get request from the url. If successful, returns the request. If not successful
    returns None.'''
    def add_to_COVID_database(data, date, location_id, cur, conn):
    '''Takes in data, date, location_id, database cursor and connector as inputs. Reformates month and date and extracts cases from API data
    Then, adds data to COVID_Cases table and commits to database connector'''
def API_driver(location, month, cur, conn):
    ''' Takes in location, month, database cursor and connector as inputs. Calls get daily cases for 25 days to get API data. Checks for errors in API response. If there are no errors,
    calls add_to_COVID_database and returns a tuple with just True. If there are errors, returns a tuple with False and the error message.'''    
    
air_quality_api.py
def get_monthly_cases(city, location, month):
    '''Takes in city, location, month as input. Puts arguments into url. Try to get request from url. If successful returns api response. If not successful returns None'''
def add_to_AQ_database(data, location_id, month, cur, conn):
    ''' Takes in data, location_id, month, database cursor and connector as inputs. Goes through api data by day. Records date, month, location, and air quality average.
    Inserts data into Air_Quality table and commits to database connector.'''
   def API_driver(location, month, cur, conn):
    ''' Takes in location, month, database cursor and connector as inputs. Calls get monthly cases to get API data. Checks for errors in API response. If there are no errors,
    calls add_to_AQ_database and returns a tuple with just True. If there are errors, returns a tuple with False and the error message.'''
     
processing.py
def linear_regression(cases, air_qualities):
    '''takes a list of cases and list of air_qualities as inputs. Returns the results of linear regression analysis performed
    by scipy.stats'''
 def check_if_entry_exists(state, city, from_date, to_date):
    ''' Takes state, city, from_date, to_date, as inputs for linear regression analysis. Tries to open results.txt and checks if
    there's already results for the inputs. Returns a boolean to avoid entering duplicate data'''
def write_stats_to_file(data, state, city):
    '''Takes data, state, and city where data is a dictionary of the cases, air qualities, and dates for the given state. First checks
    if there is already an entry in results.txt for these parameters and if not, performs linear regression analysis and records results.'''

visualization.py
def air_quality_vs_cases(data, state, city, from_month, to_month):
    ''' Takes data, state, city, from_month, and to_month as inputs, where
    data is a dictionary of the COVID-19 cases, the air qualities, and the dates.
    Creates a Pandas DataFrame of the data, formats a title for the graph, and
    then creates a scatterplot with a trend line using plotly.'''
def new_cases_line_graph(data, state, from_month, to_month):
    ''' Takes data, state, from_month, and to_month as inputs, where
    data is a dictionary of the COVID-19 cases, the air qualities, and the dates.
    Creates a Pandas DataFrame of data, and plots the DataFrame's COVID-19 cases
    column and Dates column on a line graph using plotly. Formats the title with
    state, from_month, and to_month; if from_month and to_month are equal, meaning
    the data is from one month, only display one month in the title. Else, display
    the month range in the title.'''
def air_quality_line_graph(data, city, from_month, to_month):
    ''' Takes data, city, from_month, and to_month as inputs, where
    data is a dictionary of the COVID-19 cases, the air qualities, and the dates.
    Creates a Pandas DataFrame of data, and plots the DataFrame's Air Quality
    column and Dates column on a line graph using plotly. Formats the title with
    city, from_month, and to_month; if from_month and to_month are equal, meaning
    the data is from one month, only display one month in the title. Else, display
    the month range in the title.'''
    
GUI.py

database.py
