import requests

BASE_URL = "https://api.covidtracking.com/v1/states/"

def get_daily_cases(state, date):
    url = f"{BASE_URL}{state}/{date}.json"
    try:
        cases_request = requests.get(url)
    except:
        return None
    
    return cases_request

def add_to_COVID_database(json_data, date, location_id, cur, conn):
    month = int(date[4:6])
    date = int(date)
    new_cases = json_data["positiveIncrease"]
    cur.execute("INSERT INTO COVID_Cases (date, month_id, location_id, new_cases) VALUES (?, ?, ?, ?)",
                (date, month, location_id, new_cases))
    conn.commit()

def API_driver(state, location_id, month, cur, conn):
    for i in range(1, 26):
        if i < 10:
            date = f"2020{month}0{i}"
        else:
            date = f"2020{month}{i}"
        
        daily_cases_request = get_daily_cases(state, date)
        if daily_cases_request is None:
            return (False, "No status code received")
        if not daily_cases_request:
            return (False, daily_cases_request.status_code)
        
        try:
            add_to_COVID_database(daily_cases_request.json(), date, location_id, cur, conn)
        except:
            return (False, "Data already exists in database")

    return (True,)
