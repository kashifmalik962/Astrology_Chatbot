import swisseph as swe
import math
from datetime import datetime

# Function to calculate Tithi, Vara, Lunar Month, and Hora
def get_tithi_vara_lunar_month_hora(date):
    # Set the Julian Day for the given date
    year, month, day = map(int, date.split('-'))
    jd = swe.julday(year, month, day, 0)  # Julian day at midnight

    # Get the Sun's and Moon's positions
    sun_pos = swe.calc(jd, swe.SUN)
    moon_pos = swe.calc(jd, swe.MOON)

    # Extract the longitudes (in degrees) of Sun and Moon from the first element of the tuple
    sun_longitude = sun_pos[0][0]  # First element represents longitude
    moon_longitude = moon_pos[0][0]  # First element represents longitude
    print(f"Sun Longitude: {sun_longitude}, Moon Longitude: {moon_longitude}")

    # Calculate the Tithi (lunar day) based on the angular distance between the Sun and Moon
    tithi_angle = (moon_longitude - sun_longitude) % 360
    tithi_number = int(tithi_angle / 12) + 1  # Tithi ranges from 1 to 30

    # Define the names of Tithis
    tithi_names = [
        "Pratipada", "Dvitia", "Tritiya", "Chaturthi", "Panchami", "Shashthi", "Saptami",
        "Ashtami", "Navami", "Dashami", "Ekadashi", "Dvadashi", "Trayodashi", "Chaturdashi",
        "Purnima", "Pratipada", "Dvitia", "Tritiya", "Chaturthi", "Panchami", "Shashthi",
        "Saptami", "Ashtami", "Navami", "Dashami", "Ekadashi", "Dvadashi", "Trayodashi",
        "Chaturdashi", "Amavasya"
    ]
    tithi_name = tithi_names[tithi_number - 1]  # Get the name of the Tithi

    # Get the Vara (day of the week) based on the Julian Day
    day_of_week = int((jd + 1.5) % 7)  # Calculate the day of the week (0 = Sunday, 1 = Monday, etc.)
    varas = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    vara = varas[day_of_week]

    # Lunar Month (based on the position of the Moon, either the waxing or waning phase)
    lunar_month = "Waxing" if moon_longitude < sun_longitude else "Waning"

    # Calculate Hora (planetary hour)
    hora_index = int((jd * 24) % 24)  # Get the hour of the day from the Julian Day
    horas = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu", "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu", "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    hora = horas[hora_index]

    # Return the calculated values
    return f"Tithi: {tithi_number} {tithi_name}", vara, lunar_month, hora

# Example usage
date = "2025-01-07"
tithi, vara, lunar_month, hora = get_tithi_vara_lunar_month_hora(date)

print(tithi)  # Print Tithi with the name
print(f"Vara (Day of the Week): {vara}")
print(f"Lunar Month: {lunar_month}")
print(f"Hora: {hora}")
