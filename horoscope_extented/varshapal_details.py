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



def get_varshapal_details(year, month, day, hour, minute, birth_place_pin):
    lat,lon = get_lat_long(birth_place_pin)
    api_entity = "extended-horoscope/varshapal-details"
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

            muntha_sign = response_res["muntha_sign"]
            muntha_lord = response_res["muntha_lord"]
            varshpal_date = response_res["varshpal_date"]
            varsha_lagna = response_res["varsha_lagna"]
            varsha_lagna_lord = response_res["varsha_lagna_lord"]
            dinratri_lord = response_res["dinratri_lord"]
            trirashi_lord = response_res["trirashi_lord"]
            current_ayanamsa = response_res["current_ayanamsa"]


            return {"muntha_sign":muntha_sign,"muntha_lord":muntha_lord,"varshpal_date":varshpal_date,"varsha_lagna":varsha_lagna,"varsha_lagna_lord":varsha_lagna_lord,"dinratri_lord":dinratri_lord,"trirashi_lord":trirashi_lord,"current_ayanamsa":current_ayanamsa}
        else:
            print(f"Failed to fetch horoscope data. Status code: {response.status_code}")
            return {}
    except requests.exceptions.RequestException as e:
        print(f"Error while making API call: {e}")
        return {}

print(get_varshapal_details("2001", "07", "15", "21", "05", "272175"))