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



def get_ascendant_report(year, month, day, hour, minute, birth_place_pin):
    lat,lon = get_lat_long(birth_place_pin)
    api_entity = "horoscope/ascendant-report"
    tz = 5.5
    lang = "en"

    try:
        response = requests.get(f"{VEDIC_BASE_API}/{api_entity}?dob={day}/{month}/{year}&tob={hour}:{minute}&lat={lat}&lon={lon}&tz={tz}&api_key={API_KEY}&lang={lang}")

        print(response)
        if response.status_code == 200:
            response_json = response.json()

            # print(response_json)
            response_res = response_json.get("response", [])[0]
            # print(response_res, "++++++")

            ascendant = response_res["ascendant"]
            ascendant_lord = response_res["ascendant_lord"]
            ascendant_lord_location = response_res["ascendant_lord_location"]
            ascendant_lord_house_location = response_res["ascendant_lord_house_location"]
            verbal_location = response_res["verbal_location"]
            ascendant_lord_strength = response_res["ascendant_lord_strength"]
            zodiac_characteristics = response_res["zodiac_characteristics"]
            lucky_gem = response_res["lucky_gem"]
            day_for_fasting = response_res["day_for_fasting"]
            gayatri_mantra = response_res["gayatri_mantra"]


            return {"ascendant":ascendant, "ascendant_lord":ascendant_lord, "ascendant_lord_location":ascendant_lord_location, "ascendant_lord_house_location":ascendant_lord_house_location, "verbal_location":verbal_location, "ascendant_lord_strength":ascendant_lord_strength, "zodiac_characteristics":zodiac_characteristics,"lucky_gem":lucky_gem,"day_for_fasting":day_for_fasting,"gayatri_mantra":gayatri_mantra}
        else:
            print(f"Failed to fetch horoscope data. Status code: {response.status_code}")
            return {}
        
    except requests.exceptions.RequestException as e:
        print(f"Error while making API call: {e}")
        return {}

print(get_ascendant_report("2001", "07", "15", "21", "05", "272175"))