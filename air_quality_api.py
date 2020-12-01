import requests

BASE_URL = "https://api.openaq.org/beta/averages?country=US&"

def get_monthly_cases(city, location, month):
    openaq_url = f"{BASE_URL}city={city}&location={location}&date_from=2020-{month}-01&date_to=2020-{month}-25"
    try:
        response_api = requests.get(openaq_url)
    except:
        return None

    return response_api

def add_to_AQ_database(data, location_id, month, cur, conn):
    for entry in data["results"]:
        date = int(entry["date"].replace("-", ""))
        month = int(month)
        average = entry["average"]
        cur.execute("INSERT INTO Air_Quality (date, month_id, location_id, average) VALUES (?, ?, ?, ?)", (date, month, location_id, average,))
    conn.commit()

def API_driver(location, month, cur, conn):
    daily_cases_request = get_monthly_cases(location[2], location[3], month)
    if daily_cases_request is None:
        return (False, "No status code received")
    
    if not daily_cases_request:
        return (False, daily_cases_request.status_code)
    
    air_quality_data = daily_cases_request.json()
    if not air_quality_data["results"]:
        return (False, "No data available")
    
    try:
        add_to_AQ_database(air_quality_data, location[0], month, cur, conn)
    except:
        pass

    return (True,)
