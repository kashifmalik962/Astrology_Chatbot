# from vedicastro import VedicAstro
# from geopy.geocoders import Nominatim

# utc = 5.5 
# ayanamsa = "Lahiri"
# house_system = "Placidus"

# def get_lat_long(location_name):
#     geolocator = Nominatim(user_agent="geopy_example", timeout=10)
#     location = geolocator.geocode(location_name)

#     if location:
#         latitude, longitude = location.latitude, location.longitude
#         return latitude, longitude
#     else:
#         return 28.7041, 77.1025

# def get_horoscope_data(year, month, day, hour, minute, birth_place):
#     birth_place = get_lat_long(birth_place)
    
#     # Initialize Vedic Horoscope Data
#     horoscope = VedicAstro.VedicHoroscopeData(
#         int(year), int(month), int(day), int(hour), int(minute), 0,
#         utc, int(birth_place[0]), int(birth_place[1]), ayanamsa, house_system
#     )
    
#     # Generate Chart
#     chart = horoscope.generate_chart()

#     # Extract details
#     planets_data = horoscope.get_planets_data_from_chart(chart)
#     houses_data = horoscope.get_houses_data_from_chart(chart)

#     planets_houses_data = {
#         "planets_data": planets_data,
#         "houses_data": houses_data,
#     }
    
#     # Convert planets and houses data to dictionaries
#     planets_data_list = [i._asdict() for i in planets_houses_data["planets_data"]]
#     houses_data_list = [i._asdict() for i in planets_houses_data["houses_data"]]

#     # Organize the data into dictionaries
#     final_data = [{"planets_data": planets_data_list}, {"houses_data": houses_data_list}]
    
#     # Function to format planets data with house and rasi information
#     def format_planets_data(planets_data):
#         house_lookup = {house['HouseNr']: house['Rasi'] for house in planets_data[1]['houses_data']}
#         house_planets = {}

#         # Group planets by house
#         for planet in planets_data[0]['planets_data']:
#             house = planet['HouseNr']
#             planet_info = f"{planet['Object']}{', Retrograde' if planet['isRetroGrade'] else ''}"
#             if house not in house_planets:
#                 house_planets[house] = []
#             house_planets[house].append(planet_info)

#         # Format the house details
#         house_details = []
#         for house, planets in house_planets.items():
#             rasi = house_lookup.get(house, 'Unknown')
#             house_details.append(f"House {house}: {rasi} ({', '.join(planets)})")
        
#         return house_details

#     # Format and return the final horoscope data
#     formatted_planets_data = format_planets_data(final_data)
#     return formatted_planets_data

# # Example call
# print(get_horoscope_data("1992", "1", "2", "6", "40", "Delhi"))





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

def get_horoscope_data(year, month, day, hour, minute, birth_place_pin):
    print("func running...")
    api_entity_house = "extended-horoscope/kp-houses"
    api_entity_planet = "extended-horoscope/kp-planets"
    lat,lon = get_lat_long(birth_place_pin)
  

    print(lat, lon, "birth_place_lat_lon")
    print(VEDIC_BASE_API)

    try:
        response_house = requests.get(f"{VEDIC_BASE_API}/{api_entity_house}?dob={day}/{month}/{year}&tob={hour}:{minute}&lat={26.7658}&lon={83.0834}&tz=5.5&api_key={API_KEY}&lang=en")
        print(response_house)  # Print the response_house status
        
        response_planet = requests.get(f"{VEDIC_BASE_API}/{api_entity_planet}?dob={day}/{month}/{year}&tob={hour}:{minute}&lat={26.7658}&lon={83.0834}&tz=5.5&api_key={API_KEY}&lang=en")
        
        print(response_planet, "response_planet")

        
        if response_house.status_code == 200 and response_planet.status_code == 200:

            data_house = response_house.json()  # Parse JSON response
            horoscope_data_house = data_house.get("response", [])
            # print(horoscope_data)  # Debug: print parsed response

            # Extract desired data
            result = []
            for obj in horoscope_data_house:
                result.append({
                    "house": obj.get("house"),
                    "start_rasi": obj.get("start_rasi")
                })

            data_planet = response_planet.json()  # Parse JSON response
            horoscope_data_planet = data_planet.get("response", [])
            print(horoscope_data_planet,"horoscope_data_planet")
            for dic in result:
                plants_lst = []
                for obj,val in horoscope_data_planet.items():
                    print(dic, obj, val)
                    try:
                        if dic["house"] == val.get("house"):
                            plants_lst.append(val.get("full_name"))
                            dic["planet"] = plants_lst
                    except:
                        pass
            return result
        else:
            print(f"Failed to fetch horoscope data. Status code: {response_house.status_code}")
            return {}
    except requests.exceptions.RequestException as e:
        print(f"Error while making API call: {e}")
        return {}

# Example usage:
print(get_horoscope_data("2001", "07", "15", "21", "05", "272175"))