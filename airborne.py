import matplotlib.pyplot as plt
import requests
import sqlite3

import air_quality_api
import covid_api
import database
import GUI

MONTHS = (
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November"
)

def get_locations():
    with open("locations.txt", "r") as locations_file:
        locations_dict = dict()
        for line in locations_file:
            location = line.split(",")
            locations_dict[location[0]] = location[1]
        return locations_dict

def main():
    # Connect to database
    conn = sqlite3.connect("airborne_database.db")
    cur = conn.cursor()

    locations = get_locations()
    state, month, clear_API_data = GUI.selection_GUI(list(locations.keys()), MONTHS, cur, conn)
    if clear_API_data:
        database.clear_API_data_tables()
    
    database.set_up_tables(cur, conn)

    cur.execute("SELECT * FROM Locations WHERE state = ?", (state,))
    location = cur.fetchone()
    cur.execute("SELECT id FROM Months WHERE month = ?", (month,))
    month_num = cur.fetchone()[0]
    month = str(month_num)
    if month_num < 10:
        month = "0" + month

    COVID_status = covid_api.API_driver(location[1].lower(), location[0], month, cur, conn)
    if not COVID_status[0]:
        GUI.display_error_message(COVID_status[1], COVID_API=True)
        return
    
    openAQ_status = air_quality_api.API_driver(location[2].strip(), location[0], month, cur, conn)
    if not openAQ_status[0]:
        GUI.display_error_message(openAQ_status[1])
        return

    GUI.display_load_finished_message()

if __name__ == "__main__":
    main()
