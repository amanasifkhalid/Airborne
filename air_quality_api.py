import requests

def get_monthly_cases(city, month):
    openaq_url = f"https://api.openaq.org/beta/averages?country=US&city={city}&date_from=2020-{month}-01&date_to=2020-{month}-25"
    try:
        response_api = requests.get(openaq_url)
        # response_api_text = response_api.text
        # parsed = json.loads(response_api_text)
        # jdump = json.dumps(parsed, indent=4)
    except:
        return None
    # return jdump
    return response_api

def add_to_AQ_database(data, month, location_id, cur, conn):
    location = data["results"][0]["location"]
    for entry in data["results"]:
        if entry["location"] == location:
            date = int(entry["date"].replace("-", ""))
            month = int(month)
            average = entry["average"]
            cur.execute("INSERT INTO Air_Quality (date, month_id, location_id, average) VALUES (?, ?, ?, ?)", (date, month, location_id, average,))
    conn.commit()

def API_driver(city, location_id, month, cur, conn):
    daily_cases_request = get_monthly_cases(city, month)
    if daily_cases_request is None:
        return (False, "No status code received")
    if not daily_cases_request:
        return (False, daily_cases_request.status_code)
    air_quality_data = daily_cases_request.json()
    if not air_quality_data["results"]:
        return (False, "No data available")
    try:
        add_to_AQ_database(air_quality_data, month, location_id, cur, conn)
    except:
        return (False, "Data already exists in database")

    return (True,)
