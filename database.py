def clear_API_data_tables(cur, conn):
    cur.execute("DROP TABLE IF EXISTS COVID_Cases")
    cur.execute("DROP TABLE IF EXISTS Air_Quality")
    conn.commit()

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
                   (date INTEGER PRIMARY KEY, month_id INTEGER, location_id INTEGER, average REAL,
                   FOREIGN KEY (month_id) REFERENCES Months (id),
                   FOREIGN KEY (location_id) REFERENCES Locations (id),
                   UNIQUE(date, location_id))""")
    conn.commit()