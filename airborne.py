import air_quality_api
import covid_api
import database
import GUI
import processing
import visualizations

def data_collection_driver(cur, conn):
    ''' Driver method for collecting data from COVID19 and Air Quality APIs. Takes the database cursor and connector as input. First runs the GUI for chosing the location
    and month. Formats month correctly so if smaller than 10, month would lead with a 0.  Calls methods for getting API data for 
    COIVD cases and Air Quality. If there is an error, than the GUI will display an error message. Then adds the data to airborne_database. 
    Lastly, GUI displays finished message.
    '''
    location, month, clear_API_data = GUI.selection_GUI(cur)
    if clear_API_data:
        database.clear_API_data_tables(cur, conn)
    
    month_num = month[0]
    if month_num < 10:
        month_num = "0" + str(month_num)
    else:
        month_num = str(month_num)

    COVID_status = covid_api.API_driver(location, month_num, cur, conn)
    if not COVID_status[0]:
        GUI.display_error_message(COVID_status[1], COVID_API=True)
        return
    
    openAQ_status = air_quality_api.API_driver(location, month_num, cur, conn)
    if not openAQ_status[0]:
        GUI.display_error_message(openAQ_status[1])
        return

    GUI.display_load_finished_message()

def data_visualization_driver(cur):
    ''' Driver method for creating data visualizations. Takes in database cursor as input. First runs GUI for selecting the state.  IF there is no location_id available, the method returns
    Selects timeframe for the visualization. Gets data for selected location and month from airborne_database. Creates visualizations for the data and outputs linear regression results to a file'''
    location_id = GUI.select_state_visualization_GUI(cur)
    if not location_id:
        return
    
    month_id = GUI.select_month_visualization_GUI(cur, location_id)
    API_data = database.get_API_data_for_location(cur, location_id, month_id)
    data_dict = dict()
    data_dict["Date"] = []
    data_dict["COVID-19 Cases"] = []
    data_dict["Air Pollution (PM2.5)"] = []
    for entry in API_data:
        date = str(entry[0])
        date = f"{date[:4]}-{date[4:6]}-{date[6:]}"
        data_dict["Date"].append(date)
        data_dict["COVID-19 Cases"].append(entry[2])
        data_dict["Air Pollution (PM2.5)"].append(entry[3])
    
    from_month = cur.execute("SELECT month FROM Months WHERE id = ?",
                             (API_data[0][1],)).fetchone()[0]
    to_month = cur.execute("SELECT month FROM Months WHERE id = ?",
                           (API_data[-1][1],)).fetchone()[0]
    
    location = cur.execute("SELECT state, city FROM Locations WHERE id = ?",
                           (location_id,)).fetchone()
    visualizations.air_quality_vs_cases(data_dict, location[0],
                                        location[1], from_month, to_month)
    visualizations.new_cases_line_graph(data_dict, location[0], from_month, to_month)
    visualizations.air_quality_line_graph(data_dict, location[1], from_month, to_month)
    processing.write_stats_to_file(data_dict, location[0], location[1])

def main():
    '''Driver method for Airborne. First, connects to airborne_database and sets up the tables
    Starts welcome GUI, either collects data or creates data depending on users choice'''
    conn, cur = database.set_up_tables()

    while True:
        choice = GUI.welcome_GUI()
        if choice:
            data_collection_driver(cur, conn)
        else:
            data_visualization_driver(cur)

if __name__ == "__main__":
    main()
