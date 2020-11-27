import matplotlib
import requests
import tkinter as tk
from tkinter import font
from tkinter import ttk

MONTHS = (
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
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
    root.geometry("250x250")
    root.eval("tk::PlaceWindow . center")
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

    continue_button = tk.Button(root, text="Continue", font=normal_font, command=root.quit).pack(pady=20)

    root.mainloop()
    return state.get(), month.get()

def main():
    locations = get_locations()
    selected_state, selected_month = selection_GUI(list(locations.keys()))

if __name__ == "__main__":
    main()
