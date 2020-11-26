import requests

BASE_URL = "https://api.covidtracking.com/v1/states/"

def get_cases_per_month(state, month):
    pass

def get_daily_cases(state, date):
    url = f"{BASE_URL}{state}/{date}.json"
    try:
        cases_request = requests.get(url)
        if not cases_request:
            raise Exception()

        return cases_request.json()
    except Exception as e:
        return None

def add_to_COVID_database(cur, conn):
    pass

def main():
    print(get_daily_cases("ca", "20200301"))

if __name__ == "__main__":
    main()