from fastapi import FastAPI, Response, WebSocket, WebSocketDisconnect, Request, UploadFile, File
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from io import BytesIO
import shutil
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
import requests
import os
from palmistry.code.tools import *
from palmistry.code.model import *
from palmistry.code.classifi import *
from palmistry.code.rectification import *
from palmistry.code.detection import *
from palmistry.code.measurement import *


API_KEY = "bda76f21-aad1-590f-923d-3d40f2678a1c"
VEDIC_BASE_API = f"https://api.vedicastroapi.com/v3-json"


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

a = """"
मंगल के 8वें भाव में होने और 11वें, 2वें और 3वें भाव को देखने के कारण आप पर मांगलिक दोष है। आपका काल-सर्प दोष से भी थोड़ा संबंध है, लेकिन इसे महत्वपूर्ण नहीं माना जाता है। इसके अतिरिक्त, आप 28% मांगलिक हैं, जो कि दोष का हल्का रूप है
"""

def hindi_to_roman(hindi_text):
    # print("hindi_to_roman func running...")
    impove_roman_word_dict = {"apa":"aap", "himdi": "hindi", "himglisha": "hinglish","maim":"main", "mem":"me","haim;":"hai," ,"hai|":"hai","haim|":"hain", "haim,":"hain","anuvada":"anuvaad", "vishesha":"vishesh","rupa":'roop', "mashina":"machine", "larnimga":"learning", "upayoga":"upyog", "apak":"aapka","apako":"aapko", "maॉdala":"model", "aura":"aur","para":"par", "thika":"thik","vrrishabha":"vrrishabh","sthitiyam":"sthitiya","vyavahara":"vyavahar","pahaluom":"pahalo",
               "tramsaphaॉrmara":"transformer","adharita":"aadharit", "labha":"labh", "anukulita":"anukulit", "hai|":"hai", "eka":"ek", "majabuta":"majbut", "upakarana":"upkaaran","dizaina":"design","yaha.n":"yahan", "isaka":"iska","chamdr":"chandra", "mahin":"mahina", "darshat":"darshata","mithuna":"mitthun", "chamdra":"chandra", "chamdrama":"chandrama", "sujhava":"sujhav","apane":"apne","graha":"grah","udaya":"uday","prabhavita":"prabhavit","jisase":"jisse", "taya":"tay","asa":"aas","pasa":"pas","satha":"sath","batachita":"baatcheet","karate":"karte","jij~nasu":"jigyasu","samvadashila":"samvadsheel","mesha":"meesh","bhavuka":"bhavuk","khuda":"khud","atmavishvasa":"atmavishvas","pramanika":"pramanika","prastuta":"prastut","asa-pasa":"aas-paas","dekha":"dekh","hu.n":"hun","vartamana":"vartmaan","vem":"ve","ghara":"ghar","charana":"charan","imgita":"imgit","karata":"karta","asurakshaom":"asurakshao","samane":"samne","lekina":"lekin","vikasa":"vikas","mela":"mel","samkhya":"sankhya","ju.de":"jude","samyojana":"samyojan","jivana":"jivan","kshetrom":"kshetro","shuruata":"shuruat","dhyana":"dhyaan","kemdrita":"kendritra","karane":"karne", "bahuta":"bahut","sumdara":"sundar","kainavasa":"kainvas","hu.n,":"hun,","aja":"aaj","akasha":"aaksh","chamaka":"chamak","akara":"aakar","nahim":"nahi","haim":"hai","sambamdha":"sambandh","chijem":"chije","vyavaharika":"vyavharik","ju.dava.n":"judava","jyotisha":"jyotish","atma":"aatm","khoja":"khoj","pratyeka":"pratyek","janma":"janm","anukula":"anukul","upayukta":"upyukt","kumdali":"kundali","madada":"madad","pasamda":"pasand","karumga":"karunga","salaha":"salah","pradana":"pradan","karumga|":"karunga","karum":"karu","samajha":"samajh","hamem":"hame","margadarshana":"margdarshan","nirbhara":"nirbhar", "svabhava":"svabhav","samketa":"sanket","apaka":"aapka","jala":"jal","vahaka":"vahak","svatamtrata":"swatantra","sparsha":"sparsh","manaviya":"manviya","mulamka":"mulank","shukra":"shukr","poshana":"poshan","bhara":"bhar","dekhabhala":"dekhbhal","bana":"ban","apamem":"aapme","aksara":"aksar","parivara":"parivar","shamti":"shanti","sthapita":"sthapit","sahayoga":"sahyog","jisamem":"jisme","dhyana":"dhyan","shamta":"shant","dina":"din","manasika":"mansik","amtarika":"aantarik","samtulana":"santulan","sadbhava":"sadbhav","karem":"kare","adhika":"adhik","prapta":"prapt","avasara":"avasar","bhava":"bhav","karana":"karan","mamgalika":"mangalik", "dosha":"dosh","mahatvapurna":"mahatvapurn","isake":"iske","atirikta":"atirikt", "mamgala":"mangal"}

    # Transliterate from Devanagari (Hindi) to Roman
    fresh_words = []

    roman_text = sanscript.transliterate(hindi_text, sanscript.DEVANAGARI, sanscript.ITRANS)
    # print(roman_text, "roman_text ....")
    for word in roman_text.lower().split():
        if word in impove_roman_word_dict.keys():
            fresh_words.append(impove_roman_word_dict[word])
        else:
            fresh_words.append(re.sub(r"[.!]", "", word))

    # print(fresh_words,"fresh_words")
    result = " ".join(fresh_words).replace("\n", " ")
    # print(result, "result")
    return result

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



def get_radical_no(year, month, day):
    api_entity = "utilities/radical-number-details?radical_number"
    dob = f"{day}/{month}/{year}"
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
            return {response_res["content"][0]}
        else:
            print(f"Failed to fetch horoscope data. Status code: {response.status_code}")
            return {}
    except requests.exceptions.RequestException as e:
        print(f"Error while making API call: {e}")
        return {}


def get_horoscope_data(year, month, day, hour, minute, birth_place_pin):
    print("func running...")
    api_entity_house = "extended-horoscope/kp-houses"
    api_entity_planet = "extended-horoscope/kp-planets"
    lat,lon = get_lat_long(birth_place_pin)
  

    # print(lat, lon, "birth_place_lat_lon")
    # print(VEDIC_BASE_API)

    try:
        response_house = requests.get(f"{VEDIC_BASE_API}/{api_entity_house}?dob={day}/{month}/{year}&tob={hour}:{minute}&lat={lat}&lon={lon}&tz=5.5&api_key={API_KEY}&lang=en")
        # print(response_house)  # Print the response_house status
        
        response_planet = requests.get(f"{VEDIC_BASE_API}/{api_entity_planet}?dob={day}/{month}/{year}&tob={hour}:{minute}&lat={lat}&lon={lon}&tz=5.5&api_key={API_KEY}&lang=en")
        
        # print(response_planet, "response_planet")
        
        if response_house.status_code == 200 and response_planet.status_code == 200:

            data_house = response_house.json()  # Parse JSON response
            horoscope_data_house = data_house.get("response", [])
            # print(horoscope_data)  # Debug: print parsed response

            # Extract desired data
            result = []
            for obj in horoscope_data_house:
                result.append({
                    "house": obj.get("house"),
                    "start_rasi": obj.get("start_rasi")
                })

            data_planet = response_planet.json()  # Parse JSON response
            horoscope_data_planet = data_planet.get("response", [])
            # print(horoscope_data_planet,"horoscope_data_planet")
            for dic in result:
                plants_lst = []
                for obj,val in horoscope_data_planet.items():
                    print(dic, obj, val)
                    try:
                        if dic["house"] == val.get("house"):
                            plants_lst.append(val.get("full_name"))
                            dic["planet"] = plants_lst
                    except:
                        pass
            return result
        else:
            print(f"Failed to fetch horoscope data. Status code: {response_house.status_code}")
            return {}
    except requests.exceptions.RequestException as e:
        print(f"Error while making API call: {e}")
        return {}



# Function to calculate Ascendant, Sun, and Moon Signs in Vedic astrology
def calculate_vedic_astrological_signs(year, month, day, hour, minute, birth_place_pin):

    lat,lon = get_lat_long(birth_place_pin)
    api_entity_sun_sign = "extended-horoscope/find-sun-sign"
    api_entity_moon_sign = "extended-horoscope/find-moon-sign"
    api_entity_rising_sign = "extended-horoscope/find-ascendant"

    try:
        sun_response = requests.get(f"{VEDIC_BASE_API}/{api_entity_sun_sign}?dob={day}/{month}/{year}&tob={hour}:{minute}&lat={lat}&lon={lon}&tz=5.5&api_key={API_KEY}&lang=en")
        moon_response = requests.get(f"{VEDIC_BASE_API}/{api_entity_moon_sign}?dob={day}/{month}/{year}&tob={hour}:{minute}&lat={lat}&lon={lon}&tz=5.5&api_key={API_KEY}&lang=en")
        rising_response = requests.get(f"{VEDIC_BASE_API}/{api_entity_rising_sign}?dob={day}/{month}/{year}&tob={hour}:{minute}&lat={lat}&lon={lon}&tz=5.5&api_key={API_KEY}&lang=en")

        print(sun_response, moon_response, rising_response)
        if sun_response.status_code == 200 and moon_response.status_code == 200 and rising_response.status_code == 200:
            sun_response_json = sun_response.json()
            moon_response_json = moon_response.json()
            rising_response_json = rising_response.json()
            
            sun_response_res = sun_response_json.get("response", [])
            moon_response_res = moon_response_json.get("response", [])
            rising_response_res = rising_response_json.get("response", [])
            
            print(sun_response_res, moon_response_res, rising_response_res, "++++++")

            return {
                "sun_sign": sun_response_res.get("sun_sign"),
                "moon_sign": moon_response_res.get("moon_sign"),
                "rising_sign": rising_response_res.get("ascendant")
            }
        else:
            print(f"Failed to fetch horoscope data. Status code: {sun_response.status_code, moon_response.status_code, rising_response.status_code}")
            return {}
    except requests.exceptions.RequestException as e:
        print(f"Error while making API call: {e}")
        return {}


def get_kundli_signs(year, month, day, hour, minute, birth_place_pin):

    lat,lon = get_lat_long(birth_place_pin)
    api_entity = "extended-horoscope/extended-kundli-details"
    
    try:
        response = requests.get(f"{VEDIC_BASE_API}/{api_entity}?dob={day}/{month}/{year}&tob={hour}:{minute}&lat={lat}&lon={lon}&tz=5.5&api_key={API_KEY}&lang=en")

        print(response)
        if response.status_code == 200:
            response_json = response.json()

            response_res = response_json.get("response", [])
            print(response_res, "++++++")

            return {
                "gana": response_res.get("gana"),
                "yoni": response_res.get("yoni"),
                "vasya": response_res.get("vasya"),
                "nadi": response_res.get("nadi"),
                "varna": response_res.get("varna"),
                "paya": response_res.get("paya"),
                "tatva": response_res.get("tatva"),
                "life_stone": response_res.get("life_stone"),
                "lucky_stone": response_res.get("lucky_stone"),
                "fortune_stone": response_res.get("fortune_stone"),
                "ascendant_sign": response_res.get("ascendant_sign"),
                "ascendant_nakshatra": response_res.get("ascendant_nakshatra"),
                "rasi": response_res.get("rasi"),
                "rasi_lord": response_res.get("rasi_lord"),
                "nakshatra": response_res.get("nakshatra"),
                "karana": response_res.get("karana"),
                "yoga": response_res.get("yoga")
            }
        else:
            print(f"Failed to fetch horoscope data. Status code: {response.status_code}")
            return {}
    except requests.exceptions.RequestException as e:
        print(f"Error while making API call: {e}")
        return {}
    

def get_current_location():
    import geocoder
    # Get the current location using IP
    location = geocoder.ip('me')
    if location.ok:
        return location.latlng  # Returns (latitude, longitude)
    else:
        print("location does not exist...")
        return None


def get_current_date_time():
    date = datetime.now().date()
    time = datetime.now().time()

    day, month, year = date.day, date.month, date.year
    hour, minute = time.hour, time.minute
    current_date, current_time = f"{day}/{month}/{year}", f"{hour}:{minute}"

    return current_date, current_time


def get_panchang_details():
    current_date, current_time = get_current_date_time()
    coordinates = get_current_location()
    tz = 5.5
    api_entity = "panchang/panchang"
    
    try:
        response = requests.get(f"{VEDIC_BASE_API}/{api_entity}?api_key={API_KEY}&date={current_date}&tz={tz}&lat={coordinates[0]}&lon={coordinates[1]}&time={current_time}&lang=en")

        # print(response)
        if response.status_code == 200:
            response_json = response.json()

            response_res = response_json.get("response", [])
            # print(response_res, "++++++")

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


def get_moon_rise_set():
    current_date, current_time = get_current_date_time()
    coordinates = get_current_location()
    tz = 5.5
    lang = "en"
    api_rise_entity = "panchang/moonrise"
    api_set_entity = "panchang/moonset"

    try:
        response_rise = requests.get(f"{VEDIC_BASE_API}/{api_rise_entity}?api_key={API_KEY}&date={current_date}&tz={tz}&lat={coordinates[0]}&lon={coordinates[1]}&time={current_time}&lang={lang}")
        response_set = requests.get(f"{VEDIC_BASE_API}/{api_set_entity}?api_key={API_KEY}&date={current_date}&tz={tz}&lat={coordinates[0]}&lon={coordinates[1]}&time={current_time}&lang={lang}")

        print(response_rise)
        print(response_set)
        if response_rise.status_code == 200 or response_set.status_code == 200:

            response_rise_json = response_rise.json()
            response_set_json = response_set.json()

            response_rise_res = response_rise_json.get("response", [])
            response_set_res = response_set_json.get("response", [])

            print(response_rise_res, "++++++")
            print(response_set_res, "++++++")

            print(response_rise_res["bot_response"], "response_rise_res['bot_response'] moon rise")
            print(response_set_res["bot_response"], "response_set_res['bot_response'] moon set")
            return {response_rise_res["bot_response"],response_set_res["bot_response"]}
        else:
            print(f"Failed to fetch horoscope data. Status code: {response_rise_res.status_code}")
            return {}
    except requests.exceptions.RequestException as e:
        print(f"Error while making API call: {e}")
        return {}


def get_sun_rise_set():
    current_date, current_time = get_current_date_time()
    coordinates = get_current_location()
    tz = 5.5
    lang = "en"
    api_rise_entity = "panchang/sunrise"
    api_set_entity = "panchang/sunset"

    try:
        response_rise = requests.get(f"{VEDIC_BASE_API}/{api_rise_entity}?api_key={API_KEY}&date={current_date}&tz={tz}&lat={coordinates[0]}&lon={coordinates[1]}&time={current_time}&lang={lang}")
        response_set = requests.get(f"{VEDIC_BASE_API}/{api_set_entity}?api_key={API_KEY}&date={current_date}&tz={tz}&lat={coordinates[0]}&lon={coordinates[1]}&time={current_time}&lang={lang}")

        if response_rise.status_code == 200 or response_set.status_code == 200:

            response_rise_json = response_rise.json()
            response_set_json = response_set.json()

            response_rise_res = response_rise_json.get("response", [])
            response_set_res = response_set_json.get("response", [])

            return {response_rise_res["bot_response"],response_set_res["bot_response"]}
        else:
            print(f"Failed to fetch horoscope data. Status code: {response_rise_res.status_code}")
            return {}
    except requests.exceptions.RequestException as e:
        print(f"Error while making API call: {e}")
        return {}


def get_mangal_dosh(year, month, day, hour, minute, birth_place_pin):
    lat,lon = get_lat_long(birth_place_pin)
    api_entity = "dosha/mangal-dosh"
    tz = 5.5
    lang = "en"

    try:
        response = requests.get(f"{VEDIC_BASE_API}/{api_entity}?dob={day}/{month}/{year}&tob={hour}:{minute}&lat={lat}&lon={lon}&tz={tz}&api_key={API_KEY}&lang={lang}")

        print(response)
        if response.status_code == 200:
            response_json = response.json()

            response_res = response_json.get("response", [])
            # print(response_res, "++++++")

            # print(response_res["factors"], "response_res['factors']")
            return {"manglik": response_res["bot_response"], 
                    "moon": response_res["factors"]["moon"], 
                    "saturn": response_res["factors"]["saturn"],
                    "is_dosha_present_mars_from_lagna":response_res["is_dosha_present_mars_from_lagna"],
                    "is_dosha_present_mars_from_moon":response_res["is_dosha_present_mars_from_moon"]
                    }
        else:
            print(f"Failed to fetch horoscope data. Status code: {response.status_code}")
            return {}
    except requests.exceptions.RequestException as e:
        print(f"Error while making API call: {e}")
        return {}


def get_kaalsarp_dosh(year, month, day, hour, minute, birth_place_pin):
    lat,lon = get_lat_long(birth_place_pin)
    api_entity = "dosha/kaalsarp-dosh"
    tz = 5.5
    lang = "en"

    try:
        response = requests.get(f"{VEDIC_BASE_API}/{api_entity}?dob={day}/{month}/{year}&tob={hour}:{minute}&lat={lat}&lon={lon}&tz={tz}&api_key={API_KEY}&lang={lang}")

        # print(response)
        if response.status_code == 200:
            response_json = response.json()

            response_res = response_json.get("response", [])
            # print(response_res, "++++++")

            return {"is_dosha_present": response_res["is_dosha_present"], "Kaal_Sarp":response_res["bot_response"]}
        else:
            print(f"Failed to fetch horoscope data. Status code: {response.status_code}")
            return {}
    except requests.exceptions.RequestException as e:
        print(f"Error while making API call: {e}")
        return {}
    

def get_manglik_dosh(year, month, day, hour, minute, birth_place_pin):
    lat,lon = get_lat_long(birth_place_pin)
    api_entity = "dosha/manglik-dosh"
    tz = 5.5
    lang = "en"

    try:
        response = requests.get(f"{VEDIC_BASE_API}/{api_entity}?dob={day}/{month}/{year}&tob={hour}:{minute}&lat={lat}&lon={lon}&tz={tz}&api_key={API_KEY}&lang={lang}")

        print(response)
        if response.status_code == 200:
            response_json = response.json()

            print(response_json)
            response_res = response_json.get("response", [])
            print(response_res, "++++++")

            return {
                "manglik_by_mars": response_res["manglik_by_mars"],
                "manglik_factor": response_res["factors"][0],
                "manglik": response_res["bot_response"],
                "aspects": response_res["aspects"],
                "manglik_by_saturn": response_res["manglik_by_saturn"],
                "manglik_by_rahuketu": response_res["manglik_by_rahuketu"]
            }
        else:
            print(f"Failed to fetch horoscope data. Status code: {response.status_code}")
            return {}
    except requests.exceptions.RequestException as e:
        print(f"Error while making API call: {e}")
        return {}


def get_pitra_dosh(year, month, day, hour, minute, birth_place_pin):
    lat,lon = get_lat_long(birth_place_pin)
    api_entity = "dosha/pitra-dosh"
    tz = 5.5
    lang = "en"

    try:
        response = requests.get(f"{VEDIC_BASE_API}/{api_entity}?dob={day}/{month}/{year}&tob={hour}:{minute}&lat={lat}&lon={lon}&tz={tz}&api_key={API_KEY}&lang={lang}")

        print(response)
        if response.status_code == 200:
            response_json = response.json()

            print(response_json)
            response_res = response_json.get("response", [])
            print(response_res, "++++++")

            return {
                "is_dosha_present": response_res["is_dosha_present"],
                "response": response_res["bot_response"]
            }
        else:
            print(f"Failed to fetch horoscope data. Status code: {response.status_code}")
            return {}
    except requests.exceptions.RequestException as e:
        print(f"Error while making API call: {e}")
        return {}


def calculate_mahadasha_differences(response):
    mahadasha = response["mahadasha"]
    mahadasha_order = response["mahadasha_order"]
    start_year = response["start_year"]

    differences = {}

    for i in range(len(mahadasha)):
        # Extract the year from the current mahadasha_order date
        current_year = datetime.strptime(mahadasha_order[i], "%a %b %d %Y").year

        if i == 0:
            # For the first mahadasha, calculate from start_year
            previous_year = start_year
        else:
            # For subsequent mahadashas, calculate from the previous mahadasha's year
            previous_year = datetime.strptime(mahadasha_order[i - 1], "%a %b %d %Y").year

        # Calculate the difference in years
        year_difference = current_year - previous_year
        differences[mahadasha[i].lower()] = f"{year_difference} years"

    return differences


def get_mahadasha(year, month, day, hour, minute, birth_place_pin):
    lat,lon = get_lat_long(birth_place_pin)
    api_entity = "dashas/maha-dasha"
    tz = 5.5
    lang = "en"

    try:
        response = requests.get(f"{VEDIC_BASE_API}/{api_entity}?dob={day}/{month}/{year}&tob={hour}:{minute}&lat={lat}&lon={lon}&tz={tz}&api_key={API_KEY}&lang={lang}")

        print(response)
        if response.status_code == 200:
            response_json = response.json()

            print(response_json)
            response_res = response_json.get("response", [])
            print(response_res, "++++++")

            # mahadasha = response_res["mahadasha"]
            # mahadasha_order = response_res["mahadasha_order"]
            # start_year = response_res["start_year"]

            result = calculate_mahadasha_differences(response_res)
            

            return result
        else:
            print(f"Failed to fetch horoscope data. Status code: {response.status_code}")
            return {}
    except requests.exceptions.RequestException as e:
        print(f"Error while making API call: {e}")
        return {}


# Function to get Vedic Zodiac Sign based on degree (with Lahiri Ayanamsha shift)
def get_vedic_zodiac_sign(degree):
    # Vedic zodiac signs
    vedic_zodiac_list = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 
                         'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
    # Shift by 24 degrees for Lahiri Ayanamsha and ensure degree wraps around
    degree = (degree - 24) % 360
    return vedic_zodiac_list[int(degree // 30)]


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
        print(question, "question language text...")
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
                tithi_yoga = ""
                kundli_signs = ""
                moon_rising_set = ""
                sun_rising_set = ""
                mangal_dosh = ""
                kaalsarp_dosh = ""
                manglik_dosh = ""
                pitra_dosh = ""
                mahadasha = ""
                
                if "zodiac_sign" in entity:
                    vedic_astrological_signs = calculate_vedic_astrological_signs(item.year,item.month,item.day,item.hour,item.minute,item.birth_place_pin)
                if "house_planets" in entity:
                    horoscope_data = get_horoscope_data(item.year,item.month,item.day,item.hour,item.minute,item.birth_place_pin)
                if "kundli_signs" in entity:
                    kundli_signs = get_kundli_signs(item.year,item.month,item.day,item.hour,item.minute,item.birth_place_pin)
                if "radical" in entity:
                    radical_no = get_radical_no(item.year,item.month,item.day)
                if "tithi_yoga" in entity:
                    tithi_yoga = get_panchang_details()
                if "moon_rising_set" in entity:
                    moon_rising_set = get_moon_rise_set()
                if "sun_rising_set"in entity:
                    sun_rising_set = get_sun_rise_set()
                if "mangal_dosh" in entity:
                    mangal_dosh = get_mangal_dosh(item.year,item.month,item.day,item.hour,item.minute,item.birth_place_pin)
                if "kaalsarp_dosh" in entity:
                    kaalsarp_dosh = get_kaalsarp_dosh(item.year,item.month,item.day,item.hour,item.minute,item.birth_place_pin)
                if "manglik_dosh" in entity:
                    manglik_dosh = get_manglik_dosh(item.year,item.month,item.day,item.hour,item.minute,item.birth_place_pin)
                if "pitra_dosh" in entity:
                    pitra_dosh = get_pitra_dosh(item.year,item.month,item.day,item.hour,item.minute,item.birth_place_pin)
                if "mahadasha" in entity:
                    mahadasha = get_mahadasha(item.year,item.month,item.day,item.hour,item.minute,item.birth_place_pin)
                if "lagna" in entity:
                    lagna_lord = calculate_lagna_lord(item.year,item.month,item.day,item.hour,item.minute,item.birth_place_pin)
                # if "birth_chart" in entity:
                #     birth_chart = get_full_birth_chart(item.year,item.month,item.day,item.hour,item.minute,item.birth_place_pin)
                # if "nakshatra" in entity:
                #     nakshatra = get_nakshatra_with_dasha()

                if vedic_astrological_signs or radical_no or horoscope_data or lagna_lord or birth_chart or nakshatra or tithi_yoga or kundli_signs or moon_rising_set or sun_rising_set or mangal_dosh or kaalsarp_dosh or manglik_dosh or pitra_dosh or mahadasha:
                    base_question = (
                        f"Only act as an astrologer and do not reply to questions other than astrology. "
                        f"this is my details {vedic_astrological_signs,radical_no,horoscope_data,lagna_lord, birth_chart,nakshatra, tithi_yoga, kundli_signs,moon_rising_set, sun_rising_set, mangal_dosh, kaalsarp_dosh, manglik_dosh, pitra_dosh, mahadasha} ."
                        f"Let's say the question is '{translated_text}'. "
                    )
                else:
                    base_question = (
                        f"Act as a conversational human astrologer and return user question like human astrologer. "
                        f"My birth details  {item.day}/{item.month}/{item.year} {item.hour}:{item.minute} pincode={item.birth_place_pin} "
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
                        "zodiac sign", "zodiac_sign", "zodaic sign", "sun sign", "moon sign","sun sin", "moon sin", "rising", "astrological sign", "aries", "taurus", "gemini",
                        "cancer", "leo", "virgo", "libra", "scorpio", "sagittarius", "capricorn",
                        "aquarius", "pisces", "lunar sign", "chandra rashi", "rashi", "chandra lagna", "rising sign", "ascendant", "ascendant sign", "joint sign"
                    ],
                    "house_planets": [
                        "house", "houses","bhava", "first house", "second house", "third house", "fourth house",
                        "fifth house", "sixth house", "seventh house", "eighth house", "ninth house",
                        "tenth house", "eleventh house", "twelfth house", "lagna bhava","planet", "planets","graha", "sun", "moon", "mars", "mercury", "jupiter", "jupyter" ,"venus",
                        "saturn", 
                    ],
                    "kundli_signs":["kundli_signs", "gana", "yoni", "vasya", "nadi","varna","paya","tatva","life stone", "lucky stone", "horoscope", "kundli signs","kundli sign", "birth chart", "signs", "natal chart", "kundli", "birth_chart", "horoscope chart"],

                    "radical":["radical", "radicals", "life path number", "path number", "path no" ,"destiny number", "destiny no"],
                    
                    "tithi_yoga": [
                        "yoga", "raj yoga", "dhan yoga", "gaja kesari yoga", "parivartana yoga","yoga","yog",
                        "vipareeta yoga", "laxmi yoga", "chandra mangala yoga", "karana", "yog","tithi", "tithi number", "tithi no","lunar_month", "lunar", "lunaar","vara", "varaa","rahukaal", "rahukal", "rahu","nakshatra", "naksatra", "naksatraa", "nakstra", "naksatar","karan","gulika","sun position", "moon position","rasi", "rashi","rasee","rashee", "day"
                    ],
                    
                    "moon_rising_set":["moon_rising_set", "moon rise", "moon set", "moon rice", "mon rice", "moon sets", "moon rising", "moon risings","mon rising", "moon ricing","mon rise"],
                    
                    "sun_rising_set":["sun_rising_set", "sun rise", "sun set", "sun rice", "san rice", "sun sets", "sun rising", "sun risings","san rising", "sun ricing","san rise"],
                    
                    "mangal_dosh":["mangal_dosh", "mangal dosh", "mangal dosha", "mangal dos", "mangal", "mangel", "mangel dos", "mangel dosh", "dosha"],
                    
                    "kaalsarp_dosh": ["kaalsarp_dosh", "kaalsarp dosh", "kaalsarp dosha", "kaalsarp dos", "kaalsarp", "kalsarp", "kalsarp dos", "kalsarp dosh"],

                    "manglik_dosh" : ["manglik_dosh", "manglik dosh", "manglik dosha", "manglik dos", "manglik", "manglek", "manglek dos", "manglek dosh"],

                    "pitra_dosh": ["pitra_dosh", "pitra dosh", "pitra dosha", "pitra dos", "pitra", "pitar", "pitar dos", "pitar dosh"],
                    
                    "mahadasha": ["mahadasha", "mahadasa", "mahadasha", "dasha", "dashas", "mahdasa", "mahdasha", "mahaadasha"]
                    # "lagna":["rahu", "ketu", "lagna lord", "ascendant lord", "lagna"],
                    # "birth_chart": [
                    #     "kundli", "birth chart", "birth_chart" ,"horoscope chart", "natal chart", "astrological chart",
                    #     "vedic chart", "janam kundli", "lagna chart", "janam patrika", "horoscope"
                    # ],
                    # "nakshatra": [
                    #     "nakshatra", "lunar mansion", "ashwini", "bharani", "kritika", "rohini",
                    #     "mrigashira", "ardra", "punarvasu", "pushya", "ashlesha", "magha", "purva phalguni",
                    #     "uttara phalguni", "hasta", "chitra", "swati", "vishakha", "anuradha", "jyestha",
                    #     "mula", "purva ashadha", "uttara ashadha", "shravana", "dhanishta", "shatabhisha",
                    #     "purva bhadrapada", "uttara bhadrapada", "revati", "dasha", "dasa", "vimshottari dasha", "mahadasha","yogini dasha"
                    # ],
                    
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
                    return {"answer":translated_text.replace("\n", " ")}
                
                elif "Based on your birth chart" in response or "Based on your birth details" in response or "Based on your Kundli" in response:
                    # translated_text = Translator.translate_text(response, from_language='auto', to_language='hi', translator='google')
                    translated_text = GoogleTranslator(source='auto', target='hi').translate(response)
                    print(userLanguage, "userLanguage", translated_text, "translated_text")
                    return {"answer":translated_text[translated_text.index(",")+2:].replace("\n", " ")}
                
                else:
                    # translated_text = Translator.translate_text(response, from_language='auto', to_language='hi', translator='google')
                    translated_text = GoogleTranslator(source='auto', target='hi').translate(response)
                    print(userLanguage, "userLanguage", translated_text, "translated_text")
                    return {"answer":translated_text.replace("\n", " ")}
                
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
                    print(userLanguage, "userLanguage", response, "response")
                    return {"answer":response[response.index("positive")+26:].replace("\n", " ")}
                elif "Based on your birth chart" in response or "Based on your birth details" in response or "Based on your Kundli" in response:
                    print(userLanguage, "userLanguage", response[response.index(",")+2:], "response")
                    return {"answer":response[response.index(",")+2:].replace("\n", " ")}
                else:
                    print(userLanguage, "userLanguage", response, "response")
                    return {"answer":response.replace("\n", " ")}
    except:
        return {"answer":"Not Found"}



@app.post("/palmistry")
async def palmistry(file: UploadFile = File(...)):
    try:
        # Save uploaded file to a temporary directory
        temp_dir = "./input"
        os.makedirs(temp_dir, exist_ok=True)
        input_file_path = os.path.join(temp_dir, file.filename)

        with open(input_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Define paths for intermediate and output results
        results_dir = "./palmistry/code/results"
        os.makedirs(results_dir, exist_ok=True)

        resize_value = 256
        path_to_clean_image = os.path.join(results_dir, "palm_without_background.jpg")
        path_to_warped_image = os.path.join(results_dir, "warped_palm.jpg")
        path_to_warped_image_clean = os.path.join(results_dir, "warped_palm_clean.jpg")
        path_to_warped_image_mini = os.path.join(results_dir, "warped_palm_mini.jpg")
        path_to_warped_image_clean_mini = os.path.join(results_dir, "warped_palm_clean_mini.jpg")
        path_to_palmline_image = os.path.join(results_dir, "palm_lines.png")
        path_to_model = "./palmistry/code/checkpoint/checkpoint_aug_epoch70.pth"
        path_to_result = os.path.join(results_dir, "result.jpg")

        # Step 0: Preprocess the image (remove background)
        remove_background(input_file_path, path_to_clean_image)

        # Step 1: Palm image rectification
        warp_result = warp(input_file_path, path_to_warped_image)
        if warp_result is None:
            print_error()
            return JSONResponse(status_code=400, content={"error": "Warping failed. Unable to process the image."})

        # Clean up and resize the warped image
        remove_background(path_to_warped_image, path_to_warped_image_clean)
        resize(
            path_to_warped_image,
            path_to_warped_image_clean,
            path_to_warped_image_mini,
            path_to_warped_image_clean_mini,
            resize_value,
        )

        # Step 2: Principal line detection
        net = UNet(n_channels=3, n_classes=1)
        net.load_state_dict(torch.load(path_to_model, map_location=torch.device("cpu")))
        detect(net, path_to_warped_image_clean, path_to_palmline_image, resize_value)

        # Step 3: Line classification
        lines = classify(path_to_palmline_image)

        # Step 4: Length measurement
        im, contents = measure(path_to_warped_image_mini, lines)

        # Step 5: Save result
        save_result(im, contents, resize_value, path_to_result)

        return JSONResponse(status_code=200, content={"message": "Palmistry analysis completed.", "result": contents})

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", reload=True)