# import ephem

# def get_planet_positions(date):
#     # Use ephem to calculate planetary positions at a given time
#     observer = ephem.Observer()
#     observer.date = date
    
#     # Get the current position of planets (e.g., Sun, Moon, etc.)
#     sun = ephem.Sun(observer)
#     moon = ephem.Moon(observer)
#     venus = ephem.Venus(observer)
#     jupiter = ephem.Jupiter(observer)
    
#     # Return the longitudes of the planets in degrees
#     return sun, moon, venus, jupiter

# # Example: get planet positions for today
# planet_positions = get_planet_positions("2025-01-07")

# # Convert the positions from hours to degrees and print
# for planet in planet_positions:
#     # Convert from hours (ephem.hlon) to degrees
#     longitude_in_degrees = planet.hlon * 15  # 1 hour = 15 degrees
#     if planet.name == "Moon":
#         moon_longitude = round(longitude_in_degrees,2)
#         print(moon_longitude)



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


def calculate_mahadasha_differences(response):
    mahadasha = response["mahadasha"]
    mahadasha_order = response["mahadasha_order"]
    start_year = response["start_year"]

    differences = {}

    for i in range(len(mahadasha)):
        # Extract the year from the current mahadasha_order date
        current_year = datetime.strptime(mahadasha_order[i], "%a %b %d %Y").year

        if i == 0:
            # For the first mahadasha, calculate from start_year
            previous_year = start_year
        else:
            # For subsequent mahadashas, calculate from the previous mahadasha's year
            previous_year = datetime.strptime(mahadasha_order[i - 1], "%a %b %d %Y").year

        # Calculate the difference in years
        year_difference = current_year - previous_year
        differences[mahadasha[i].lower()] = f"{year_difference} years"

    return differences



def get_mahadasha(year, month, day, hour, minute, birth_place_pin):
    lat,lon = get_lat_long(birth_place_pin)
    api_entity = "dashas/maha-dasha"
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

            # mahadasha = response_res["mahadasha"]
            # mahadasha_order = response_res["mahadasha_order"]
            # start_year = response_res["start_year"]

            result = calculate_mahadasha_differences(response_res)
            

            return result
        else:
            print(f"Failed to fetch horoscope data. Status code: {response.status_code}")
            return {}
    except requests.exceptions.RequestException as e:
        print(f"Error while making API call: {e}")
        return {}

print(get_mahadasha("2001", "07", "15", "21", "05", "272175"))