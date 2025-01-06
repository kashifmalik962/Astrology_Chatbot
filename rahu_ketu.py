import swisseph as swe
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


# Zodiac signs and their rulers
ZODIAC_RULERS = {
    1: "Mars",        # Aries
    2: "Venus",       # Taurus
    3: "Mercury",     # Gemini
    4: "Moon",        # Cancer
    5: "Sun",         # Leo
    6: "Mercury",     # Virgo
    7: "Venus",       # Libra
    8: "Mars",        # Scorpio
    9: "Jupiter",     # Sagittarius
    10: "Saturn",     # Capricorn
    11: "Saturn",     # Aquarius
    12: "Jupiter"     # Pisces
}

# Function to calculate Rahu and Ketu
def calculate_rahu_ketu(jd):
    # Get the position of the Moon's Mean Node (Rahu)
    rahu_position, _ = swe.calc_ut(jd, swe.MEAN_NODE)  # MEAN_NODE for Rahu
    
    # Calculate Ketu as 180 degrees opposite to Rahu
    ketu_position = (rahu_position[0] + 180) % 360  # Opposite to Rahu

    # Find the zodiac signs for Rahu and Ketu
    rahu_sign = int(rahu_position[0] // 30) + 1
    ketu_sign = int(ketu_position // 30) + 1

    return rahu_position[0], rahu_sign, ketu_position, ketu_sign

# Function to calculate the Ascendant and its Lord
def calculate_lagna_lord(year, month, day, hour, minute, birth_place_pin):

    birth_place_lat_lon = get_lat_long(birth_place_pin)

    # Convert date and time to Julian Day
    jd = swe.julday(year, month, day, hour + minute / 60.0)
    
    # Calculate sidereal time
    sidereal_time = swe.sidtime(jd)
    
    # Calculate the Ascendant (Lagna)
    ascendant = swe.houses(jd, birth_place_lat_lon[0], birth_place_lat_lon[1], b'P')[0][0]  # 'P' for Placidus house system
    ascendant_sign = int(ascendant // 30) + 1  # Divide by 30 to get the zodiac sign (1-12)

    # Determine the Lagna Lord
    lagna_lord = ZODIAC_RULERS[ascendant_sign]

    # Calculate Rahu and Ketu
    rahu_position, rahu_sign, ketu_position, ketu_sign = calculate_rahu_ketu(jd)

    return {
        "ascendant": ascendant,
        "ascendant_sign": ascendant_sign,
        "lagna_lord": lagna_lord,
        "rahu_position": rahu_position,
        "rahu_sign": rahu_sign,
        "ketu_position": ketu_position,
        "ketu_sign": ketu_sign
    }



print(calculate_lagna_lord(2001,7,15,21,5,272175))