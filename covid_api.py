import requests

US_CASES_BASE_URL = "https://api.covid19api.com/total/country/united-states/status/confirmed"

def get_US_confirmed_cases(from_date, to_date):
    url = f"{US_CASES_BASE_URL}?from={from_date}T00:00:00Z&to={to_date}T00:00:00Z"
    try:
        cases_request = requests.get(url)
        if not cases_request:
            raise Exception(cases_request.status_code)

        return cases_request.json()
    except Exception as e:
        print("An exception occurred. Here's the message:")
        print(e)

def get_US_cases_by_month(month):
    pass

def add_to_COVID_database(cur, conn):
    pass

def build_COVID_database():
    pass

def main():
    print(get_US_confirmed_cases("2020-11-01", "2020-11-02"))

if __name__ == "__main__":
    main()