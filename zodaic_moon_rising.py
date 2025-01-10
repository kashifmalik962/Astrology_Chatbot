# import datetime
# import swisseph as swe

# # Function to get Vedic Zodiac Sign based on degree (with Lahiri Ayanamsha shift)
# def get_vedic_zodiac_sign(degree):
#     # Vedic zodiac signs
#     vedic_zodiac_list = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 
#                          'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
#     # Shift by 24 degrees for Lahiri Ayanamsha and ensure degree wraps around
#     degree = (degree - 24) % 360
#     return vedic_zodiac_list[int(degree // 30)]

# # Function to calculate Ascendant, Sun, and Moon Signs in Vedic astrology
# def calculate_vedic_astrological_signs(date_of_birth, latitude, longitude):
#     # Convert birthdate to Julian Date
#     birthdate = datetime.datetime.strptime(date_of_birth, "%Y-%m-%d %H:%M")
#     jd_ut = swe.julday(birthdate.year, birthdate.month, birthdate.day,
#                        birthdate.hour + birthdate.minute / 60 + birthdate.second / 3600)
    
#     # Calculate Ascendant (Rising sign) with Lahiri Ayanamsha
#     cusps, _ = swe.houses(jd_ut, latitude, longitude, b'P')
#     ascendant_degree = cusps[0]  # Ascendant is the first house cusp
#     rising_sign = get_vedic_zodiac_sign(ascendant_degree)
    
#     # Calculate Sun and Moon Signs in Sidereal Zodiac
#     sun_pos = swe.calc_ut(jd_ut, swe.SUN)[0]
#     moon_pos = swe.calc_ut(jd_ut, swe.MOON)[0]
#     sun_sign = get_vedic_zodiac_sign(sun_pos[0])
#     moon_sign = get_vedic_zodiac_sign(moon_pos[0])
    
#     return {
#         'Rising Sign': rising_sign,
#         'Sun Sign': sun_sign,
#         'Moon Sign': moon_sign
#     }

# # Example usage
# date_of_birth = "2001-07-15 21:05"
# latitude, longitude = 26.7606, 83.3732

# # Calculate Vedic astrological signs
# vedic_astrological_signs = calculate_vedic_astrological_signs(date_of_birth, latitude, longitude)

# # Output the results
# print(f"Rising Sign (Ascendant): {vedic_astrological_signs['Rising Sign']}")
# print(f"Sun Sign (Zodiac): {vedic_astrological_signs['Sun Sign']}")
# print(f"Moon Sign (Zodiac): {vedic_astrological_signs['Moon Sign']}")




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

def calculate_vedic_astrological_signs(year, month, day, hour, minute, birth_place_pin):

    lat,lon = get_lat_long(birth_place_pin)
    api_entity_sun_sign = "extended-horoscope/find-sun-sign"
    api_entity_moon_sign = "extended-horoscope/find-moon-sign"
    api_entity_rising_sign = "extended-horoscope/find-ascendant"

    try:
        sun_response = requests.get(f"{VEDIC_BASE_API}/{api_entity_sun_sign}?dob={day}/{month}/{year}&tob={hour}:{minute}&lat={lat}&lon={lon}&tz=5.5&api_key={API_KEY}&lang=en")
        moon_response = requests.get(f"{VEDIC_BASE_API}/{api_entity_moon_sign}?dob={day}/{month}/{year}&tob={hour}:{minute}&lat={lat}&lon={lon}&tz=5.5&api_key={API_KEY}&lang=en")
        rising_response = requests.get(f"{VEDIC_BASE_API}/{api_entity_rising_sign}?dob={day}/{month}/{year}&tob={hour}:{minute}&lat={lat}&lon={lon}&tz=5.5&api_key={API_KEY}&lang=en")

        print(sun_response, moon_response, rising_response)
        if sun_response.status_code == 200 and moon_response.status_code == 200 and rising_response.status_code == 200:
            sun_response_json = sun_response.json()
            moon_response_json = moon_response.json()
            rising_response_json = rising_response.json()
            
            sun_response_res = sun_response_json.get("response", [])
            moon_response_res = moon_response_json.get("response", [])
            rising_response_res = rising_response_json.get("response", [])
            
            print(sun_response_res, moon_response_res, rising_response_res, "++++++")

            return {
                "sun_sign": sun_response_res.get("sun_sign"),
                "moon_sign": moon_response_res.get("moon_sign"),
                "rising_sign": rising_response_res.get("ascendant")
            }
        else:
            print(f"Failed to fetch horoscope data. Status code: {sun_response.status_code, moon_response.status_code, rising_response.status_code}")
            return {}
    except requests.exceptions.RequestException as e:
        print(f"Error while making API call: {e}")
        return {}
    

print(calculate_vedic_astrological_signs("2001","07","15","21","05", "272175"))