from fastapi import FastAPI, Response, WebSocket, WebSocketDisconnect, Request
from pydantic import BaseModel
import pandas as pd
import re
from nltk.corpus import stopwords
stopwords = stopwords.words('english')
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
porter = PorterStemmer()
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from vedicastro import VedicAstro
from langdetect import detect
import translators as Translator
from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from datetime import datetime
from geopy.geocoders import Nominatim
from indic_transliteration import sanscript
from fastapi.templating import Jinja2Templates
import swisseph as swe
from deep_translator import GoogleTranslator
import ephem


class Item(BaseModel):
    year:str=None
    month:str=None
    day:str=None
    hour:str=None
    minute:str=None
    birth_place_pin:str=None



utc = 5.5  # UTC offset for the time zone
latitude = 28.6139  # Example: Delhi latitude
longitude = 77.2090  # Example: Delhi longitude
ayanamsa = "Lahiri"
house_system = "Placidus"
return_style = "json"


def detect_hinglish(text):
    # print(text, "text in detect_hinglish")
    hindi_words = ['agar', 'jab','kab' ,'isliye', 'jabki', 'kyun', 'par', 'hogi' ,'phir', 'kaise', 'bas', 'hai', 'kya', 'apni' ,'koi', 'kis', 'mera', 'meri','sabhi', 'magar', 'aur', 'toh', 'lekin', 'kuch', 'kisne', 'jise', 'tum', 'he','aaj']  # Add more transliterated Hindi words
    hinglish = [word for word in hindi_words if word.lower() in text.split()]
    print(hinglish, "hinglish +++++++++")
    if len(hinglish) > 0:
        return "Hinglish"
    else:
        return detect(text)

a = """
आह, मेरे दोस्त, मुझे लगता है कि आप ज्योतिष के क्षेत्र में सत्य और प्रामाणिकता की तलाश कर रहे हैं। मैं इसे आपके साथ साझा करना चाहता हूँ: ज्योतिष एक ऐसा विज्ञान नहीं है जो सभी पर लागू हो, बल्कि यह एक जटिल प्रणाली है जिसके लिए सूक्ष्मता और समझ की आवश्यकता होती है। सितारे हमें मार्गदर्शन कर सकते हैं, लेकिन यह प्रत्येक व्यक्ति पर निर्भर करता है कि वह अपनी ब्रह्मांडीय भाषा की व्याख्या कैसे करे
"""

def hindi_to_roman(hindi_text):
    impove_roman_word_dict = {"apa":"aap", "himdi": "hindi", "himglisha": "hinglish","maim":"main", "mem":"me","haim;":"hai," ,"hai|":"hai","haim|":"hain", "haim,":"hain","anuvada":"anuvaad", "vishesha":"vishesh","rupa":'roop', "mashina":"machine", "larnimga":"learning", "upayoga":"upyog", "apak":"aapka","apako":"aapko", "maॉdala":"model", "aura":"aur","para":"par", "thika":"thik","vrrishabha":"vrrishabh","sthitiyam":"sthitiya","vyavahara":"vyavahar","pahaluom":"pahalo",
               "tramsaphaॉrmara":"transformer","adharita":"aadharit", "labha":"labh", "anukulita":"anukulit", "hai|":"hai", "eka":"ek", "majabuta":"majbut", "upakarana":"upkaaran","dizaina":"design","yaha.n":"yahan", "isaka":"iska","chamdr":"chandra", "mahin":"mahina", "darshat":"darshata","mithuna":"mitthun", "chamdra":"chandra", "chamdrama":"chandrama", "sujhava":"sujhav","apane":"apne","graha":"grah","udaya":"uday","prabhavita":"prabhavit","jisase":"jisse", "taya":"tay","asa":"aas","pasa":"pas","satha":"sath","batachita":"baatcheet","karate":"karte","jij~nasu":"jigyasu","samvadashila":"samvadsheel","mesha":"meesh","bhavuka":"bhavuk","khuda":"khud","atmavishvasa":"atmavishvas","pramanika":"pramanika","prastuta":"prastut","asa-pasa":"aas-paas","dekha":"dekh","hu.n":"hun","vartamana":"vartmaan","vem":"ve","ghara":"ghar","charana":"charan","imgita":"imgit","karata":"karta","asurakshaom":"asurakshao","samane":"samne","lekina":"lekin","vikasa":"vikas","mela":"mel","samkhya":"sankhya","ju.de":"jude","samyojana":"samyojan","jivana":"jivan","kshetrom":"kshetro","shuruata":"shuruat","dhyana":"dhyaan","kemdrita":"kendritra","karane":"karne", "bahuta":"bahut","sumdara":"sundar","kainavasa":"kainvas","hu.n,":"hun,","aja":"aaj","akasha":"aaksh","chamaka":"chamak","akara":"aakar","nahim":"nahi","haim":"hai","sambamdha":"sambandh","chijem":"chije","vyavaharika":"vyavharik","ju.dava.n":"judava","jyotisha":"jyotish","atma":"aatm","khoja":"khoj","pratyeka":"pratyek","janma":"janm","anukula":"anukul","upayukta":"upyukt","kumdali":"kundali","madada":"madad","pasamda":"pasand","karumga":"karunga","salaha":"salah","pradana":"pradan","karumga|":"karunga","karum":"karu","samajha":"samajh","hamem":"hame","margadarshana":"margdarshan","nirbhara":"nirbhar"}

    # Transliterate from Devanagari (Hindi) to Roman
    fresh_words = []

    roman_text = sanscript.transliterate(hindi_text, sanscript.DEVANAGARI, sanscript.ITRANS)
    for word in roman_text.lower().split():
        if word in impove_roman_word_dict.keys():
            fresh_words.append(impove_roman_word_dict[word])
        else:
            fresh_words.append(re.sub(r"[.!\]", "", word))
    print(fresh_words,"fresh_words")
    return " ".join(fresh_words)

def calculate_age(birth_year):
    current_year = datetime.now().year
    age = int(current_year) - int(birth_year)
    return age


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


def get_zodiac_info(radical_number):
    # Zodiac signs mapping using a dictionary for constant-time lookup
    zodiac_signs = {
        1: {"name": "Aries", "range": "0° - 30°"},
        2: {"name": "Taurus", "range": "30° - 60°"},
        3: {"name": "Gemini", "range": "60° - 90°"},
        4: {"name": "Cancer", "range": "90° - 120°"},
        5: {"name": "Leo", "range": "120° - 150°"},
        6: {"name": "Virgo", "range": "150° - 180°"},
        7: {"name": "Libra", "range": "180° - 210°"},
        8: {"name": "Scorpio", "range": "210° - 240°"},
        9: {"name": "Sagittarius", "range": "240° - 270°"},
        10: {"name": "Capricorn", "range": "270° - 300°"},
        11: {"name": "Aquarius", "range": "300° - 330°"},
        12: {"name": "Pisces", "range": "330° - 360°"},
    }
    
    # Fetch zodiac information directly from the dictionary
    zodiac = zodiac_signs.get(radical_number)
    
    if zodiac:
        return f'My zodiac sign is {zodiac["name"]}, Radical Number is: {radical_number}'
    else:
        return "Invalid Radical Number"

def calculate_lagna(jd, latitude, longitude):
    """
    Calculate the Ascendant (Lagna) sign based on the Julian Day and geographical coordinates.
    """
    # Get the house cusps and Ascendant (first element of the tuple is Ascendant degree)
    houses, ascendant = swe.houses(jd, latitude, longitude, b'P')
    
    # Ascendant degree is the first element of the "houses" array
    ascendant_degree = houses[0]
    
    # Determine the zodiac sign for the Ascendant
    sign_index = int(ascendant_degree / 30) + 1  # Divide by 30° for each zodiac sign
    return sign_index


def get_radical_no(year, month, day, hour, minute, birth_place_pin):

    birth_place_lat_lon = get_lat_long(birth_place_pin)

    # Get radical Lagna number
    jd = swe.julday(int(year), int(month), int(day), int(hour) + int(minute) / 60.0)
    lagna = calculate_lagna(jd, birth_place_lat_lon[0], birth_place_lat_lon[1])
    zodiac_info = get_zodiac_info(lagna)

    print(zodiac_info, "zodiac_info +++++++=====")
    return zodiac_info


def get_horoscope_data(year, month, day, hour, minute, birth_place_pin):
    birth_place_pin = get_lat_long(birth_place_pin)
    
    # Initialize Vedic Horoscope Data
    horoscope = VedicAstro.VedicHoroscopeData(
        int(year), int(month), int(day), int(hour), int(minute), 0,
        utc, int(birth_place_pin[0]), int(birth_place_pin[1]), ayanamsa, house_system
    )
    
    # Generate Chart
    chart = horoscope.generate_chart()

    # Extract details
    planets_data = horoscope.get_planets_data_from_chart(chart)
    houses_data = horoscope.get_houses_data_from_chart(chart)

    planets_houses_data = {
        "planets_data": planets_data,
        "houses_data": houses_data,
    }
    
    # Convert planets and houses data to dictionaries
    planets_data_list = [i._asdict() for i in planets_houses_data["planets_data"]]
    houses_data_list = [i._asdict() for i in planets_houses_data["houses_data"]]

    # Organize the data into dictionaries
    final_data = [{"planets_data": planets_data_list}, {"houses_data": houses_data_list}]
    
    # Function to format planets data with house and rasi information
    def format_planets_data(planets_data):
        house_lookup = {house['HouseNr']: house['Rasi'] for house in planets_data[1]['houses_data']}
        house_planets = {}

        # Group planets by house
        for planet in planets_data[0]['planets_data']:
            house = planet['HouseNr']
            planet_info = f"{planet['Object']}{', Retrograde' if planet['isRetroGrade'] else ''}"
            if house not in house_planets:
                house_planets[house] = []
            house_planets[house].append(planet_info)

        # Format the house details
        house_details = []
        for house, planets in house_planets.items():
            rasi = house_lookup.get(house, 'Unknown')
            house_details.append(f"House {house}: {rasi} ({', '.join(planets)})")
        
        return house_details

    # Format and return the final horoscope data
    formatted_planets_data = format_planets_data(final_data)
    
    return formatted_planets_data


# Function to get Vedic Zodiac Sign based on degree (with Lahiri Ayanamsha shift)
def get_vedic_zodiac_sign(degree):
    # Vedic zodiac signs
    vedic_zodiac_list = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 
                         'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
    # Shift by 24 degrees for Lahiri Ayanamsha and ensure degree wraps around
    degree = (degree - 24) % 360
    return vedic_zodiac_list[int(degree // 30)]

# Function to calculate Ascendant, Sun, and Moon Signs in Vedic astrology
def calculate_vedic_astrological_signs(year, month, day, hour, minute, birth_place_pin):

    birth_place_lat_lon = get_lat_long(birth_place_pin)

    # Convert birthdate to Julian Date
    jd_ut = swe.julday(int(year), int(month), int(day), int(hour) + int(minute) / 60.0)
    
    # Calculate Ascendant (Rising sign) with Lahiri Ayanamsha
    cusps, _ = swe.houses(jd_ut, birth_place_lat_lon[0], birth_place_lat_lon[1], b'P')
    ascendant_degree = cusps[0]  # Ascendant is the first house cusp
    rising_sign = get_vedic_zodiac_sign(ascendant_degree)
    
    # Calculate Sun and Moon Signs in Sidereal Zodiac
    sun_pos = swe.calc_ut(jd_ut, swe.SUN)[0]
    moon_pos = swe.calc_ut(jd_ut, swe.MOON)[0]
    sun_sign = get_vedic_zodiac_sign(sun_pos[0])
    moon_sign = get_vedic_zodiac_sign(moon_pos[0])
    
    print('Rising Sign is', rising_sign,
        'Sun Sign is', sun_sign,
        'Moon Sign is', moon_sign)
    
    return {
        'Rising Sign': rising_sign,
        'Sun Sign': sun_sign,
        'Moon Sign': moon_sign
    }


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
    jd = swe.julday(int(year), int(month), int(day), int(hour) + int(minute) / 60.0)
    
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



# Get Birth, Natal Chart, Kundli 
vedic_zodiac_list = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 
                     'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

# Function to get Vedic Zodiac Sign based on degree (with Lahiri Ayanamsha shift)
def get_vedic_zodiac_sign(degree):
    degree = (degree - 24) % 360  # Adjust by 24 degrees for Lahiri Ayanamsha
    return vedic_zodiac_list[int(degree // 30)]


# Function to calculate Planetary Positions in the Birth Chart
def calculate_planetary_positions(year, month, day, hour, minute, birth_place_pin):
    
    # Convert birthdate to Julian Date
    birth_place_lat_lon = get_lat_long(birth_place_pin)

    jd_ut = swe.julday(int(year), int(month), int(day), int(hour) + int(minute) / 60)

    # List of planets
    planets = [swe.SUN, swe.MOON, swe.MERCURY, swe.VENUS, swe.MARS, swe.JUPITER, swe.SATURN, swe.URANUS, swe.NEPTUNE, swe.PLUTO]
    planet_names = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto']

    planetary_positions = {}

    for i, planet in enumerate(planets):
        planet_pos = swe.calc_ut(jd_ut, planet)[0]
        planetary_positions[planet_names[i]] = [
            get_vedic_zodiac_sign(planet_pos[0]),
            round(planet_pos[0] % 30,2)  # degree within the sign
        ]

    return planetary_positions

# Function to calculate Houses in the Birth Chart
def calculate_houses(year, month, day, hour, minute, birth_place_pin):
    
    # Convert birthdate to Julian Date
    birth_place_lat_lon = get_lat_long(birth_place_pin)

    jd_ut = swe.julday(int(year), int(month), int(day), int(hour) + int(minute) / 60)

    # Calculate Houses with Lahiri Ayanamsha
    cusps, _ = swe.houses(jd_ut, birth_place_lat_lon[0], birth_place_lat_lon[1], b'P')
    
    houses = {}
    for i in range(12):
        house_sign = get_vedic_zodiac_sign(cusps[i])
        house_degree = cusps[i] % 30
        houses[f'House {i+1}'] = [
            house_sign,
            round(house_degree,2)
        ]

    return houses

# Function to get full birth chart
def get_full_birth_chart(year, month, day, hour, minute, birth_place_pin):
    # Calculate the planetary positions
    print("planetary_positions runnng.....")
    planetary_positions = calculate_planetary_positions(year, month, day, hour, minute, birth_place_pin)

    # Calculate the Ascendant, Sun, and Moon signs
    print("vedic_astrological_signs runnng.....")
    vedic_astrological_signs = calculate_vedic_astrological_signs(year, month, day, hour, minute, birth_place_pin)

    # Calculate the Houses in the birth chart
    print("calculate_houses runnng.....")
    houses = calculate_houses(year, month, day, hour, minute, birth_place_pin)

    print('Planetary Positions', planetary_positions,
        'Ascendant, Sun, and Moon Signs', vedic_astrological_signs,
        'Houses', houses)
    
    # Combine all the information into a single dictionary
    birth_chart = {
        'Planetary Positions': planetary_positions,
        'Ascendant, Sun, and Moon Signs': vedic_astrological_signs,
        'Houses': houses
    }

    return birth_chart

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

def get_nakshatra_with_dasha():

    year, month, day, hour, minute = extract_date_time_variables()
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

    # Function to get the Dasha based on the Nakshatra
    def get_dasha(date):
         # Use ephem to calculate planetary positions at a given time
        observer = ephem.Observer()
        observer.date = date
        
        # Get the current position of planets (e.g., Sun, Moon, etc.)
        sun = ephem.Sun(observer)
        moon = ephem.Moon(observer)
        venus = ephem.Venus(observer)
        jupiter = ephem.Jupiter(observer)
        
        # Return the longitudes of the planets in degrees
        return sun, moon, venus, jupiter
    
    
    # Get the Dasha for the current Nakshatra
    planet_positions = get_dasha(f"{year}-{month}-{day}")
    # Convert the positions from hours to degrees and print
    for planet in planet_positions:
        # Convert from hours (ephem.hlon) to degrees
        longitude_in_degrees = planet.hlon * 15  # 1 hour = 15 degrees
        if planet.name == "Moon":
            moon_longitude = round(longitude_in_degrees,2)
            print(moon_longitude)

    # Get Nakshatra name
    nakshatra_name = get_nakshatra(moon_longitude)

    return {"moon_longitude":moon_longitude, "current nakshatra is ":nakshatra_name, "current_dasha":moon_longitude}


def get_yoga_and_karana():
    year, month, day, hour, minute = extract_date_time_variables()
    # Use ephem to calculate planetary positions at a given time
    observer = ephem.Observer()
    observer.date = f"{year}-{month}-{day}"
    
    # Get the positions of the Sun and Moon
    sun = ephem.Sun(observer)
    moon = ephem.Moon(observer)
    
    # Calculate the angular distance between Sun and Moon in degrees
    angle_between_sun_moon = abs(sun.hlon - moon.hlon)
    
    # Ensure the angle is within 0 to 180 degrees
    if angle_between_sun_moon > 180:
        angle_between_sun_moon = 360 - angle_between_sun_moon
    
    # 1 Yoga = 13.33° (360° / 27)
    yoga_index = int(angle_between_sun_moon // 13.33)
    
    # 1 Karana = 25.71° (360° / 14)
    karana_index = int(angle_between_sun_moon // 25.71)
    
    # List of Yoga names (27 Yogas)
    yogas = [
        "Vishkumbh", "Priti", "Ayushman", "Sowbhagya", "Shobhana", "Atiganda", "Sukarma",
        "Dhriti", "Shoola", "Gand", "Vridhi", "Dhruva", "Vyagha", "Harshana", "Vajra",
        "Siddhi", "Vyatipata", "Variyana", "Parigha", "Shiva", "Sandhi", "Brahma", "Indra",
        "Vaidhriti", "Vishkumbh", "Priti", "Ayushman", "Sowbhagya"
    ]
    
    # List of Karana names (11 Karanas)
    karanas = ["Bava", "Balava", "Kaulava", "Taitila", "Garija", "Vaidhrti", "Shakuni", 
               "Chatushpada", "Naga", "Kimstughna", "Shakuni"]

    # Yoga and Karana based on the index
    yoga = yogas[yoga_index % len(yogas)]  # Ensure it's within 27
    karana = karanas[karana_index % len(karanas)]  # Ensure it's within 11
    
    return {"yoga": yoga, "karana": karana}


def get_tithi_vara_lunar_month_hora():
    # Set the Julian Day for the given date
    year, month, day, hour, minute = extract_date_time_variables()
    jd = swe.julday(int(year), int(month), int(day), 0)  # Julian day at midnight

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
    return {"Tithi": [tithi_number, tithi_name], "vara": vara, "lunar_month": lunar_month, "hora":hora}


# Create object of tf-idf class
cv = TfidfVectorizer()


app = FastAPI()

# Convert Lowercase
def cnvrtLowerCase(text):
    lowercase = text.lower()
    return lowercase

# Remove HTML tag
def removeHtmlTag(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

# Remove URL with the help of RegEX Library
def removeUrls(text):
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    return url_pattern.sub('', text)


# Remove Punctuation with the help of RegEX Library
def removePunctuation(text):
    return re.sub(r'[^\w\s]', '', text)

# Function of removing stopwords
def removeStopwords(text):
    str = []
    for i in text.split():
        if i not in stopwords:
            str.append(i)
    return " ".join(str)

# Replacing Quatation
def removeQuatation(text):
    text = text.replace("'","")
    return text.replace('"',"")

# Tokenize word into token
def tokenize(text):
    return word_tokenize(text)

# Function of stemming
def stemming(text):
    stemmed_word = [porter.stem(word) for word in text]
    return stemmed_word


templates = Jinja2Templates(directory="templates")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

global similarity, df, questions

@app.get("/re-train")
async def reTrainModel():
    global similarity, questions, df
    df = pd.read_csv("data/data.csv", encoding='ISO-8859-1')
    df["Questions"] = df["Questions"].apply(lambda x: cnvrtLowerCase(x))
    df["Questions"] = df["Questions"].apply(lambda x: removeHtmlTag(x))
    df["Questions"] = df["Questions"].apply(lambda x: removeUrls(x))
    df["Questions"] = df["Questions"].apply(lambda x: removePunctuation(x))
    # df["Questions"] = df["Questions"].apply(lambda x: removeStopwords(x))
    df["Questions"] = df["Questions"].apply(lambda x: removeQuatation(x))
    # df["Questions"] = df["Questions"].apply(lambda x: tokenize(x))
    # df["Questions"] = df["Questions"].apply(lambda x: stemming(x))
    
    
    questions = df["Questions"].tolist()
    print(df["Questions"])
    vectors = cv.fit_transform(df["Questions"]).toarray()
    
    similarity = cosine_similarity(vectors)
    
    print(list(sorted(enumerate(similarity[17]), reverse=True, key=lambda x:x[1]))[0])
    
    return {"response":"Successfully Re-trained"}


@app.post("/getAnswer")
async def getAnswer(question:str, item:Item, response:Response, request: Request):
    global questions, df, userLanguage,  year, month, day, hour , minute, second, birth_place_pin
    
    detect_lang_user = detect_hinglish(question)

    # detect_lang_user = detect(question)
    print(detect_lang_user, "detect_lang_user ++")
    
    if detect_lang_user == "hi":
        # translated_text = Translator.translate_text(question, from_language='auto', to_language='en', translator='google')
        translated_text = GoogleTranslator(source='auto', target='en').translate(question)
        print(translated_text, "convert question ++")
        userLanguage = "hi"
        text = cnvrtLowerCase(removeHtmlTag(removeUrls(removePunctuation(removeQuatation(translated_text)))))
        print(text, "text")
    elif detect_lang_user == "Hinglish":
        # translated_text = Translator.translate_text(question, from_language='auto', to_language='hi', translator='google')
        # translated_text = Translator.translate_text(question, from_language='auto', to_language='en', translator='google')
        translated_text = GoogleTranslator(source='auto', target='en').translate(question)
        print(translated_text, "convert question Hinglish ++")
        userLanguage = "Hinglish"
        text = cnvrtLowerCase(removeHtmlTag(removeUrls(removePunctuation(removeQuatation(translated_text)))))
    else:
        userLanguage = "en"
        translated_text = question
        text = cnvrtLowerCase(removeHtmlTag(removeUrls(removePunctuation(removeQuatation(question)))))
    print(userLanguage, "userLanguage ++++++++++")
    # Create token of querry
    user_vector = cv.transform([text]).toarray()
    
    # Calculate similarity with stored questions
    similarities = sorted(list(enumerate(cosine_similarity(user_vector, cv.transform(questions).toarray())[0])), reverse=True, key=lambda x: x[1])[0]
    print(similarities, "similarities")
    
    try:
        if similarities[1] > .80:
            print(df["Answer"][similarities[0]])
            if userLanguage == "hi":
                # translated_text = Translator.translate_text(df["Answer"][similarities[0]],from_language='auto', to_language='hi', translator='google')
                translated_text = GoogleTranslator(source='auto', target='hi').translate(df["Answer"][similarities[0]])
                return {"answer":translated_text}
            elif userLanguage == "Hinglish":
                # translated_text = Translator.translate_text(df["Answer"][similarities[0]],from_language='auto', to_language='hi', translator='google')
                translated_text = GoogleTranslator(source='auto', target='hi').translate(df["Answer"][similarities[0]])
                roman_text = hindi_to_roman(translated_text)
                return {"answer":roman_text}
            else:
                return {"answer":df["Answer"][similarities[0]]}
        else:
            print("llama model running......")

            def generate_question(translated_text, entity=None , age=None):
                """Generate the appropriate question based on age."""
                print(entity, "entity in generate_question")
                
                vedic_astrological_signs = ""
                radical_no = ""
                horoscope_data = ""
                lagna_lord = ""
                birth_chart = ""
                nakshatra = ""
                yogas = ""
                tithi = ""
                
                if "zodiac_sign" in entity:
                    vedic_astrological_signs = calculate_vedic_astrological_signs(item.year,item.month,item.day,item.hour,item.minute,item.birth_place_pin)
                if "radical" in entity:
                    radical_no = get_radical_no(item.year,item.month,item.day,item.hour,item.minute,item.birth_place_pin)
                if "house_planets" in entity:
                    horoscope_data = get_horoscope_data(item.year,item.month,item.day,item.hour,item.minute,item.birth_place_pin)
                if "lagna" in entity:
                    lagna_lord = calculate_lagna_lord(item.year,item.month,item.day,item.hour,item.minute,item.birth_place_pin)
                if "birth_chart" in entity:
                    birth_chart = get_full_birth_chart(item.year,item.month,item.day,item.hour,item.minute,item.birth_place_pin)
                if "nakshatra" in entity:
                    nakshatra = get_nakshatra_with_dasha()
                if "yogas" in entity:
                    yogas = get_yoga_and_karana()
                if "tithi" in entity:
                    tithi = get_tithi_vara_lunar_month_hora()
                
                if vedic_astrological_signs or radical_no or horoscope_data or lagna_lord or birth_chart or nakshatra or yogas or tithi:
                    base_question = (
                        f"Only act as an astrologer and do not reply to questions other than astrology. "
                        f"this is my details {vedic_astrological_signs,radical_no,horoscope_data,lagna_lord, birth_chart,nakshatra, yogas, tithi} ."
                        f"Let's say the question is '{translated_text}'. "
                    )
                else:
                    base_question = (
                        f"Act as a conversational human astrologer and return user question like human astrologer. "
                        # f"Please only respond to question related to astrology and conversation. "
                        # f"My question is: '{translated_text}'."
                        f"user question is '{translated_text}'. "
                    )

                if age < 15:
                    print(base_question + "Considering my age is under 15, please give an answer in 50 to 60 words only.")
                    return base_question + "Considering my age is under 15, please give an answer in 50 to 60 words only."
                elif age > 50:
                    print(base_question + "Considering my age is greater than 50, please give an answer in 50 to 60 words only.")
                    return base_question + "Considering my age is greater than 50, please give an answer in 50 to 60 words only."
                else:
                    print(base_question + "please give an answer in 50 to 60 words only.")
                    return base_question + "please give an answer in 50 to 60 words only."
                
            
            data = await request.json()
            print("Raw data received:", data)
            
            try:
                # Extract `item` from the parsed data
                item_data = data.get('item')
                print("Parsed item:", item_data)
                item_data["year"]
            except:
                item_data = data
            
            # Convert dictionary into Pydantic model for dot notation access
            item = Item(**item_data)
            
            # print("horoscope_data running...",item.year,item.month,item.day,item.hour,item.minute,item.birth_place_pin)

            print("template running ...")
            template = """
                Answer the question below:
                
                here the conversational history: {history}
                
                Question: {question}
                
                Answer:
            """
            
            print("model running...")
            model = OllamaLLM(model="llama3.2:latest", temperature=0.1, top_k=10, top_p=0.8)
            prompt = ChatPromptTemplate.from_template(template)
            memory = ConversationBufferMemory(input_key="question", memory_key="history")
            chain = LLMChain(llm=model, prompt=prompt, memory=memory)
            
            age = calculate_age(item.year)
            # Generate question and get response
            try:
                import re
                # Define keywords and entities
                keywords = {
                    "zodiac_sign": [
                        "zodiac sign", "zodiac_sign", "zodaic sign", "sun sign", "moon sign","astrological sign", "aries", "taurus", "gemini",
                        "cancer", "leo", "virgo", "libra", "scorpio", "sagittarius", "capricorn",
                        "aquarius", "pisces", "lunar sign", "chandra rashi", "rashi", "chandra lagna", "rising sign", "ascendant", "ascendant sign", "joint sign"
                    ],
                    "radical":["radical", "radicals", "life path number", "path number", "path no" ,"destiny number", "destiny no"],
                    "house_planets": [
                        "house", "bhava", "first house", "second house", "third house", "fourth house",
                        "fifth house", "sixth house", "seventh house", "eighth house", "ninth house",
                        "tenth house", "eleventh house", "twelfth house", "lagna bhava","planet", "planets","graha", "sun", "moon", "mars", "mercury", "jupiter", "jupyter" ,"venus",
                        "saturn", 
                    ],
                    "lagna":["rahu", "ketu", "lagna lord", "ascendant lord", "lagna"],
                    "birth_chart": [
                        "kundli", "birth chart", "birth_chart" ,"horoscope chart", "natal chart", "astrological chart",
                        "vedic chart", "janam kundli", "lagna chart", "janam patrika", "horoscope"
                    ],
                    "nakshatra": [
                        "nakshatra", "lunar mansion", "ashwini", "bharani", "kritika", "rohini",
                        "mrigashira", "ardra", "punarvasu", "pushya", "ashlesha", "magha", "purva phalguni",
                        "uttara phalguni", "hasta", "chitra", "swati", "vishakha", "anuradha", "jyestha",
                        "mula", "purva ashadha", "uttara ashadha", "shravana", "dhanishta", "shatabhisha",
                        "purva bhadrapada", "uttara bhadrapada", "revati", "dasha", "dasa", "vimshottari dasha", "mahadasha","yogini dasha"
                    ],
                    "yogas": [
                        "yoga", "raj yoga", "dhan yoga", "gaja kesari yoga", "parivartana yoga",
                        "vipareeta yoga", "laxmi yoga", "chandra mangala yoga", "karana", "yog"
                    ],
                    "tithi": ["tithi", "tithi number", "tithi no","lunar_month", "lunar", "lunaar","vara", "varaa"],
                    # "transits": [
                    #     "transit", "gochar", "planetary transit", "saturn transit", "rahu transit",
                    #     "ketu transit", "jupiter transit", "venus transit", "retrograde", "direct motion"
                    # ],
                    # "aspects": [
                    #     "aspect", "drishti", "planetary aspect", "full aspect", "partial aspect",
                    #     "graha drishti"
                    # ],
                    # "elements": [
                    #     "element", "tattva", "fire sign", "earth sign", "air sign", "water sign",
                    #     "fire element", "earth element", "air element", "water element"
                    # ],
                    # "compatibility": [
                    #     "compatibility", "relationship compatibility", "love compatibility", "marriage compatibility",
                    #     "synastry", "matching kundli", "guna matching", "ashtakoota matching", "score"
                    # ],
                    # "remedies": [
                    #     "remedy", "upaya", "astrological remedy", "gemstone", "mantra", "yantra",
                    #     "homa", "puja", "fasting", "donation"
                    # ],
                    # "timing": [
                    #     "timing", "muhurta", "auspicious time", "shubh muhurta", "marriage muhurta",
                    #     "grahapravesha muhurta", "naming ceremony muhurta", "baby naming muhurta"
                    # ],
                }

                def extractEntity(query):
                    entities = []
                    for entity, variations in keywords.items():
                        for variation in variations:
                            if re.search(rf"\b{re.escape(variation)}\b", query, re.IGNORECASE):
                                entities.append(entity)
                    return entities

                entity = extractEntity(translated_text)
                print(translated_text, "translated_text")
                print(entity, "extract entity")
                # Generate the question "zodiac_sign" or "moon_sign" or "rising_sign"
 
                question = generate_question(translated_text, entity, age)
                response = chain.invoke({"context": memory.load_memory_variables({})["history"], "question": question})
                result = response["text"]

            except Exception as e:
                print(f"Model invocation failed with error: {e}")
            
            response = result

            print(response, "+++")
            if userLanguage == "hi":
                if "positive interpretation" in response or "positive prediction" in response:
                    response = response[response.index("positive")+26:]
                    # translated_text = Translator.translate_text(response, from_language='auto', to_language='hi', translator='google')
                    translated_text = GoogleTranslator(source='auto', target='hi').translate(response)
                    print(userLanguage, "userLanguage", translated_text, "translated_text")
                    return {"answer":translated_text}
                
                elif "Based on your birth chart" in response or "Based on your birth details" in response or "Based on your Kundli" in response:
                    # translated_text = Translator.translate_text(response, from_language='auto', to_language='hi', translator='google')
                    translated_text = GoogleTranslator(source='auto', target='hi').translate(response)
                    print(userLanguage, "userLanguage", translated_text, "translated_text")
                    return {"answer":translated_text[translated_text.index(",")+2:]}
                
                else:
                    # translated_text = Translator.translate_text(response, from_language='auto', to_language='hi', translator='google')
                    translated_text = GoogleTranslator(source='auto', target='hi').translate(response)
                    print(userLanguage, "userLanguage", translated_text, "translated_text")
                    return {"answer":translated_text}
                
            elif userLanguage == "Hinglish":
                if "positive interpretation" in response or "positive prediction" in response:
                    response = response[response.index("positive")+26:]
                    # translated_text = Translator.translate_text(response, from_language='auto', to_language='hi', translator='google')
                    translated_text = GoogleTranslator(source='auto', target='hi').translate(response)
                    print(translated_text, "translated_text before apply hindi_to_roman")
                    roman_text = hindi_to_roman(translated_text)
                    print(roman_text)
                    print(userLanguage, "userLanguage", roman_text, "roman_text")
                    return {"answer": roman_text}
                
                elif "Based on your birth chart" in response or "Based on your birth details" in response or "Based on your Kundli" in response:
                    response = response[response.index(",")+2:]
                    # translated_text = Translator.translate_text(response, from_language='auto', to_language='hi', translator='google')
                    translated_text = GoogleTranslator(source='auto', target='hi').translate(response)
                    print(translated_text, "translated_text before apply hindi_to_roman")
                    roman_text = hindi_to_roman(translated_text)
                    print(userLanguage, "userLanguage", roman_text, "roman_text")
                    return {"answer":roman_text}

                else:
                    # translated_text = Translator.translate_text(response, from_language='auto', to_language='hi', translator='google')
                    translated_text = GoogleTranslator(source='auto', target='hi').translate(response)
                    print(translated_text, "translated_text before apply hindi_to_roman")
                    roman_text = hindi_to_roman(translated_text)
                    print(userLanguage, "userLanguage", roman_text, "roman_text")
                    return {"answer":roman_text}
                
            else:
                # User by-default language is english
                
                if "positive interpretation" in response or "positive prediction" in response:
                    response = response[response.index("positive")+26:]
                    print(userLanguage, "userLanguage", response, "response")
                    return {"answer":response}
                elif "Based on your birth chart" in response or "Based on your birth details" in response or "Based on your Kundli" in response:
                    print(userLanguage, "userLanguage", response[response.index(",")+2:], "response")
                    return {"answer":response[response.index(",")+2:]}
                else:
                    print(userLanguage, "userLanguage", response, "response")
                    return {"answer":response}
    except:
        return {"answer":"Not Found"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", reload=True)