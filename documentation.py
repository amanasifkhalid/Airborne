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
def welcome_GUI():
    ''' Creates and shows the first GUI the user sees upon running Airborne.
    Prompts the user to choose between collecting and analyzing data with radio
    buttons, and returns the user's choice as an integer. If the user picks
    "Analyze Data," 0 is returned. If the user picks "Collect Data," 1 is returned.'''
def selection_GUI(cur):
    ''' Takes a cursor to airborne_database.db as input and runs the GUI for
    selecting a state and month to collect API data for. The state and month
    dropdown menus are populated by selecting all available states and months
    from airborne_database.db. A check box is provided to clear airborne_database.db's
    COVID_Cases and Air_Quality tables. Once the user chooses to continue,
    the selected state and month, along with an integer determining whether to
    clear the COVID_Cases and Air_Quality tables, are returned.'''
def display_error_message(status_code, COVID_API=False):
    ''' Takes an error status code and an optional parameter specifying if the 
    API that failed is the COVID-19 API. Runs the GUI for notifying the user of
    any errors that occur while downloading, parsing, and saving API data to the
    database. If the API returns an HTTP status code, it will be shown. Else, one
    of Airborne's custom error messages will be shown. If the COVID-19 API fails,
    COVID_API will be specified as True.'''
def display_visualization_error_message():
    ''' Runs the GUI for displaying an error message if the user chooses to
    analyze data before collecting any; that is, if the user chooses "Analyze Data"
    from the welcome GUI when airborne_database.db's COVID_Cases and Air_Quality
    tables are empty, this error message GUI will run.'''
def display_load_finished_message():
    ''' Runs the GUI for notifying the user that the program has finished collecting
    data from the APIs without running into any errors.'''
def select_state_visualization_GUI(cur):
    ''' Takes a cursor pointing to airborne_database.db as input and prompts the
    user to select a state to analyze and create visualizations for. The state
    dropdown menu is populated by obtaining all location_ids with available data from
    Air_Quality, and then selecting their corresponding states from Locations using
    cur. If no data is available, an error message is displayed. When the user
    chooses to continue, the location_id of the selected state is returned.'''
def select_month_visualization_GUI(cur, location_id):
    ''' Takes a cursor pointing to airborne_database.db and the location_id of
    the state/city the user wishes to create visualizations for. Based on the
    selected location, the GUI prompts the user to select a time period of data
    to analyze. The month dropdown menu is populated by reading the available
    month_ids in the Air_Quality table using cur. If the corresponding checkbox
    is checked, all available data for the location will be used, and the returned
    month will be None. Another checkbox is provided to clear results.txt. A truthy
    integer will also be returned, its value dependent on if this box is checked.'''
def display_results_finished_message():
    ''' Displays a GUI notifying the user that the linear regression analysis
    performed on the data for the selected location and time frame has finished,
    and its results have been recorded in results.txt. This message pops up after
    all visualizations have been displayed.'''

database.py
def clear_API_data_tables(cur, conn):
    ''' Takes a cursor and connector to airborne_database.db as inputs, and
    drops the COVID_Cases and Air_Quality tables. Then, to re-setup these tables,
    calls set_up_COVID_table() and set_up_openAQ_table(). This method will be
    caled if the user specifies to clear these tables when collecting API data.'''
def check_if_table_exists(cur, table_name):
    ''' Takes a cursor to airborne_database.db and a table name as inputs, and
    uses the cursor to execute a SQL command to select all tables named table_name.
    Returns a boolean specifying if a table with table_name was found.'''
def set_up_locations_table(cur):
    ''' Takes a cursor to airborne_database.db as input, and creates the Locations
    table, assuming it doesn't already exist. The Locations table provides an
    id, state, city, and location (where air quality is specifically read from)
    for each entry. Supported locations are read into the table from locations.txt.'''
def set_up_months_table(cur):
    ''' Takes a cursor to airborne_database.db as input, and creates the Months
    table, assuming it doesn't already exist. The Months table provides an id and
    month name for each entry. Supported months are read into the table from
    months.txt. The first line in months.txt is an integer specifying what id
    should start counting from, and should be the number of the first supported
    month in the file.'''
def set_up_COVID_table(cur):
    ''' Takes a cursor to airborne_database.db as input, and creates the COVID_Cases
    table. The COVID_Cases table provides date, month_id, location_id, and
    new_cases attributes for each entry, where new_cases is the number of new
    COVID-19 cases on that day. month_id and location_id are foreign keys
    referencing the id attributes of the Months and Locations tables, respectively.
    This table requires that each entry's location_id and date pairing is
    unique in order to avoid entering duplicate data.'''
def set_up_openAQ_table(cur):
    ''' Takes a cursor to airborne_database.db as input, and creates the Air_Quality
    table. the Air_Quality table provides date, month_id, location_id, and average
    attributes for each entry, where average is the average PM2.5 present in the
    air on that day. month_id and location_id are foreign keys referencing the
    id attributes of the Months and Locations tables, respectively. This table
    requires that each entry's location_id and date pairing is unique in order
    to avoid entering duplicate data.'''
def set_up_tables():
    ''' Driver method for setting up airborne_database.db's tables. Creates a
    connector and cursor for the database, and calls the setup methods for each
    table. Commits these changes, and returns the connector and cursor to main()
    in airborne.py.'''
def get_API_data_for_location(cur, location_id, month_id):
    ''' Takes a cursor pointing to airborne_database.db, a location_id, and a
    month_id as inputs, and selects all data corresponding to location_id and
    month_id from the joined COVID_Cases and Air_Quality tables. If month_id is
    None, then all data corresponding to location_id, regardless of month, is
    selected. Each entry in the selected data contains the date, month_id, new_cases,
    and average attribute. This data is returned as a list of tuples.'''
