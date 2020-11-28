import matplotlib
import requests
import sqlite3
import sys
import tkinter as tk
from tkinter import font
from tkinter import ttk

import covid_api

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

def selection_GUI(state_list):
    root = tk.Tk()
    root.eval("tk::PlaceWindow . center")
    root.protocol("WM_DELETE_WINDOW", sys.exit)
    root.title("Airborne")
    welcome_font = font.Font(family="Courier", size=14)
    normal_font = font.Font(family="Roboto", size=12)
    small_font = font.Font(family="Roboto Condensed", size=10)
    welcome_label = tk.Label(root, text="Welcome to Airborne!", font=welcome_font).pack(pady=10)

    # State selection
    state_label = tk.Label(root, text="Please select a state:", font=normal_font).pack()
    state = tk.StringVar()
    state.set(state_list[0])
    state_menu = ttk.Combobox(root, width=15, textvariable=state,
                              values=state_list, font=small_font).pack()
    
    spacing = tk.Label(root).pack()
    
    # Month selection
    month_label = tk.Label(root, text="Please select a month:", font=normal_font).pack()
    month = tk.StringVar()
    month.set(MONTHS[0])
    month_menu = ttk.Combobox(root, width=15, textvariable=month, values=MONTHS, font=small_font).pack()

    continue_button = tk.Button(root, text="Continue", font=normal_font, command=root.destroy).pack(pady=20)
    warning_msg = "Note: Downloading the data will take time.\nDon't be alarmed if you don't see anything for a few seconds!"
    warning_label = tk.Label(root, text=warning_msg, font=small_font).pack(padx=15, pady=10)

    root.mainloop()
    return state.get(), month.get()

def display_error_message(status_code, COVID_API=False):
    root = tk.Tk()
    root.eval("tk::PlaceWindow . center")
    root.protocol("WM_DELETE_WINDOW", sys.exit)
    root.title("Airborne")
    normal_font = font.Font(family="Roboto", size=12)
    error_font = font.Font(family="Courier", size=12)
    header_label = tk.Label(root, text="Oops...", font=normal_font).pack(pady=10)

    if COVID_API:
        error_API = "COVID-19"
    else:
        error_API = "OpenAQ"
    
    error_label = tk.Label(root, text=f"An error occurred while collecting the {error_API} data. Here's the server's response:", font=normal_font).pack(padx=15)
    response_abel = tk.Label(root, text=status_code, font=error_font).pack()

    exit_button = tk.Button(root, text="Exit", font=normal_font, command=root.destroy).pack(pady=20)
    root.mainloop()

def display_load_finished_message():
    root = tk.Tk()
    root.eval("tk::PlaceWindow . center")
    root.protocol("WM_DELETE_WINDOW", sys.exit)
    root.title("Airborne")
    normal_font = font.Font(family="Roboto", size=12)
    msg_label = tk.Label(root, text="Data finished downloading!", font=normal_font).pack(padx=15, pady=10)
    continue_button = tk.Button(root, text="Continue", font=normal_font, command=root.destroy).pack(pady=20)

    root.mainloop()

def check_if_table_exists(cur, table_name):
    cur.execute(f"SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    return cur.fetchone()[0] == 1

def set_up_locations_table(cur):
    if check_if_table_exists(cur, "Locations"):
        return
    
    cur.execute("CREATE TABLE Locations (id INTEGER PRIMARY KEY, state TEXT, city TEXT)")
    locations = get_locations()
    count = 1
    for state in locations:
        cur.execute("INSERT INTO Locations (id, state, city) VALUES (?, ?, ?)", (count, state, locations[state],))
        count += 1

def set_up_months_table(cur):
    if check_if_table_exists(cur, "Months"):
        return
    
    cur.execute("CREATE TABLE Months (id INTEGER PRIMARY KEY, month TEXT)")
    count = 4
    for month in MONTHS:
        cur.execute("INSERT INTO Months (id, month) VALUES (?, ?)", (count, month,))
        count += 1

def set_up_tables(cur, conn):
    set_up_locations_table(cur)
    set_up_months_table(cur)
    
    cur.execute("""CREATE TABLE IF NOT EXISTS COVID_Cases
                   (date INTEGER PRIMARY KEY, month_id INTEGER, location_id INTEGER, new_cases INTEGER,
                   FOREIGN KEY (month_id) REFERENCES Months (id),
                   FOREIGN KEY (location_id) REFERENCES Locations (id),
                   UNIQUE(date, location_id))""")
    cur.execute("""CREATE TABLE IF NOT EXISTS Air_Quality
                   (date INTEGER PRIMARY KEY, month_id INTEGER, location_id INTEGER, quality REAL,
                   FOREIGN KEY (month_id) REFERENCES Months (id),
                   FOREIGN KEY (location_id) REFERENCES Locations (id),
                   UNIQUE(date, location_id))""")
    conn.commit()

def main():
    # Connect to database
    conn = sqlite3.connect("airborne_database.db")
    cur = conn.cursor()
    set_up_tables(cur, conn)
    locations = get_locations()

    state, month = selection_GUI(list(locations.keys()))
    cur.execute("SELECT * FROM Locations WHERE state = ?", (state,))
    location = cur.fetchone()
    cur.execute("SELECT id FROM Months WHERE month = ?", (month,))
    month_num = cur.fetchone()[0]
    month = str(month_num)
    if month_num < 10:
        month = "0" + month

    COVID_status = covid_api.API_driver(location[1].lower(), location[0], month, cur, conn)
    if not COVID_status[0]:
        display_error_message(COVID_status[1], COVID_API=True)
        return
    
    # openAQ_status = air_quality_api.API_driver(location[2], month, cur, conn)
    # if not openAQ_status[0]:
    #     display_error_message(openAQ_status[1])
    #     return

    display_load_finished_message()

if __name__ == "__main__":
    main()
