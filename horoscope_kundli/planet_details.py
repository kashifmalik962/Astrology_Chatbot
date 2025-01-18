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



def get_planets_details(year, month, day, hour, minute, birth_place_pin):
    lat,lon = get_lat_long(birth_place_pin)
    api_entity = "horoscope/planet-details"
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

            filter_plantes_detail = [] 
            for key, val in response_res.items():
                try:
                    filter_data = {}
                    filter_data["full_name"] = val["full_name"]
                    filter_data["local_degree"] = val["local_degree"]
                    filter_data["global_degree"] = val["global_degree"]
                    filter_data["rasi_no"] = val["rasi_no"]
                    filter_data["zodiac"] = val["zodiac"]
                    filter_data["house"] = val["house"]
                    filter_data["nakshatra"] = val["nakshatra"]
                    filter_data["nakshatra_lord"] = val["nakshatra_lord"]
                    filter_data["nakshatra_no"] = val["nakshatra_no"]
                    filter_data["zodiac_lord"] = val["zodiac_lord"]
                    filter_plantes_detail.append(filter_data)
                except:
                    pass

            return {"plantes_details":filter_plantes_detail}
        else:
            print(f"Failed to fetch horoscope data. Status code: {response.status_code}")
            return {}
    except requests.exceptions.RequestException as e:
        print(f"Error while making API call: {e}")
        return {}

print(get_planets_details("2001", "07", "15", "21", "05", "272175"))