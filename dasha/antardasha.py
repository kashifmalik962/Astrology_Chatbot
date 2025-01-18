
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


API_KEY = "bda76f21-aad1-590f-923d-3d40f2678a1c"
VEDIC_BASE_API = f"https://api.vedicastroapi.com/v3-json"


def compare_date(start_date, end_date):
    try:
        start_date_obj = datetime.strptime(start_date, "%a %b %d %Y")
        end_date_obj = datetime.strptime(end_date, "%a %b %d %Y")
        
        current_date = datetime.now()
        
        if start_date_obj < current_date and end_date_obj > current_date:
            return True
        else:
            False
    except:
        False

# Function to calculate filtered antardasha list
def calculate_antardasha(antardashas, antardasha_order):
    filter_antardasha = []

    # Iterate over each set of antardashas and their corresponding orders
    for i in range(len(antardashas)):
        current_antardasha = antardashas[i]
        current_order = antardasha_order[i]
        previous_date = None

        for j in range(len(current_antardasha)):
            # Current antardasha and start/end dates
            start_date = current_order[j] if j < len(current_order) else None
            end_date = current_order[j + 1] if j + 1 < len(current_order) else None

            # Append to the result list
            print(f"{current_antardasha[j]} {start_date} to {end_date}")
            if compare_date(start_date, end_date):
                filter_antardasha.append(f"{current_antardasha[j]} {start_date} to {end_date}")
                previous_date = end_date

    return filter_antardasha


def get_antardasha(year, month, day, hour, minute, birth_place_pin):
    lat,lon = get_lat_long(birth_place_pin)
    api_entity = "dashas/antar-dasha"
    tz = 5.5
    lang = "en"

    try:
        response = requests.get(f"{VEDIC_BASE_API}/{api_entity}?dob={day}/{month}/{year}&tob={hour}:{minute}&lat={lat}&lon={lon}&tz={tz}&api_key={API_KEY}&lang={lang}")

        # print(response)
        if response.status_code == 200:
            response_json = response.json()

            # print(response_json)
            response_res = response_json.get("response", [])
            # print(response_res, "++++++")

            antardasha = response_res["antardashas"]
            antardasha_order = response_res["antardasha_order"]

            # print(antardasha, antardasha_order, "antardasha, antardasha_order")

            result = calculate_antardasha(antardasha, antardasha_order)
            

            return result
        else:
            print(f"Failed to fetch horoscope data. Status code: {response.status_code}")
            return {}
    except requests.exceptions.RequestException as e:
        print(f"Error while making API call: {e}")
        return {}

print(get_antardasha("2001", "07", "15", "21", "05", "272175"))