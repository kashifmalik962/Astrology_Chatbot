# import swisseph as swe
# import math
# from datetime import datetime

# # Function to calculate Tithi, Vara, Lunar Month, and Hora
# def get_tithi_vara_lunar_month_hora(date):
#     # Set the Julian Day for the given date
#     year, month, day = map(int, date.split('-'))
#     jd = swe.julday(year, month, day, 0)  # Julian day at midnight

#     # Get the Sun's and Moon's positions
#     sun_pos = swe.calc(jd, swe.SUN)
#     moon_pos = swe.calc(jd, swe.MOON)

#     # Extract the longitudes (in degrees) of Sun and Moon from the first element of the tuple
#     sun_longitude = sun_pos[0][0]  # First element represents longitude
#     moon_longitude = moon_pos[0][0]  # First element represents longitude
#     print(f"Sun Longitude: {sun_longitude}, Moon Longitude: {moon_longitude}")

#     # Calculate the Tithi (lunar day) based on the angular distance between the Sun and Moon
#     tithi_angle = (moon_longitude - sun_longitude) % 360
#     tithi_number = int(tithi_angle / 12) + 1  # Tithi ranges from 1 to 30

#     # Define the names of Tithis
#     tithi_names = [
#         "Pratipada", "Dvitia", "Tritiya", "Chaturthi", "Panchami", "Shashthi", "Saptami",
#         "Ashtami", "Navami", "Dashami", "Ekadashi", "Dvadashi", "Trayodashi", "Chaturdashi",
#         "Purnima", "Pratipada", "Dvitia", "Tritiya", "Chaturthi", "Panchami", "Shashthi",
#         "Saptami", "Ashtami", "Navami", "Dashami", "Ekadashi", "Dvadashi", "Trayodashi",
#         "Chaturdashi", "Amavasya"
#     ]
#     tithi_name = tithi_names[tithi_number - 1]  # Get the name of the Tithi

#     # Get the Vara (day of the week) based on the Julian Day
#     day_of_week = int((jd + 1.5) % 7)  # Calculate the day of the week (0 = Sunday, 1 = Monday, etc.)
#     varas = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
#     vara = varas[day_of_week]

#     # Lunar Month (based on the position of the Moon, either the waxing or waning phase)
#     lunar_month = "Waxing" if moon_longitude < sun_longitude else "Waning"

#     # Calculate Hora (planetary hour)
#     hora_index = int((jd * 24) % 24)  # Get the hour of the day from the Julian Day
#     horas = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu", "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu", "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
#     hora = horas[hora_index]

#     # Return the calculated values
#     return {"Tithi": [tithi_number, tithi_name], "vara": vara, "lunar_month": lunar_month, "hora":hora}

# print(get_tithi_vara_lunar_month_hora())
# Example usage
# date = "2025-01-07"


# print(tithi)  # Print Tithi with the name
# print(f"Vara (Day of the Week): {vara}")
# print(f"Lunar Month: {lunar_month}")
# print(f"Hora: {hora}")



import requests
from datetime import datetime
from geopy.geocoders import Nominatim
import geocoder

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
    

def get_current_location():
    # Get the current location using IP
    location = geocoder.ip('me')
    if location.ok:
        return location.latlng  # Returns (latitude, longitude)
    else:
        return None


def get_current_date_time():
    date = datetime.now().date()
    time = datetime.now().time()

    day = date.day
    month = date.month
    year = date.year

    hour = time.hour
    minute = time.minute

    current_date = f"{day}/{month}/{year}"
    current_time = f"{hour}:{minute}"

    return current_date, current_time

API_KEY = "bda76f21-aad1-590f-923d-3d40f2678a1c"
VEDIC_BASE_API = f"https://api.vedicastroapi.com/v3-json"

def get_panchang_details():
    current_date, current_time = get_current_date_time()
    coordinates = get_current_location()
    tz = 5.5
    api_entity = "panchang/panchang"
    
    try:
        response = requests.get(f"{VEDIC_BASE_API}/{api_entity}?api_key={API_KEY}&date={current_date}&tz={tz}&lat={coordinates[0]}&lon={coordinates[1]}&time={current_time}&lang=en")

        print(response)
        if response.status_code == 200:
            response_json = response.json()

            response_res = response_json.get("response", [])
            print(response_res, "++++++")

            return {"day":response_res["day"]["name"],
                    "tithi":response_res["tithi"]["name"],
                    "nakshatra":response_res["nakshatra"]["name"],
                    "karana":response_res["karana"]["name"],
                    "yoga":response_res["yoga"]["name"],
                    "rasi":response_res["rasi"]["name"],
                    "sun_position":response_res["sun_position"]["zodiac"],
                    "moon_position":response_res["moon_position"]["moon_degree"],
                    "rahukaal":response_res["rahukaal"],
                    "gulika":response_res["gulika"],
                    "yamakanta":response_res["yamakanta"],
                    "gulika":response_res["gulika"]}
        
        else:
            print(f"Failed to fetch horoscope data. Status code: {response.status_code}")
            return {}
    except requests.exceptions.RequestException as e:
        print(f"Error while making API call: {e}")
        return {}
    

print(get_panchang_details())