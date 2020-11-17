import requests

SUMMARIES_URL = "https://api.covid19api.com/summary"

def get_US_summary():
    try:
        summary_request = requests.get(SUMMARIES_URL)
        if not summary_request:
            raise Exception(summary_request.status_code)

        summary_json = summary_request.json()
        for summary in summary_json["Countries"]:
            if summary["CountryCode"] == "US":
                return summary
        
        raise Exception("US summary not returned.")
    except Exception as e:
        print("An exception occurred Here's the message:")
        print(e)
