import swisseph as swe
from datetime import datetime

def extract_date_time_variables():
    # Parse the date string into datetime object
    date_obj = datetime.now()
    
    # Extract year, month, day, hour, minute
    year = date_obj.year
    month = date_obj.month
    day = date_obj.day
    hour = date_obj.hour
    minute = date_obj.minute
    
    print(year, month, day, hour, minute)
    return year, month, day, hour, minute

# Set the date and time
year, month, day, hour, minute = extract_date_time_variables()

# Convert to Julian Day (required by Swiss Ephemeris)
jd_ut = swe.julday(year, month, day, hour + minute / 60.0)

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
