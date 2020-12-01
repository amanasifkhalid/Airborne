import air_quality_api
import covid_api
import database
import GUI
import visualizations

def data_collection_driver(cur, conn):
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
    location_id = GUI.select_state_visualization_GUI(cur)
    if not location_id:
        return
    
    month_id = GUI.select_month_visualization_GUI(cur, location_id)
    API_data = database.get_API_data_for_location(cur, location_id, month_id)
    dates = []
    cases = []
    air_qualities = []
    for entry in API_data:
        dates.append(entry[0])
        cases.append(entry[2])
        air_qualities.append(entry[3])
    
    from_month = cur.execute("SELECT month FROM Months WHERE id = ?",
                             (API_data[0][1],)).fetchone()[0]
    to_month = cur.execute("SELECT month FROM Months WHERE id = ?",
                           (API_data[-1][1],)).fetchone()[0]
    
    location = cur.execute("SELECT state, city FROM Locations WHERE id = ?",
                           (location_id,)).fetchone()
    visualizations.air_quality_vs_cases(cases, air_qualities, location[0],
                                        location[1], from_month, to_month)

def main():
    conn, cur = database.set_up_tables()

    while True:
        choice = GUI.welcome_GUI()
        if choice:
            data_collection_driver(cur, conn)
        else:
            data_visualization_driver(cur)

if __name__ == "__main__":
    main()
