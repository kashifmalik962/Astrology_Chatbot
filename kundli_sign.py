import requests
from geopy.geocoders import Nominatim



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

def get_kundli_signs(year, month, day, hour, minute, birth_place_pin):

    lat,lon = get_lat_long(birth_place_pin)
    api_entity = "extended-horoscope/extended-kundli-details"
    
    try:
        response = requests.get(f"{VEDIC_BASE_API}/{api_entity}?dob={day}/{month}/{year}&tob={hour}:{minute}&lat={lat}&lon={lon}&tz=5.5&api_key={API_KEY}&lang=en")

        print(response)
        if response.status_code == 200:
            response_json = response.json()

            response_res = response_json.get("response", [])
            print(response_res, "++++++")

            return {
                "gana": response_res.get("gana"),
                "yoni": response_res.get("yoni"),
                "vasya": response_res.get("vasya"),
                "nadi": response_res.get("nadi"),
                "varna": response_res.get("varna"),
                "paya": response_res.get("paya"),
                "tatva": response_res.get("tatva"),
                "life_stone": response_res.get("life_stone"),
                "lucky_stone": response_res.get("lucky_stone"),
                "fortune_stone": response_res.get("fortune_stone"),
                "ascendant_sign": response_res.get("ascendant_sign"),
                "ascendant_nakshatra": response_res.get("ascendant_nakshatra"),
                "rasi": response_res.get("rasi"),
                "rasi_lord": response_res.get("rasi_lord"),
                "nakshatra": response_res.get("nakshatra"),
                "karana": response_res.get("karana"),
                "yoga": response_res.get("yoga")
            }
        else:
            print(f"Failed to fetch horoscope data. Status code: {response.status_code}")
            return {}
    except requests.exceptions.RequestException as e:
        print(f"Error while making API call: {e}")
        return {}
    

print(get_kundli_signs("2001","07","15","21","05", "272175"))