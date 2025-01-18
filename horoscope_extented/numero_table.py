import requests
from geopy.geocoders import Nominatim
from datetime import datetime


API_KEY = "bda76f21-aad1-590f-923d-3d40f2678a1c"
VEDIC_BASE_API = f"https://api.vedicastroapi.com/v3-json"



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



def get_numero_table(year, month, day, hour, minute, birth_place_pin):
    lat,lon = get_lat_long(birth_place_pin)
    api_entity = "extended-horoscope/numero-table"
    tz = 5.5
    lang = "en"

    try:
        response = requests.get(f"{VEDIC_BASE_API}/{api_entity}?name=-&dob={day}/{month}/{year}&tob={hour}:{minute}&lat={lat}&lon={lon}&tz={tz}&api_key={API_KEY}&lang={lang}")

        print(response)
        if response.status_code == 200:
            response_json = response.json()

            print(response_json)
            response_res = response_json.get("response", [])
            print(response_res, "++++++")

            radical_number = response_res["radical_number"]
            radical_ruler = response_res["radical_ruler"]
            characteristics = response_res["characteristics"]
            fav_color = response_res["fav_color"]
            fav_day = response_res["fav_day"]
            fav_god = response_res["fav_god"]
            fav_mantra = response_res["fav_mantra"]
            fav_metal = response_res["fav_metal"]
            fav_stone = response_res["fav_stone"]
            fav_substone = response_res["fav_substone"]

            return {"radical_number":radical_number, "radical_ruler":radical_ruler, "characteristics":characteristics, "fav_color":fav_color,"fav_day":fav_day, "fav_god":fav_god, "fav_mantra":fav_mantra, "fav_metal":fav_metal, "fav_stone":fav_stone, "fav_substone":fav_substone}
        else:
            print(f"Failed to fetch horoscope data. Status code: {response.status_code}")
            return {}
    except requests.exceptions.RequestException as e:
        print(f"Error while making API call: {e}")
        return {}

print(get_numero_table("2001", "07", "15", "21", "05", "272175"))