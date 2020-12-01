import sqlite3

MONTHS = (
    "March",
    "April",
    "May",
    "June",
)

def clear_API_data_tables(cur, conn):
    cur.execute("DROP TABLE IF EXISTS COVID_Cases")
    cur.execute("DROP TABLE IF EXISTS Air_Quality")
    set_up_COVID_table(cur)
    set_up_openAQ_table(cur)
    conn.commit()

def check_if_table_exists(cur, table_name):
    cur.execute(f"SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    return cur.fetchone()[0] == 1

def set_up_locations_table(cur):
    if check_if_table_exists(cur, "Locations"):
        return
    
    cur.execute("CREATE TABLE Locations (id INTEGER PRIMARY KEY, state TEXT, city TEXT, location TEXT)")
    with open("locations.txt", "r") as locations_file:
        count = 1
        for line in locations_file:
            location = tuple([count] + line.split(","))
            cur.execute("INSERT INTO Locations (id, state, city, location) VALUES (?, ?, ?, ?)", location)
            count += 1

def set_up_months_table(cur):
    if check_if_table_exists(cur, "Months"):
        return
    
    cur.execute("CREATE TABLE Months (id INTEGER PRIMARY KEY, month TEXT)")
    count = 3
    for month in MONTHS:
        cur.execute("INSERT INTO Months (id, month) VALUES (?, ?)", (count, month,))
        count += 1

def set_up_COVID_table(cur):
    cur.execute("""CREATE TABLE IF NOT EXISTS COVID_Cases
                   (date INTEGER KEY, month_id INTEGER, location_id INTEGER, new_cases INTEGER,
                   FOREIGN KEY (month_id) REFERENCES Months (id),
                   FOREIGN KEY (location_id) REFERENCES Locations (id),
                   UNIQUE(location_id, date))""")

def set_up_openAQ_table(cur):
    cur.execute("""CREATE TABLE IF NOT EXISTS Air_Quality
                   (date INTEGER KEY, month_id INTEGER, location_id INTEGER, average REAL,
                   FOREIGN KEY (month_id) REFERENCES Months (id),
                   FOREIGN KEY (location_id) REFERENCES Locations (id),
                   UNIQUE(location_id, date))""")

def set_up_tables():
    conn = sqlite3.connect("airborne_database.db")
    cur = conn.cursor()

    set_up_locations_table(cur)
    set_up_months_table(cur)
    set_up_COVID_table(cur)
    set_up_openAQ_table(cur)

    conn.commit()
    return conn, cur

def get_API_data_for_location(cur, location_id, month_id):
    if month_id:
        cur.execute("""SELECT COVID_Cases.date, COVID_Cases.month_id, new_cases, average FROM COVID_Cases
                       JOIN Air_Quality ON COVID_Cases.date = Air_Quality.date
                       AND COVID_Cases.location_id = Air_Quality.location_id
                       WHERE COVID_Cases.location_id = ? AND COVID_Cases.month_id = ?""",
                       (location_id, month_id,))
    else:
        cur.execute("""SELECT COVID_Cases.date, COVID_Cases.month_id, new_cases, average FROM COVID_Cases
                       JOIN Air_Quality ON COVID_Cases.date = Air_Quality.date
                       AND COVID_Cases.location_id = Air_Quality.location_id
                       WHERE COVID_Cases.location_id = ?""",
                       (location_id,))
    
    return cur.fetchall()
