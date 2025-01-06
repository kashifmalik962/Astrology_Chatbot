import datetime
import swisseph as swe

# Function to get Vedic Zodiac Sign based on degree (with Lahiri Ayanamsha shift)
def get_vedic_zodiac_sign(degree):
    # Vedic zodiac signs
    vedic_zodiac_list = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 
                         'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
    # Shift by 24 degrees for Lahiri Ayanamsha and ensure degree wraps around
    degree = (degree - 24) % 360
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

# Example usage
date_of_birth = "2001-07-15 21:05"
latitude, longitude = 26.7606, 83.3732

# Calculate Vedic astrological signs
vedic_astrological_signs = calculate_vedic_astrological_signs(date_of_birth, latitude, longitude)

# Output the results
print(f"Rising Sign (Ascendant): {vedic_astrological_signs['Rising Sign']}")
print(f"Sun Sign (Zodiac): {vedic_astrological_signs['Sun Sign']}")
print(f"Moon Sign (Zodiac): {vedic_astrological_signs['Moon Sign']}")
