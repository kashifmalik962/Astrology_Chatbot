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

def get_current_location():
    import geocoder
    # Get the current location using IP
    location = geocoder.ip('me')
    if location.ok:
        return location.latlng  # Returns (latitude, longitude)
    else:
        print("location does not exist...")
        return None





# def get_moon_rise_set():
#     current_date, current_time = get_current_date_time()
#     coordinates = get_current_location()
#     tz = 5.5
#     lang = "en"
#     api_rise_entity = "panchang/moonrise"
#     api_set_entity = "panchang/moonset"

#     try:
#         response_rise = requests.get(f"{VEDIC_BASE_API}/{api_rise_entity}?api_key={API_KEY}&date={current_date}&tz={tz}&lat={coordinates[0]}&lon={coordinates[1]}&time={current_time}&lang={lang}")
#         response_set = requests.get(f"{VEDIC_BASE_API}/{api_set_entity}?api_key={API_KEY}&date={current_date}&tz={tz}&lat={coordinates[0]}&lon={coordinates[1]}&time={current_time}&lang={lang}")

#         print(response_rise)
#         print(response_set)
#         if response_rise.status_code == 200 or response_set.status_code == 200:

#             response_rise_json = response_rise.json()
#             response_set_json = response_set.json()

#             response_rise_res = response_rise_json.get("response", [])
#             response_set_res = response_set_json.get("response", [])

#             print(response_rise_res, "++++++")
#             print(response_set_res, "++++++")

#             print(response_rise_res["bot_response"], "response_rise_res['bot_response'] moon rise")
#             print(response_set_res["bot_response"], "response_set_res['bot_response'] moon set")
#             return {response_rise_res["bot_response"],response_set_res["bot_response"]}
#         else:
#             print(f"Failed to fetch horoscope data. Status code: {response_rise_res.status_code}")
#             return {}
#     except requests.exceptions.RequestException as e:
#         print(f"Error while making API call: {e}")
#         return {}

# print(get_moon_rise_set())



# a = "https://api.vedicastroapi.com/v3-json/panchang/sunrise?api_key=YOUR_API_KEY&date=11/03/1994&tz=5.5&lat=11&lon=77&time=10:40&lang=en"


def get_sun_rise_set():
    current_date, current_time = get_current_date_time()
    coordinates = get_current_location()
    tz = 5.5
    lang = "en"
    api_rise_entity = "panchang/sunrise"
    api_set_entity = "panchang/sunset"

    try:
        response_rise = requests.get(f"{VEDIC_BASE_API}/{api_rise_entity}?api_key={API_KEY}&date={current_date}&tz={tz}&lat={coordinates[0]}&lon={coordinates[1]}&time={current_time}&lang={lang}")
        response_set = requests.get(f"{VEDIC_BASE_API}/{api_set_entity}?api_key={API_KEY}&date={current_date}&tz={tz}&lat={coordinates[0]}&lon={coordinates[1]}&time={current_time}&lang={lang}")

        print(response_rise)
        print(response_set)
        if response_rise.status_code == 200 or response_set.status_code == 200:

            response_rise_json = response_rise.json()
            response_set_json = response_set.json()

            response_rise_res = response_rise_json.get("response", [])
            response_set_res = response_set_json.get("response", [])

            print(response_rise_res, "++++++")
            print(response_set_res, "++++++")

            print(response_rise_res["bot_response"], "response_rise_res['bot_response'] moon rise")
            print(response_set_res["bot_response"], "response_set_res['bot_response'] moon set")
            return {response_rise_res["bot_response"],response_set_res["bot_response"]}
        else:
            print(f"Failed to fetch horoscope data. Status code: {response_rise_res.status_code}")
            return {}
    except requests.exceptions.RequestException as e:
        print(f"Error while making API call: {e}")
        return {}

print(get_sun_rise_set())