import requests

BASE_URL = "https://api.covidtracking.com/v1/states/"

def get_daily_cases(state, date):
    '''Takes in state and date as inputs. Puts arguments into url. Tries to make
    a get request from the url. If successful, returns the request. If not successful 
    returns None.'''
    url = f"{BASE_URL}{state}/{date}.json"
    try:
        cases_request = requests.get(url)
    except:
        return None
    
    return cases_request

def add_to_COVID_database(data, date, location_id, cur, conn):
    '''Takes in data, date, location_id, database cursor and connector as inputs. 
    Reformates month and date and extracts cases from API data. Then adds data 
    to COVID_Cases table and commits to database connector'''
    month = int(date[4:6])
    date = int(date)
    new_cases = data["positiveIncrease"]
    cur.execute("INSERT INTO COVID_Cases (date, month_id, location_id, new_cases) VALUES (?, ?, ?, ?)",
                (date, month, location_id, new_cases))
    conn.commit()

def API_driver(location, month, cur, conn):
    ''' Takes in location, month, database cursor and connector as inputs. Calls 
    get daily cases for 25 days to get API data. Checks for errors in API response. 
    If there are no errors, calls add_to_COVID_database and returns a tuple with 
    just True. If there are errors, returns a tuple with False and the error message.''' 
    for i in range(1, 26):
        if i < 10:
            date = f"2020{month}0{i}"
        else:
            date = f"2020{month}{i}"
        
        daily_cases_request = get_daily_cases(location[1].lower(), date)
        if daily_cases_request is None:
            if month == "03":
                continue

            return (False, "No status code received")
        
        if not daily_cases_request:
            if month == "03":
                continue
            
            return (False, daily_cases_request.status_code)
        
        try:
            add_to_COVID_database(daily_cases_request.json(), date, location[0], cur, conn)
        except:
            break

    return (True,)
