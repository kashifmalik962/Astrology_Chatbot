import requests
from geopy.geocoders import Nominatim
from datetime import datetime

def get_lat_long(location_name_pin):
    geolocator = Nominatim(user_agent="pincode_locator",timeout=10)
    location = geolocator.geocode(location_name_pin)

    if location:
        latitude, longitude = location.latitude, location.longitude
        print("location mil gyi", latitude, longitude)
        return latitude, longitude
    else:
        print("location nhi mili", latitude, longitude)
        return 28.7041, 77.1025


def calculate_chardasha_differences(response):
    # Parse dates
    sub_dasha_start_date = datetime.strptime(response["sub_dasha_start_date"], "%a %b %d %Y")
    sub_dasha_end_dates = [
        datetime.strptime(date.split(" GMT")[0], "%a %b %d %Y %H:%M:%S")
        for date in response["sub_dasha_end_dates"]
    ]

    # Get current date dynamically
    current_date = datetime.now()

    # Find the current sub-dasha
    current_chardasha = None
    for i, end_date in enumerate(sub_dasha_end_dates):
        # The first sub-dasha starts at sub_dasha_start_date
        start_date = sub_dasha_start_date if i == 0 else sub_dasha_end_dates[i - 1]
        if start_date <= current_date <= end_date:
            current_chardasha = response["sub_dasha_list"][i]
            break

    # Output result
    if current_chardasha:
        return f"Current Chardasha on {current_date.strftime('%a %b %d %Y')}: {current_chardasha}"
    else:
        print("No active Chardasha found.")
        return "No active Chardasha found."

API_KEY = "bda76f21-aad1-590f-923d-3d40f2678a1c"
VEDIC_BASE_API = f"https://api.vedicastroapi.com/v3-json"



def get_chardasha(year, month, day, hour, minute, birth_place_pin):
    lat,lon = get_lat_long(birth_place_pin)
    api_entity = "dashas/char-dasha-current"
    tz = 5.5
    lang = "en"

    try:
        response = requests.get(f"{VEDIC_BASE_API}/{api_entity}?dob={day}/{month}/{year}&tob={hour}:{minute}&lat={lat}&lon={lon}&tz={tz}&api_key={API_KEY}&lang={lang}")

        print(response)
        if response.status_code == 200:
            response_json = response.json()

            print(response_json)
            response_res = response_json.get("response", [])
            print(response_res, "++++++")

            result = calculate_chardasha_differences(response_res)
        
            return result
        else:
            print(f"Failed to fetch horoscope data. Status code: {response.status_code}")
            return {}
    except requests.exceptions.RequestException as e:
        print(f"Error while making API call: {e}")
        return {}

print(get_chardasha("2001", "07", "15", "21", "05", "272175"))