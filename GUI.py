import tkinter as tk
from tkinter import font
from tkinter import ttk
import sys

def selection_GUI(state_list, month_list, cur, conn):
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
    month.set(month_list[0])
    month_menu = ttk.Combobox(root, width=15, textvariable=month, values=month_list, font=small_font).pack()

    clear_database = tk.IntVar()
    database_check = tk.Checkbutton(root, text="Clear database", variable=clear_database, font=small_font).pack(pady=20)
    continue_button = tk.Button(root, text="Continue", font=normal_font, command=root.destroy).pack()
    warning_msg = "Note: Downloading the data will take time.\nDon't be alarmed if you don't see anything for a few seconds!"
    warning_label = tk.Label(root, text=warning_msg, font=small_font).pack(padx=15, pady=10)

    root.mainloop()

    return state.get(), month.get(), clear_database.get()

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
    response_label = tk.Label(root, text=status_code, font=error_font).pack()

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