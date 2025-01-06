import datetime
import swisseph as swe

# Vedic Zodiac Signs (Sidereal)
vedic_zodiac_list = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 
                     'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

# Function to get Vedic Zodiac Sign based on degree (with Lahiri Ayanamsha shift)
def get_vedic_zodiac_sign(degree):
    degree = (degree - 24) % 360  # Adjust by 24 degrees for Lahiri Ayanamsha
    return vedic_zodiac_list[int(degree // 30)]

# Function to calculate Ascendant, Sun, and Moon Signs in Vedic astrology
def calculate_vedic_astrological_signs(date_of_birth, latitude, longitude):
    # Convert birthdate to Julian Date
    birthdate = datetime.datetime.strptime(date_of_birth, "%Y-%m-%d %H:%M")
    jd_ut = swe.julday(birthdate.year, birthdate.month, birthdate.day,
                       birthdate.hour + birthdate.minute / 60 + birthdate.second / 3600)
    
    # Calculate Ascendant (Rising sign) with Lahiri Ayanamsha
    cusps, _ = swe.houses(jd_ut, latitude, longitude, b'P')
    ascendant_degree = cusps[0]  # Ascendant is the first house cusp
    rising_sign = get_vedic_zodiac_sign(ascendant_degree)
    
    # Calculate Sun and Moon Signs in Sidereal Zodiac
    sun_pos = swe.calc_ut(jd_ut, swe.SUN)[0]
    moon_pos = swe.calc_ut(jd_ut, swe.MOON)[0]
    sun_sign = get_vedic_zodiac_sign(sun_pos[0])
    moon_sign = get_vedic_zodiac_sign(moon_pos[0])
    
    return {
        'Rising Sign': rising_sign,
        'Sun Sign': sun_sign,
        'Moon Sign': moon_sign
    }

# Function to calculate Planetary Positions in the Birth Chart
def calculate_planetary_positions(date_of_birth, latitude, longitude):
    # Convert birthdate to Julian Date
    birthdate = datetime.datetime.strptime(date_of_birth, "%Y-%m-%d %H:%M")
    jd_ut = swe.julday(birthdate.year, birthdate.month, birthdate.day,
                       birthdate.hour + birthdate.minute / 60 + birthdate.second / 3600)

    # List of planets
    planets = [swe.SUN, swe.MOON, swe.MERCURY, swe.VENUS, swe.MARS, swe.JUPITER, swe.SATURN, swe.URANUS, swe.NEPTUNE, swe.PLUTO]
    planet_names = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto']

    planetary_positions = {}

    for i, planet in enumerate(planets):
        planet_pos = swe.calc_ut(jd_ut, planet)[0]
        planetary_positions[planet_names[i]] = {
            'sign': get_vedic_zodiac_sign(planet_pos[0]),
            'degree': round(planet_pos[0] % 30,2)  # degree within the sign
        }

    return planetary_positions

# Function to calculate Houses in the Birth Chart
def calculate_houses(date_of_birth, latitude, longitude):
    # Convert birthdate to Julian Date
    birthdate = datetime.datetime.strptime(date_of_birth, "%Y-%m-%d %H:%M")
    jd_ut = swe.julday(birthdate.year, birthdate.month, birthdate.day,
                       birthdate.hour + birthdate.minute / 60 + birthdate.second / 3600)

    # Calculate Houses with Lahiri Ayanamsha
    cusps, _ = swe.houses(jd_ut, latitude, longitude, b'P')
    
    houses = {}
    for i in range(12):
        house_sign = get_vedic_zodiac_sign(cusps[i])
        house_degree = cusps[i] % 30
        houses[f'House {i+1}'] = {
            'sign': house_sign,
            'degree': round(house_degree,2)
        }

    return houses

# Function to get full birth chart
def get_full_birth_chart(date_of_birth, latitude, longitude):
    # Calculate the planetary positions
    planetary_positions = calculate_planetary_positions(date_of_birth, latitude, longitude)

    # Calculate the Ascendant, Sun, and Moon signs
    vedic_astrological_signs = calculate_vedic_astrological_signs(date_of_birth, latitude, longitude)

    # Calculate the Houses in the birth chart
    houses = calculate_houses(date_of_birth, latitude, longitude)

    # Combine all the information into a single dictionary
    birth_chart = {
        'Planetary Positions': planetary_positions,
        'Ascendant, Sun, and Moon Signs': vedic_astrological_signs,
        'Houses': houses
    }

    return birth_chart

# Example usage
date_of_birth = "2001-07-15 21:05"
latitude, longitude = 26.7606, 83.3732

# Get the full birth chart as a dictionary
birth_chart = get_full_birth_chart(date_of_birth, latitude, longitude)

# Print the full birth chart
print(birth_chart)
