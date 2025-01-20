import requests
from datetime import datetime


API_KEY = "a9a96b0a-fbfb-593b-b0dc-2ca6306964a0"
VEDIC_BASE_API = f"https://api.vedicastroapi.com/v3-json"


def get_current_date_time():
    date = datetime.now().date()
    time = datetime.now().time()

    day, month, year = date.day, date.month, date.year

    hour, minute = time.hour, time.minute
    current_date, current_time = f"{day}/{month}/{year}", f"{hour}:{minute}"

    return current_date, current_time



def get_moon_phase():
    current_date, current_time = get_current_date_time()
    tz = 5.5
    lang = "en"
    api_rise_entity = "panchang/moon-phase"

    try:
        response = requests.get(f"{VEDIC_BASE_API}/{api_rise_entity}?api_key={API_KEY}&date={current_date}&tz={tz}&lang={lang}")

        print(response)
        if response.status_code == 200:

            response_json = response.json()
            response_res = response_json.get("response", [])

            print(response_res, "response_res")
            
            bot_response = response_res["bot_response"]
            luminance = response_res["luminance"]
            phase = response_res["phase"]
            paksha = response_res["paksha"]
            state = response_res["state"]
            date = response_res["date"]
            
            return {"Moon Phase =>": phase, "response": bot_response, "luminance":luminance, "paksha":paksha, "state":state, "date":date}
        else:
            print(f"Failed to fetch horoscope data. Status code: {response_res.status_code}")
            return {}
    except requests.exceptions.RequestException as e:
        print(f"Error while making API call: {e}")
        return {}

print(get_moon_phase())