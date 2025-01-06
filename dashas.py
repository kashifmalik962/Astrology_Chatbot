import swisseph as swe
import datetime

# Function to calculate Nakshatra
def get_nakshatra(moon_longitude):
    nakshatras = [
        "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu", 
        "Pushya", "Ashlesha", "Magha", "Purvaphalguni", "Uttara-phalguni", "Hasta", 
        "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purvashadha", 
        "Uttarasadha", "Shravana", "Dhanishta", "Shatabhisha", "Purvabhadrapada", 
        "Uttara-bhadrapada", "Revati"
    ]
    
    nakshatra_index = int(moon_longitude // 13.3333)
    return nakshatras[nakshatra_index]

# Function to get the Mahadasha based on the Nakshatra
def get_mahadasha(nakshatra_name):
    # Vimshottari Dasha system sequence (Planetary Lords and their durations)
    mahadasha_lords = {
        "Ashwini": ("Ketu", 7),
        "Bharani": ("Venus", 20),
        "Krittika": ("Sun", 6),
        "Rohini": ("Moon", 10),
        "Mrigashira": ("Mars", 7),
        "Ardra": ("Rahu", 18),
        "Punarvasu": ("Jupiter", 16),
        "Pushya": ("Saturn", 19),
        "Ashlesha": ("Mercury", 17),
        "Magha": ("Ketu", 7),
        "Purvaphalguni": ("Venus", 20),
        "Uttara-phalguni": ("Sun", 6),
        "Hasta": ("Moon", 10),
        "Chitra": ("Mars", 7),
        "Swati": ("Rahu", 18),
        "Vishakha": ("Jupiter", 16),
        "Anuradha": ("Saturn", 19),
        "Jyeshtha": ("Mercury", 17),
        "Mula": ("Ketu", 7),
        "Purvashadha": ("Venus", 20),
        "Uttarasadha": ("Sun", 6),
        "Shravana": ("Moon", 10),
        "Dhanishta": ("Mars", 7),
        "Shatabhisha": ("Rahu", 18),
        "Purvabhadrapada": ("Jupiter", 16),
        "Uttara-bhadrapada": ("Saturn", 19),
        "Revati": ("Mercury", 17)
    }
    
    return mahadasha_lords.get(nakshatra_name, ("Unknown", 0))

# Set the date and time
date = datetime.datetime(2001, 7, 15, 21, 5)  # Example date (Year, Month, Day, Hour, Minute)

# Convert to Julian Day (required by Swiss Ephemeris)
jd_ut = swe.julday(date.year, date.month, date.day, date.hour + date.minute / 60.0)

# Get the position of the Moon
moon_longitude, _ = swe.calc(jd_ut, swe.MOON)

# Extract the longitude from the tuple
moon_longitude = moon_longitude[0]

# Get Nakshatra name
nakshatra_name = get_nakshatra(moon_longitude)

# Get the Mahadasha for the current Nakshatra
mahadasha_name, mahadasha_duration = get_mahadasha(nakshatra_name)

# Get the Antardasha (sub-period) based on Mahadasha
# Example: if Mahadasha is Ketu, the first Antardasha is Ketu itself, then Venus, etc.
antardasha_sequence = [
    "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"
]

# Print results
print(f"Moon's Longitude: {moon_longitude}°")
print(f"The Nakshatra is: {nakshatra_name}")
print(f"Current Mahadasha: {mahadasha_name} ({mahadasha_duration} years)")
print(f"Antardasha Sequence: {antardasha_sequence}")
