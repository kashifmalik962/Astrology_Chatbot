import swisseph as swe
import datetime

# Set the date and time
date = datetime.datetime(2001, 7, 15, 21, 5)  # Example date (Year, Month, Day, Hour, Minute)

# Convert to Julian Day (required by Swiss Ephemeris)
jd_ut = swe.julday(date.year, date.month, date.day, date.hour + date.minute / 60.0)

# Get the position of the Moon
moon_longitude, _ = swe.calc(jd_ut, swe.MOON)

# Extract the longitude from the tuple
moon_longitude = moon_longitude[0]

# Nakshatra calculation: Nakshatra index is moon_longitude // 13.3333
nakshatra_index = int(moon_longitude // 13.3333)

# List of Nakshatras
nakshatras = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu", 
    "Pushya", "Ashlesha", "Magha", "Purvaphalguni", "Uttara-phalguni", "Hasta", 
    "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purvashadha", 
    "Uttarasadha", "Shravana", "Dhanishta", "Shatabhisha", "Purvabhadrapada", 
    "Uttara-bhadrapada", "Revati"
]

# Get Nakshatra name from index
nakshatra_name = nakshatras[nakshatra_index]

print(f"The Nakshatra is: {nakshatra_name}")
