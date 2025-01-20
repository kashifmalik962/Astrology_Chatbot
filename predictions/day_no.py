import requests
from datetime import datetime


API_KEY = "a9a96b0a-fbfb-593b-b0dc-2ca6306964a0"
VEDIC_BASE_API = f"https://api.vedicastroapi.com/v3-json"



def get_day_no(year, month, day):
    tz = 5.5
    lang = "en"
    api_rise_entity = "prediction/day-number"

    try:
        response = requests.get(f"{VEDIC_BASE_API}/{api_rise_entity}?dob={day}/{month}/{year}&api_key={API_KEY}&lang={lang}")

        print(response)
        if response.status_code == 200:

            response_json = response.json()
            response_res = response_json.get("response", [])

            print(response_res, "response_res")

            
            return {"day number =>": response_res}
        else:
            print(f"Failed to fetch horoscope data. Status code: {response_res.status_code}")
            return {}
    except requests.exceptions.RequestException as e:
        print(f"Error while making API call: {e}")
        return {}

print(get_day_no(2001, 7, 15))