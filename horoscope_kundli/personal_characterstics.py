import requests
from geopy.geocoders import Nominatim
from datetime import datetime


API_KEY = "a9a96b0a-fbfb-593b-b0dc-2ca6306964a0"
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



def get_per_charcterstics(year, month, day, hour, minute, birth_place_pin):
    lat,lon = get_lat_long(birth_place_pin)
    api_entity = "horoscope/personal-characteristics"
    tz = 5.5
    lang = "en"

    try:
        response = requests.get(f"{VEDIC_BASE_API}/{api_entity}?dob={day}/{month}/{year}&tob={hour}:{minute}&lat={lat}&lon={lon}&tz={tz}&api_key={API_KEY}&lang={lang}")

        print(response)
        if response.status_code == 200:
            response_json = response.json()

            # print(response_json)
            response_res = response_json.get("response", [])
            # print(response_res, "++++++")
            filer_result = []
            for rec in response_res:
                filter_dict = {}
                filter_dict["current_house"] =  rec["current_house"]
                filter_dict["verbal_location"] =  rec["verbal_location"]
                filter_dict["current_zodiac"] =  rec["current_zodiac"]
                filter_dict["lord_of_zodiac"] =  rec["lord_of_zodiac"]
                filter_dict["lord_zodiac_location"] =  rec["lord_zodiac_location"]
                filter_dict["lord_house_location"] =  rec["lord_house_location"]
                filter_dict["lord_strength"] =  rec["lord_strength"]
                filer_result.append(filter_dict)
            return filer_result
        else:
            print(f"Failed to fetch horoscope data. Status code: {response.status_code}")
            return {}
        
    except requests.exceptions.RequestException as e:
        print(f"Error while making API call: {e}")
        return {}

print(get_per_charcterstics("2001", "07", "15", "21", "05", "272175"))