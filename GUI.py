import tkinter as tk
from tkinter import font
from tkinter import ttk
import sys

def welcome_GUI():
    root = tk.Tk()
    root.eval("tk::PlaceWindow . center")
    root.protocol("WM_DELETE_WINDOW", sys.exit)
    root.title("Airborne")
    welcome_font = font.Font(family="Courier", size=14)
    normal_font = font.Font(family="Roboto", size=12)
    small_font = font.Font(family="Roboto Condensed", size=10)
    tk.Label(root, text="Welcome to Airborne!", font=welcome_font).pack(pady=10, padx=10)
    choice = tk.IntVar()
    choice.set(1)

    tk.Label(root, text="What would you like to do?", font=normal_font).pack()
    tk.Radiobutton(root, text="Collect Data", font=small_font, variable=choice, value=1).pack()
    tk.Radiobutton(root, text="Analyze Data", font=small_font, variable=choice, value=0).pack()

    tk.Label(root).pack()

    tk.Button(root, text="Continue", font=normal_font, command=root.destroy).pack()
    tk.Button(root, text="Exit", font=normal_font, command=sys.exit).pack(pady=5)

    root.mainloop()
    return choice.get()

def selection_GUI(cur):
    root = tk.Tk()
    root.eval("tk::PlaceWindow . center")
    root.protocol("WM_DELETE_WINDOW", sys.exit)
    root.title("Airborne")
    normal_font = font.Font(family="Roboto", size=12)
    small_font = font.Font(family="Roboto Condensed", size=10)

    # Location selection
    cur.execute("SELECT state FROM Locations")
    locations = []
    for entry in cur.fetchall():
        locations.append(entry[0])
    
    tk.Label(root).pack()
    
    tk.Label(root, text="Please select a state:", font=normal_font).pack()
    loc_selection = tk.StringVar()
    loc_selection.set(locations[0])
    ttk.Combobox(root, width=15, textvariable=loc_selection,
                 values=locations, font=small_font).pack()
    
    tk.Label(root).pack()
    
    # Month selection
    cur.execute("SELECT month FROM Months")
    months = []
    for entry in cur.fetchall():
        months.append(entry[0])
    
    tk.Label(root, text="Please select a month:", font=normal_font).pack()
    month_selection = tk.StringVar()
    month_selection.set(months[0])
    ttk.Combobox(root, width=15, textvariable=month_selection, values=months, font=small_font).pack()

    clear_database = tk.IntVar()
    tk.Checkbutton(root, text="Clear database", variable=clear_database, font=small_font).pack(pady=20)
    tk.Button(root, text="Continue", font=normal_font, command=root.destroy).pack()
    warning_msg = "Note: Downloading the data will take time.\nDon't be alarmed if you don't see anything for a few seconds!"
    tk.Label(root, text=warning_msg, font=small_font).pack(padx=15, pady=10)

    root.mainloop()

    location = cur.execute("SELECT * FROM Locations WHERE state = ?",
                           (loc_selection.get(),)).fetchone()
    month = cur.execute("SELECT * FROM Months WHERE month = ?",
                        (month_selection.get(),)).fetchone()
    return location, month, clear_database.get()

def display_error_message(status_code, COVID_API=False):
    root = tk.Tk()
    root.eval("tk::PlaceWindow . center")
    root.protocol("WM_DELETE_WINDOW", sys.exit)
    root.title("Airborne")
    normal_font = font.Font(family="Roboto", size=12)
    error_font = font.Font(family="Courier", size=12)
    tk.Label(root, text="Oops...", font=normal_font).pack(pady=10)

    if COVID_API:
        error_API = "COVID-19"
    else:
        error_API = "OpenAQ"
    
    tk.Label(root, text=f"An error occurred while collecting the {error_API} data. Here's the server's response:", font=normal_font).pack(padx=15)
    tk.Label(root, text=status_code, font=error_font).pack()

    tk.Button(root, text="Exit", font=normal_font, command=sys.exit).pack(pady=20)
    root.mainloop()

def display_visualization_error_message():
    root = tk.Tk()
    root.eval("tk::PlaceWindow . center")
    root.protocol("WM_DELETE_WINDOW", sys.exit)
    root.title("Airborne")
    normal_font = font.Font(family="Roboto", size=12)
    tk.Label(root, text="Oops...", font=normal_font).pack(pady=10)

    tk.Label(root, text=f"No data is available yet!", font=normal_font).pack(padx=15)

    tk.Button(root, text="Exit", font=normal_font, command=root.destroy).pack(pady=20)
    root.mainloop()

def display_load_finished_message():
    root = tk.Tk()
    root.eval("tk::PlaceWindow . center")
    root.protocol("WM_DELETE_WINDOW", sys.exit)
    root.title("Airborne")
    normal_font = font.Font(family="Roboto", size=12)
    tk.Label(root, text="Data finished downloading!", font=normal_font).pack(padx=15, pady=10)
    tk.Button(root, text="Continue", font=normal_font, command=root.destroy).pack(pady=20)

    root.mainloop()

def select_state_visualization_GUI(cur):
    cur.execute("SELECT location_id FROM Air_Quality")
    avaliable_locs = cur.fetchall()
    cur.execute("SELECT id, state FROM Locations")
    states = []
    for entry in cur.fetchall():
        if (entry[0],) in avaliable_locs:
            states.append(entry[1])
    
    if not states:
        display_visualization_error_message()
        return None
    
    root = tk.Tk()
    root.eval("tk::PlaceWindow . center")
    root.protocol("WM_DELETE_WINDOW", sys.exit)
    root.title("Airborne")
    normal_font = font.Font(family="Roboto", size=12)
    small_font = font.Font(family="Roboto Condensed", size=10)

    tk.Label(root, text="Please select a state:", font=normal_font).pack(padx=15, pady=10)
    loc_selection = tk.StringVar()
    loc_selection.set(states[0])
    ttk.Combobox(root, width=15, textvariable=loc_selection,
                 values=states, font=small_font).pack()

    tk.Button(root, text="Continue", font=normal_font, command=root.destroy).pack(pady=20)

    root.mainloop()

    location = cur.execute("SELECT id FROM Locations WHERE state = ?",
                           (loc_selection.get(),)).fetchone()
    return location[0]

def select_month_visualization_GUI(cur, location_id):
    cur.execute("SELECT month_id FROM Air_Quality WHERE location_id = ?", (location_id,))
    available_months = cur.fetchall()
    cur.execute("SELECT id, month FROM Months")
    months = []
    for entry in cur.fetchall():
        if (entry[0],) in available_months:
            months.append(entry[1])
    
    root = tk.Tk()
    root.eval("tk::PlaceWindow . center")
    root.protocol("WM_DELETE_WINDOW", sys.exit)
    root.title("Airborne")
    normal_font = font.Font(family="Roboto", size=12)
    small_font = font.Font(family="Roboto Condensed", size=10)

    tk.Label(root, text="Please select a month:", font=normal_font).pack(pady=10)
    month_selection = tk.StringVar()
    month_selection.set(months[0])
    ttk.Combobox(root, width=15, textvariable=month_selection,
                 values=months, font=small_font).pack()
    
    use_all_data = tk.IntVar()
    tk.Checkbutton(root, text="Use all data available for location",
                   variable=use_all_data, font=small_font).pack(padx=15, pady=20)
    tk.Button(root, text="Continue", font=normal_font, command=root.destroy).pack(pady=20)

    root.mainloop()

    if use_all_data.get():
        return None
    
    month = cur.execute("SELECT id FROM Months WHERE month = ?",
                        (month_selection.get(),)).fetchone()
    return month[0]
