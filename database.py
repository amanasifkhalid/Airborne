import sqlite3

def clear_API_data_tables(cur, conn):
    ''' Takes a cursor and connector to airborne_database.db as inputs, and
    drops the COVID_Cases and Air_Quality tables. Then, to re-setup these tables,
    calls set_up_COVID_table() and set_up_openAQ_table(). This method will be
    caled if the user specifies to clear these tables when collecting API data.'''
    cur.execute("DROP TABLE IF EXISTS COVID_Cases")
    cur.execute("DROP TABLE IF EXISTS Air_Quality")
    set_up_COVID_table(cur)
    set_up_openAQ_table(cur)
    conn.commit()

def check_if_table_exists(cur, table_name):
    ''' Takes a cursor to airborne_database.db and a table name as inputs, and
    uses the cursor to execute a SQL command to select all tables named table_name.
    Returns a boolean specifying if a table with table_name was found.'''
    cur.execute(f"SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    return cur.fetchone()[0] == 1

def set_up_locations_table(cur):
    ''' Takes a cursor to airborne_database.db as input, and creates the Locations
    table, assuming it doesn't already exist. The Locations table provides an
    id, state, city, and location (where air quality is specifically read from)
    for each entry. Supported locations are read into the table from locations.txt.'''
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
    ''' Takes a cursor to airborne_database.db as input, and creates the Months
    table, assuming it doesn't already exist. The Months table provides an id and
    month name for each entry. Supported months are read into the table from
    months.txt. The first line in months.txt is an integer specifying what id
    should start counting from, and should be the number of the first supported
    month in the file.'''
    if check_if_table_exists(cur, "Months"):
        return
    
    cur.execute("CREATE TABLE Months (id INTEGER PRIMARY KEY, month TEXT)")
    count = 3
    with open("months.txt", "r") as months_file:
        count = int(months_file.readline())
        for line in months_file.readlines():
            cur.execute("INSERT INTO Months (id, month) VALUES (?, ?)", (count, line.strip(),))
            count += 1

def set_up_COVID_table(cur):
    ''' Takes a cursor to airborne_database.db as input, and creates the COVID_Cases
    table. The COVID_Cases table provides date, month_id, location_id, and
    new_cases attributes for each entry, where new_cases is the number of new
    COVID-19 cases on that day. month_id and location_id are foreign keys
    referencing the id attributes of the Months and Locations tables, respectively.
    This table requires that each entry's location_id and date pairing is
    unique in order to avoid entering duplicate data.'''
    cur.execute("""CREATE TABLE IF NOT EXISTS COVID_Cases
                   (date INTEGER KEY, month_id INTEGER, location_id INTEGER, new_cases INTEGER,
                   FOREIGN KEY (month_id) REFERENCES Months (id),
                   FOREIGN KEY (location_id) REFERENCES Locations (id),
                   UNIQUE(location_id, date))""")

def set_up_openAQ_table(cur):
    ''' Takes a cursor to airborne_database.db as input, and creates the Air_Quality
    table. the Air_Quality table provides date, month_id, location_id, and average
    attributes for each entry, where average is the average PM2.5 present in the
    air on that day. month_id and location_id are foreign keys referencing the
    id attributes of the Months and Locations tables, respectively. This table
    requires that each entry's location_id and date pairing is unique in order
    to avoid entering duplicate data.'''
    cur.execute("""CREATE TABLE IF NOT EXISTS Air_Quality
                   (date INTEGER KEY, month_id INTEGER, location_id INTEGER, average REAL,
                   FOREIGN KEY (month_id) REFERENCES Months (id),
                   FOREIGN KEY (location_id) REFERENCES Locations (id),
                   UNIQUE(location_id, date))""")

def set_up_tables():
    ''' Driver method for setting up airborne_database.db's tables. Creates a
    connector and cursor for the database, and calls the setup methods for each
    table. Commits these changes, and returns the connector and cursor to main()
    in airborne.py.'''
    conn = sqlite3.connect("airborne_database.db")
    cur = conn.cursor()

    set_up_locations_table(cur)
    set_up_months_table(cur)
    set_up_COVID_table(cur)
    set_up_openAQ_table(cur)

    conn.commit()
    return conn, cur

def get_API_data_for_location(cur, location_id, month_id):
    ''' Takes a cursor pointing to airborne_database.db, a location_id, and a
    month_id as inputs, and selects all data corresponding to location_id and
    month_id from the joined COVID_Cases and Air_Quality tables. If month_id is
    None, then all data corresponding to location_id, regardless of month, is
    selected. Each entry in the selected data contains the date, month_id, new_cases,
    and average attribute. This data is returned as a list of tuples.'''
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
