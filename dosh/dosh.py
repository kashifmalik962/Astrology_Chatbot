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

# api = "https://api.vedicastroapi.com/v3-json/dosha/mangal-dosh?dob=15/07/2001&tob=21:05&lat=26.7779767&lon=83.0486050375&tz=5.5&api_key={API_KEY}&lang=en"
#apis = "https://api.vedicastroapi.com/v3-json/dosha/mangal-dosh?dob=15/07/2001&tob=21:05&lat=26.7779767&lon=83.0486050375&tz=5.5&api_key=bda76f21-aad1-590f-923d-3d40f2678a1c&lang=en"


# def get_mangal_dosh(year, month, day, hour, minute, birth_place_pin):
#     lat,lon = get_lat_long(birth_place_pin)
#     api_entity = "dosha/mangal-dosh"
#     tz = 5.5
#     lang = "en"

#     try:
#         response = requests.get(f"{VEDIC_BASE_API}/{api_entity}?dob={day}/{month}/{year}&tob={hour}:{minute}&lat={lat}&lon={lon}&tz={tz}&api_key={API_KEY}&lang={lang}")

#         print(response)
#         if response.status_code == 200:
#             response_json = response.json()

#             response_res = response_json.get("response", [])
#             print(response_res, "++++++")

#             print(response_res["factors"], "response_res['factors']")
#             return {"manglik": response_res["bot_response"], 
#                     "moon": response_res["factors"]["moon"], 
#                     "saturn": response_res["factors"]["saturn"],
#                     "is_dosha_present_mars_from_lagna":response_res["is_dosha_present_mars_from_lagna"],
#                     "is_dosha_present_mars_from_moon":response_res["is_dosha_present_mars_from_moon"]}
#         else:
#             print(f"Failed to fetch horoscope data. Status code: {response.status_code}")
#             return {}
#     except requests.exceptions.RequestException as e:
#         print(f"Error while making API call: {e}")
#         return {}

# print(get_mangal_dosh("2001", "07", "15", "21", "05", "272175"))



# def get_kaalsarp_dosh(year, month, day, hour, minute, birth_place_pin):
#     lat,lon = get_lat_long(birth_place_pin)
#     api_entity = "dosha/kaalsarp-dosh"
#     tz = 5.5
#     lang = "en"

#     try:
#         response = requests.get(f"{VEDIC_BASE_API}/{api_entity}?dob={day}/{month}/{year}&tob={hour}:{minute}&lat={lat}&lon={lon}&tz={tz}&api_key={API_KEY}&lang={lang}")

#         print(response)
#         if response.status_code == 200:
#             response_json = response.json()

#             response_res = response_json.get("response", [])
#             # print(response_res, "++++++")

#             return {"is_dosha_present": response_res["is_dosha_present"], "response":response_res["bot_response"]}
#         else:
#             print(f"Failed to fetch horoscope data. Status code: {response.status_code}")
#             return {}
#     except requests.exceptions.RequestException as e:
#         print(f"Error while making API call: {e}")
#         return {}

# print(get_kaalsarp_dosh("2001", "07", "15", "21", "05", "272175"))




# def get_manglik_dosh(year, month, day, hour, minute, birth_place_pin):
#     lat,lon = get_lat_long(birth_place_pin)
#     api_entity = "dosha/manglik-dosh"
#     tz = 5.5
#     lang = "en"

#     try:
#         response = requests.get(f"{VEDIC_BASE_API}/{api_entity}?dob={day}/{month}/{year}&tob={hour}:{minute}&lat={lat}&lon={lon}&tz={tz}&api_key={API_KEY}&lang={lang}")

#         print(response)
#         if response.status_code == 200:
#             response_json = response.json()

#             print(response_json)
#             response_res = response_json.get("response", [])
#             print(response_res, "++++++")

#             return {
#                 "manglik_by_mars": response_res["manglik_by_mars"],
#                 "manglik_factor": response_res["factors"][0],
#                 "manglik": response_res["bot_response"],
#                 "aspects": response_res["aspects"],
#                 "manglik_by_saturn": response_res["manglik_by_saturn"],
#                 "manglik_by_rahuketu": response_res["manglik_by_rahuketu"]
#             }
#         else:
#             print(f"Failed to fetch horoscope data. Status code: {response.status_code}")
#             return {}
#     except requests.exceptions.RequestException as e:
#         print(f"Error while making API call: {e}")
#         return {}

# print(get_manglik_dosh("2001", "07", "15", "21", "05", "272175"))




def get_pitra_dosh(year, month, day, hour, minute, birth_place_pin):
    lat,lon = get_lat_long(birth_place_pin)
    api_entity = "dosha/pitra-dosh"
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

            return {
                "is_dosha_present": response_res["is_dosha_present"],
                "response": response_res["bot_response"]
            }
        else:
            print(f"Failed to fetch horoscope data. Status code: {response.status_code}")
            return {}
    except requests.exceptions.RequestException as e:
        print(f"Error while making API call: {e}")
        return {}

print(get_pitra_dosh("2001", "07", "15", "21", "05", "272175"))