# import swisseph as swe

# def get_zodiac_info(radical_number):
#     # Zodiac signs mapping using a dictionary for constant-time lookup
#     zodiac_signs = {
#         1: {"name": "Aries", "range": "0° - 30°"},
#         2: {"name": "Taurus", "range": "30° - 60°"},
#         3: {"name": "Gemini", "range": "60° - 90°"},
#         4: {"name": "Cancer", "range": "90° - 120°"},
#         5: {"name": "Leo", "range": "120° - 150°"},
#         6: {"name": "Virgo", "range": "150° - 180°"},
#         7: {"name": "Libra", "range": "180° - 210°"},
#         8: {"name": "Scorpio", "range": "210° - 240°"},
#         9: {"name": "Sagittarius", "range": "240° - 270°"},
#         10: {"name": "Capricorn", "range": "270° - 300°"},
#         11: {"name": "Aquarius", "range": "300° - 330°"},
#         12: {"name": "Pisces", "range": "330° - 360°"},
#     }
    
#     # Fetch zodiac information directly from the dictionary
#     zodiac = zodiac_signs.get(radical_number)
    
#     if zodiac:
#         return f'My zodiac sign is {zodiac["name"]}, Radical Number is: {radical_number}'
#     else:
#         return "Invalid Radical Number"

# def calculate_lagna(jd, latitude, longitude):
#     """
#     Calculate the Ascendant (Lagna) sign based on the Julian Day and geographical coordinates.
#     """
#     # Get the house cusps and Ascendant (first element of the tuple is Ascendant degree)
#     houses, ascendant = swe.houses(jd, latitude, longitude, b'P')
    
#     # Ascendant degree is the first element of the "houses" array
#     ascendant_degree = houses[0]
    
#     # Determine the zodiac sign for the Ascendant
#     sign_index = int(ascendant_degree / 30) + 1  # Divide by 30° for each zodiac sign
#     return sign_index




# birth_date = "2001-07-15"  # Format: YYYY-MM-DD
# birth_time = "21:05"  # Format: HH:MM
# latitude = 26.7658 # Replace with your birth latitude
# longitude = 83.0834  # Replace with your birth longitude

# # Convert date and time to Julian Day
# year, month, day = map(int, birth_date.split('-'))
# hour, minute = map(int, birth_time.split(':'))

# print(year, month, day, hour + minute / 60.0, "++++++++++++++++++++++++++")

# jd = swe.julday(year, month, day, hour + minute / 60.0)

# # Calculate Lagna
# lagna = calculate_lagna(jd, latitude, longitude)
# zodiac_info = get_zodiac_info(lagna)
# print(zodiac_info)


import requests

API_KEY = "bda76f21-aad1-590f-923d-3d40f2678a1c"
VEDIC_BASE_API = f"https://api.vedicastroapi.com/v3-json"

def get_radical_number(dob):
    api_entity = "utilities/radical-number-details?radical_number"
    dob_array = dob.split('/')
    day = int(dob_array[0])
    
    while day >= 10:
        day = sum(int(digit) for digit in str(day))

    try:
        response = requests.get(f"{VEDIC_BASE_API}/{api_entity}={day}&lang=en&api_key={API_KEY}")

        print(response)
        if response.status_code == 200:
            response_json = response.json()

            response_res = response_json.get("response", [])
            print(response_res, "++++++")

            print(response_res["content"][0], "response_res.content[0]")
            return {"response":response_res["content"][0]}
        else:
            print(f"Failed to fetch horoscope data. Status code: {response.status_code}")
            return {}
    except requests.exceptions.RequestException as e:
        print(f"Error while making API call: {e}")
        return {}

print(get_radical_number("15/07/2001"))