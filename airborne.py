import air_quality_api
import covid_api
import database
import GUI
import visualizations

def main():
    conn, cur = database.set_up_tables()

    while True:
        choice = GUI.welcome_GUI()
        if choice:
            data_collection_driver(cur, conn)
        else:
            data_visualization_driver(cur)

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

    # API_data = database.get_API_data_for_location(cur, location[0], int(month_num))
    # dates = []
    # new_cases = []
    # air_qualities = []
    # for entry in API_data:
    #     dates.append(entry[0])
    #     new_cases.append(entry[1])
    #     air_qualities.append(entry[2])
    
    # visualizations.air_quality_vs_cases(new_cases, air_qualities, location[2], location[1], month[1])

def data_visualization_driver(cur):
    location_id = GUI.select_state_visualization_GUI(cur)
    if not location_id:
        return
    
    month_id = GUI.select_month_visualization_GUI(cur, location_id)

if __name__ == "__main__":
    main()
