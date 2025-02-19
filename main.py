from fastapi import FastAPI, Response, WebSocket, WebSocketDisconnect, Request, UploadFile, File
from fastapi.responses import JSONResponse, FileResponse
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
import requests
import os
from palmistry.code.tools import *
from palmistry.code.model import *
from palmistry.code.classifi import *
from palmistry.code.rectification import *
from palmistry.code.detection import *
from palmistry.code.measurement import *
# from vedicastro import VedicAstro
# from deep_translator import GoogleTranslator


API_KEY = "a9a96b0a-fbfb-593b-b0dc-2ca6306964a0"
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



def hindi_to_roman(hindi_text):
    # print("hindi_to_roman func running...")
    impove_roman_word_dict = {"apa":"aap", "himdi": "hindi", "himglisha": "hinglish","maim":"main", "mem":"me","haim;":"hai," ,"hai|":"hai","haim|":"hain", "haim,":"hain","anuvada":"anuvaad", "vishesha":"vishesh","rupa":'roop', "mashina":"machine", "larnimga":"learning", "upayoga":"upyog", "apak":"aapka","apako":"aapko", "maॉdala":"model", "aura":"aur","para":"par", "thika":"thik","vrrishabha":"vrrishabh","sthitiyam":"sthitiya","vyavahara":"vyavahar","pahaluom":"pahalo",
               "tramsaphaॉrmara":"transformer","adharita":"aadharit", "labha":"labh", "anukulita":"anukulit", "hai|":"hai", "eka":"ek", "majabuta":"majbut", "upakarana":"upkaaran","dizaina":"design","yaha.n":"yahan", "isaka":"iska","chamdr":"chandra", "mahin":"mahina", "darshat":"darshata","mithuna":"mitthun", "chamdra":"chandra", "chamdrama":"chandrama", "sujhava":"sujhav","apane":"apne","graha":"grah","udaya":"uday","prabhavita":"prabhavit","jisase":"jisse", "taya":"tay","asa":"aas","pasa":"pas","satha":"sath","batachita":"baatcheet","karate":"karte","jij~nasu":"jigyasu","samvadashila":"samvadsheel","mesha":"meesh","bhavuka":"bhavuk","khuda":"khud","atmavishvasa":"atmavishvas","pramanika":"pramanika","prastuta":"prastut","asa-pasa":"aas-paas","dekha":"dekh","hu.n":"hun","vartamana":"vartmaan","vem":"ve","ghara":"ghar","charana":"charan","imgita":"imgit","karata":"karta","asurakshaom":"asurakshao","samane":"samne","lekina":"lekin","vikasa":"vikas","mela":"mel","samkhya":"sankhya","ju.de":"jude","samyojana":"samyojan","jivana":"jivan","kshetrom":"kshetro","shuruata":"shuruat","dhyana":"dhyaan","kemdrita":"kendritra","karane":"karne", "bahuta":"bahut","sumdara":"sundar","kainavasa":"kainvas","hu.n,":"hun,","aja":"aaj","akasha":"aaksh","chamaka":"chamak","akara":"aakar","nahim":"nahi","haim":"hai","sambamdha":"sambandh","chijem":"chije","vyavaharika":"vyavharik","ju.dava.n":"judava","jyotisha":"jyotish","atma":"aatm","khoja":"khoj","pratyeka":"pratyek","janma":"janm","anukula":"anukul","upayukta":"upyukt","kumdali":"kundali","madada":"madad","pasamda":"pasand","karumga":"karunga","salaha":"salah","pradana":"pradan","karumga|":"karunga","karum":"karu","samajha":"samajh","hamem":"hame","margadarshana":"margdarshan","nirbhara":"nirbhar", "svabhava":"svabhav","samketa":"sanket","apaka":"aapka","jala":"jal","vahaka":"vahak","svatamtrata":"swatantra","sparsha":"sparsh","manaviya":"manviya","mulamka":"mulank","shukra":"shukr","poshana":"poshan","bhara":"bhar","dekhabhala":"dekhbhal","bana":"ban","apamem":"aapme","aksara":"aksar","parivara":"parivar","shamti":"shanti","sthapita":"sthapit","sahayoga":"sahyog","jisamem":"jisme","dhyana":"dhyan","shamta":"shant","dina":"din","manasika":"mansik","amtarika":"aantarik","samtulana":"santulan","sadbhava":"sadbhav","karem":"kare","adhika":"adhik","prapta":"prapt","avasara":"avasar","bhava":"bhav","karana":"karan","mamgalika":"mangalik", "dosha":"dosh","mahatvapurna":"mahatvapurn","isake":"iske","atirikta":"atirikt", "mamgala":"mangal", "adhara":"aadhar", "para":"par", "haim:":"hain", "brrihaspati ":"brhaspati", "uttara":"uttar","bedaruma":"bedroom","dakshina":"dakshin","sabase": "sabse","dvara":"dvar","bachem":"bache","pashchima":"pashchim"}

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


# Remove special character from string
def remove_special_characters(input_string):
    # print("remove_special_characters func runn....")
    # Regular expression to keep only alphanumeric characters and periods
    result = re.sub(r'[^a-zA-Z0-9\s.]', '', input_string)
    return result

# Remove question from answer
def remove_ques_from_ans(question, answer):
    question = question.lower()
    answer = answer.lower()
    # print(question, "question", answer, "answer in remove_ques_from_ans")
    if question in answer:
        new_answer =  remove_special_characters(answer.replace(question, ""))
        return new_answer
    return remove_special_characters(answer)

# Get planet from question/text
def get_planet_from_text(question):
    lst = ["sun", "moon", "mercury", "venus", "mars", "saturn", "jupiter", "jupyter", "rahu", "ketu"]
    for word in question.split():
        if word.lower() in lst:
            if word.lower() == "jupyter":
                return "jupiter"
            return word.lower()

    return "sun"

# Get gems from question/text
def get_gem_from_text(question):
    lst = ["cat_eye", "cat eye", "diamond", "ruby", "pearl", "coral", "gomedhaka", "yellow_sapphire", "blue_sapphire", "emerald"]
    for word in question.split():
        if word.lower() in lst:
            if word.lower() == "cat eye":
                return "cat_eye"
            return word.lower()

    return "coral"


# Get vastu no from question/text
def get_nakshatra_vastu_no(question):
    for word in question.split():
        # print(word, type(word))
        try:
            if int(word) in range(1,28):
                # print("inner no")
                return word
        except:
            pass

    return 1


# User-Question related to Greeting
def is_greeting(user_input):
    # List of common greetings
    greetings = [
        "hi", "hii", "hello", "hey", "hyy", "heyy","namaste", "greetings", 
        "good morning", "good afternoon", "good evening",
         "what's up", "how are you", "how do you do", "shubh prabhat",  "as-salamu alaykum", "marhaba"
    ]
    
    # Normalize user input (lowercase and strip extra spaces)
    user_input = user_input.lower().strip()
    
    # Check if the input is in the greetings list or contains a greeting as a substring
    for greeting in greetings:
        if greeting in user_input:
            return True
    return False


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
            # print(response_res, "++++++")

            # print(response_res["content"][0], "response_res.content[0]")
            return {"Radical no =>":response_res["content"][0]}
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
            result = ["house and planets =>"]
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
                plants_degree = []
                for obj,val in horoscope_data_planet.items():
                    # print(dic, obj, val)
                    try:
                        if dic["house"] == val.get("house"):
                            plants_lst.append(val.get("full_name"))
                            plants_degree.append(round(val.get("local_degree"),2))
                            dic["planet"] = plants_lst
                            dic["degree"] = plants_degree
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

        # print(sun_response, moon_response, rising_response)
        if sun_response.status_code == 200 and moon_response.status_code == 200 and rising_response.status_code == 200:
            sun_response_json = sun_response.json()
            moon_response_json = moon_response.json()
            rising_response_json = rising_response.json()
            
            sun_response_res = sun_response_json.get("response", [])
            moon_response_res = moon_response_json.get("response", [])
            rising_response_res = rising_response_json.get("response", [])
            
            # print(sun_response_res, moon_response_res, rising_response_res, "++++++")

            return ["Signs =>",{
                "sun_sign": sun_response_res.get("sun_sign"),
                "moon_sign": moon_response_res.get("moon_sign"),
                "rising_sign": rising_response_res.get("ascendant")
            }]
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

        # print(response)
        if response.status_code == 200:
            response_json = response.json()

            response_res = response_json.get("response", [])
            # print(response_res, "++++++")

            return ["Kundli signs =>",{
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
            }]
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


def convert_24_to_12_hour(time_str):
  hour = int(time_str[:2])
  minute = time_str[3:]
  period = "AM"

  if hour >= 12:
    if hour > 12:
      hour -= 12
    period = "PM"

  return f"{hour}:{minute} {period}"

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

            return ["Panchang details =>",{"day":response_res["day"]["name"],
                    "tithi":response_res["tithi"]["name"],
                    "nakshatra":response_res["nakshatra"]["name"],
                    "karana":response_res["karana"]["name"],
                    "yoga":response_res["yoga"]["name"],
                    "rasi":response_res["rasi"]["name"],
                    "sun_position":response_res["sun_position"]["zodiac"],
                    "moon_position":round(response_res["moon_position"]["moon_degree"],2),
                    "rahukaal":response_res["rahukaal"],
                    "gulika":response_res["gulika"],
                    "yamakanta":response_res["yamakanta"],
                    "gulika":response_res["gulika"]}]
        
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

            # print(response_rise_res, "++++++")
            # print(response_set_res, "++++++")

            # print(response_rise_res["bot_response"], "response_rise_res['bot_response'] moon rise")
            # print(response_set_res["bot_response"], "response_set_res['bot_response'] moon set")
            return {"Moon rise/set =>",response_rise_res["bot_response"],response_set_res["bot_response"]}
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


# Calculate the filtered mahadasha list
def calculate_mahadasha_differences(mahadasha, mahadasha_order, start_year):
    filter_mahadasha = []
    previous_date = str(start_year)  # Start year as the initial date

    for i in range(len(mahadasha)):
        # Current mahadasha and end date
        end_date = mahadasha_order[i] if i < len(mahadasha_order) else None
        filter_mahadasha.append(f"{mahadasha[i]} {previous_date} to {end_date}")
        previous_date = end_date  # Update the previous date to the current end date

    return filter_mahadasha


def get_mahadasha(year, month, day, hour, minute, birth_place_pin):
    lat,lon = get_lat_long(birth_place_pin)
    api_entity = "dashas/maha-dasha"
    tz = 5.5
    lang = "en"

    try:
        response = requests.get(f"{VEDIC_BASE_API}/{api_entity}?dob={day}/{month}/{year}&tob={hour}:{minute}&lat={lat}&lon={lon}&tz={tz}&api_key={API_KEY}&lang={lang}")

        # print(response)
        if response.status_code == 200:
            response_json = response.json()

            # print(response_json)
            response_res = response_json.get("response", [])
            print(response_res, "++++++")

            result = calculate_mahadasha_differences(response_res["mahadasha"], response_res["mahadasha_order"], response_res["start_year"])
            
            return {"mahadasha":result, "current_date_is":datetime.now().date()}
        else:
            print(f"Failed to fetch horoscope data. Status code: {response.status_code}")
            return {}
    except requests.exceptions.RequestException as e:
        print(f"Error while making API call: {e}")
        return {}


def compare_date(start_date, end_date):
    try:
        start_date_obj = datetime.strptime(start_date, "%a %b %d %Y")
        end_date_obj = datetime.strptime(end_date, "%a %b %d %Y")
        
        current_date = datetime.now()
        
        if start_date_obj < current_date and end_date_obj > current_date:
            return True
        else:
            False
    except:
        False


# Function to calculate filtered antardasha list
def calculate_antardasha(antardashas, antardasha_order):
    filter_antardasha = []

    # Iterate over each set of antardashas and their corresponding orders
    for i in range(len(antardashas)):
        current_antardasha = antardashas[i]
        current_order = antardasha_order[i]
        previous_date = None

        for j in range(len(current_antardasha)):
            # Current antardasha and start/end dates
            start_date = current_order[j] if j < len(current_order) else None
            end_date = current_order[j + 1] if j + 1 < len(current_order) else None

            # Append to the result list
            if compare_date(start_date, end_date):
                filter_antardasha.append({"antardasha":f"{current_antardasha[j]} {start_date} to {end_date}"})
                previous_date = end_date

    return filter_antardasha


def get_antardasha(year, month, day, hour, minute, birth_place_pin):
    lat,lon = get_lat_long(birth_place_pin)
    api_entity = "dashas/antar-dasha"
    tz = 5.5
    lang = "en"

    try:
        response = requests.get(f"{VEDIC_BASE_API}/{api_entity}?dob={day}/{month}/{year}&tob={hour}:{minute}&lat={lat}&lon={lon}&tz={tz}&api_key={API_KEY}&lang={lang}")

        print(response)
        if response.status_code == 200:
            response_json = response.json()

            # print(response_json)
            response_res = response_json.get("response", [])
            # print(response_res, "++++++")

            antardasha = response_res["antardashas"]
            antardasha_order = response_res["antardasha_order"]
            
            result = calculate_antardasha(antardasha, antardasha_order)
            
            return result
        else:
            print(f"Failed to fetch horoscope data. Status code: {response.status_code}")
            return {}
    except requests.exceptions.RequestException as e:
        print(f"Error while making API call: {e}")
        return {}

# Char-Dasha-Current
def calculate_chardasha_differences(response):
    # Parse dates
    sub_dasha_start_date = datetime.strptime(response["sub_dasha_start_date"], "%a %b %d %Y")
    sub_dasha_end_dates = [
        datetime.strptime(date.split(" GMT")[0], "%a %b %d %Y %H:%M:%S")
        for date in response["sub_dasha_end_dates"]
    ]

    # Get current date dynamically
    current_date = datetime.now()

    # Find the current sub-dasha
    current_chardasha = None
    for i, end_date in enumerate(sub_dasha_end_dates):
        # The first sub-dasha starts at sub_dasha_start_date
        start_date = sub_dasha_start_date if i == 0 else sub_dasha_end_dates[i - 1]
        if start_date <= current_date <= end_date:
            current_chardasha = response["sub_dasha_list"][i]
            break

    # Output result
    if current_chardasha:
        return f"Current Chardasha on {current_date.strftime('%a %b %d %Y')}: {current_chardasha}"
    else:
        print("No active Chardasha found.")
        return "No active Chardasha found."


def get_chardasha(year, month, day, hour, minute, birth_place_pin):
    lat,lon = get_lat_long(birth_place_pin)
    api_entity = "dashas/char-dasha-current"
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

            result = calculate_chardasha_differences(response_res)
        
            return result
        else:
            print(f"Failed to fetch horoscope data. Status code: {response.status_code}")
            return {}
    except requests.exceptions.RequestException as e:
        print(f"Error while making API call: {e}")
        return {}



# Char-Dasha-Main
def calculate_chardasha_main_differences(response):
    start_date = datetime.strptime(response["start_date"], "%a %b %d %Y %H:%M:%S GMT+0000 (Coordinated Universal Time)")
    dasha_end_dates = [datetime.strptime(date, "%a %b %d %Y %H:%M:%S GMT+0000 (Coordinated Universal Time)") for date in response["dasha_end_dates"]]

    # Get current date dynamically
    current_date = datetime.now()

    # Find the current dasha
    current_dasha = None
    for i, end_date in enumerate(dasha_end_dates):
        # The first dasha starts from the provided start date
        start_dasha_date = start_date if i == 0 else dasha_end_dates[i - 1]
        
        if start_dasha_date <= current_date <= end_date:
            current_dasha = response["dasha_list"][i]
            break

    # Output result
    if current_dasha:
        print(f"Current char-dasha-main on {current_date.strftime('%a %b %d %Y')}: {current_dasha}")
        return f"Current char-dasha-main on {current_date.strftime('%a %b %d %Y')}: {current_dasha}"
    else:
        print("No active Dasha found.")
        return "No active Dasha found."


def get_chardasha_main(year, month, day, hour, minute, birth_place_pin):
    lat,lon = get_lat_long(birth_place_pin)
    api_entity = "dashas/char-dasha-main"
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

            result = calculate_chardasha_main_differences(response_res)
        
            return result
        else:
            print(f"Failed to fetch horoscope data. Status code: {response.status_code}")
            return {}
    except requests.exceptions.RequestException as e:
        print(f"Error while making API call: {e}")
        return {}



# Get Yogini Dasha
def calculate_yogini_differences(response, current_date):
    for i, end_date_str in enumerate(response["dasha_end_dates"]):
        # Convert end date from string to datetime
        end_date = datetime.strptime(end_date_str.split(" GMT")[0], "%a %b %d %Y %H:%M:%S")
        
        # Check if current date is less than or equal to the end date
        if current_date <= end_date:
            dasha_name = response["dasha_list"][i]
            dasha_lord = response["dasha_lord_list"][i]
            end_date_formatted = end_date.strftime("%a %b %d %Y")
            return {
                "current_dasha": dasha_name,
                "lord": dasha_lord,
                "end_date": end_date_formatted
            }
    return None



def get_yogini(year, month, day, hour, minute, birth_place_pin):
    lat,lon = get_lat_long(birth_place_pin)
    api_entity = "dashas/yogini-dasha-main"
    tz = 5.5
    lang = "en"

    try:
        response = requests.get(f"{VEDIC_BASE_API}/{api_entity}?dob={day}/{month}/{year}&tob={hour}:{minute}&lat={lat}&lon={lon}&tz={tz}&api_key={API_KEY}&lang={lang}")

        print(response)
        if response.status_code == 200:
            response_json = response.json()

            # print(response_json)
            response_res = response_json.get("response", [])
            # print(response_res, "++++++")

            current_date = datetime.now()

            result = calculate_yogini_differences(response_res, current_date)
            
            return result
        else:
            print(f"Failed to fetch horoscope data. Status code: {response.status_code}")
            return {}
    except requests.exceptions.RequestException as e:
        print(f"Error while making API call: {e}")
        return {}


# Get Sade-Sati-details
def get_sade_sati(year, month, day, hour, minute, birth_place_pin):
    lat,lon = get_lat_long(birth_place_pin)
    api_entity = "extended-horoscope/current-sade-sati"
    tz = 5.5
    lang = "en"

    try:
        response = requests.get(f"{VEDIC_BASE_API}/{api_entity}?dob={day}/{month}/{year}&tob={hour}:{minute}&lat={lat}&lon={lon}&tz={tz}&api_key={API_KEY}&lang={lang}")

        print(response)
        if response.status_code == 200:
            response_json = response.json()

            # print(response_json)
            response_res = response_json.get("response", [])
            # print(response_res, "++++++")

            date_considered = response_res["date_considered"]
            is_in_sade_sati = response_res["shani_period_type"]
            retrograde = response_res["saturn_retrograde"]
            bot_response = response_res["bot_response"]
            age = response_res["age"]
            

            return {"date_considered":date_considered,"retrograde":retrograde,"age":age, "is_in_sade_sati":is_in_sade_sati, "answer":bot_response}
        else:
            print(f"Failed to fetch horoscope data. Status code: {response.status_code}")
            return {}
    except requests.exceptions.RequestException as e:
        print(f"Error while making API call: {e}")
        return {}


# Get Friend and enemy planets
def get_friend_planets(year, month, day, hour, minute, birth_place_pin):
    lat,lon = get_lat_long(birth_place_pin)
    api_entity = "extended-horoscope/friendship"
    tz = 5.5
    lang = "en"

    try:
        response = requests.get(f"{VEDIC_BASE_API}/{api_entity}?dob={day}/{month}/{year}&tob={hour}:{minute}&lat={lat}&lon={lon}&tz={tz}&api_key={API_KEY}&lang={lang}")

        print(response)
        if response.status_code == 200:
            response_json = response.json()

            # print(response_json)
            response_res = response_json.get("response", [])
            # print(response_res, "++++++")

            friends_planets = response_res["permanent_table"]

            return {"friends_planets":friends_planets}
        else:
            print(f"Failed to fetch horoscope data. Status code: {response.status_code}")
            return {}
    except requests.exceptions.RequestException as e:
        print(f"Error while making API call: {e}")
        return {}


# Get Numero-Table like-> Favorite god,color, stone, mantra, day
def get_numero_table(year, month, day, hour, minute, birth_place_pin):
    lat,lon = get_lat_long(birth_place_pin)
    api_entity = "extended-horoscope/numero-table"
    tz = 5.5
    lang = "en"

    try:
        response = requests.get(f"{VEDIC_BASE_API}/{api_entity}?name=-&dob={day}/{month}/{year}&tob={hour}:{minute}&lat={lat}&lon={lon}&tz={tz}&api_key={API_KEY}&lang={lang}")

        print(response)
        if response.status_code == 200:
            response_json = response.json()

            # print(response_json)
            response_res = response_json.get("response", [])
            # print(response_res, "++++++")

            radical_number = response_res["radical_number"]
            radical_ruler = response_res["radical_ruler"]
            characteristics = response_res["characteristics"]
            fav_color = response_res["fav_color"]
            fav_day = response_res["fav_day"]
            fav_god = response_res["fav_god"]
            fav_mantra = response_res["fav_mantra"]
            fav_metal = response_res["fav_metal"]
            fav_stone = response_res["fav_stone"]
            fav_substone = response_res["fav_substone"]

            return {"radical_number":radical_number, "radical_ruler":radical_ruler, "characteristics":characteristics, "favorite_color":fav_color,"favorite_day":fav_day, "favorite_god":fav_god, "favorite_mantra":fav_mantra, "favorite_metal":fav_metal, "favorite_stone":fav_stone, "favorite_substone":fav_substone}
        else:
            print(f"Failed to fetch horoscope data. Status code: {response.status_code}")
            return {}
    except requests.exceptions.RequestException as e:
        print(f"Error while making API call: {e}")
        return {}


# Get Varshapal-Details like -> muntha sign, din-rathi, tri-rathi, ayanamsa
def get_varshapal_details(year, month, day, hour, minute, birth_place_pin):
    lat,lon = get_lat_long(birth_place_pin)
    api_entity = "extended-horoscope/varshapal-details"
    tz = 5.5
    lang = "en"

    try:
        response = requests.get(f"{VEDIC_BASE_API}/{api_entity}?dob={day}/{month}/{year}&tob={hour}:{minute}&lat={lat}&lon={lon}&tz={tz}&api_key={API_KEY}&lang={lang}")

        print(response)
        if response.status_code == 200:
            response_json = response.json()

            # print(response_json)
            response_res = response_json.get("response", [])
            # print(response_res, "++++++")

            muntha_sign = response_res["muntha_sign"]
            muntha_lord = response_res["muntha_lord"]
            varshpal_date = response_res["varshpal_date"]
            varsha_lagna = response_res["varsha_lagna"]
            varsha_lagna_lord = response_res["varsha_lagna_lord"]
            dinratri_lord = response_res["dinratri_lord"]
            trirashi_lord = response_res["trirashi_lord"]
            current_ayanamsa = response_res["current_ayanamsa"]


            return {"muntha_sign":muntha_sign,"muntha_lord":muntha_lord,"varshpal_date":varshpal_date,"varsha_lagna":varsha_lagna,"varsha_lagna_lord":varsha_lagna_lord,"dinratri_lord":dinratri_lord,"trirashi_lord":trirashi_lord,"current_ayanamsa":current_ayanamsa}
        else:
            print(f"Failed to fetch horoscope data. Status code: {response.status_code}")
            return {}
    except requests.exceptions.RequestException as e:
        print(f"Error while making API call: {e}")
        return {}



# Get Ascendant/langna/Rising report
def get_ascendant_report(year, month, day, hour, minute, birth_place_pin):
    lat,lon = get_lat_long(birth_place_pin)
    api_entity = "horoscope/ascendant-report"
    tz = 5.5
    lang = "en"

    try:
        response = requests.get(f"{VEDIC_BASE_API}/{api_entity}?dob={day}/{month}/{year}&tob={hour}:{minute}&lat={lat}&lon={lon}&tz={tz}&api_key={API_KEY}&lang={lang}")

        print(response)
        if response.status_code == 200:
            response_json = response.json()

            # print(response_json)
            response_res = response_json.get("response", [])[0]
            print(response_res, "++++++")

            ascendant = response_res["ascendant"]
            ascendant_lord = response_res["ascendant_lord"]
            ascendant_lord_location = response_res["ascendant_lord_location"]
            ascendant_lord_house_location = response_res["ascendant_lord_house_location"]
            verbal_location = response_res["verbal_location"]
            ascendant_lord_strength = response_res["ascendant_lord_strength"]
            zodiac_characteristics = response_res["zodiac_characteristics"]
            lucky_gem = response_res["lucky_gem"]
            day_for_fasting = response_res["day_for_fasting"]
            gayatri_mantra = response_res["gayatri_mantra"]


            return {"ascendant":ascendant, "ascendant_lord":ascendant_lord, "ascendant_lord_location":ascendant_lord_location, "ascendant_lord_house_location":ascendant_lord_house_location, "verbal_location":verbal_location, "ascendant_lord_strength":ascendant_lord_strength, "zodiac_characteristics":zodiac_characteristics,"lucky_gem":lucky_gem,"day_for_fasting":day_for_fasting,"gayatri_mantra":gayatri_mantra}
        else:
            print(f"Failed to fetch horoscope data. Status code: {response.status_code}")
            return {}
        
    except requests.exceptions.RequestException as e:
        print(f"Error while making API call: {e}")
        return {}


# Get planets Report
def get_planets_report(year, month, day, hour, minute, birth_place_pin, planet):
    lat,lon = get_lat_long(birth_place_pin)
    api_entity = "horoscope/planet-report"
    tz = 5.5
    lang = "en"

    try:
        response = requests.get(f"{VEDIC_BASE_API}/{api_entity}?dob={day}/{month}/{year}&tob={hour}:{minute}&lat={lat}&lon={lon}&tz={tz}&api_key={API_KEY}&planet={planet}&lang={lang}")

        print(response)
        if response.status_code == 200:
            response_json = response.json()

            # print(response_json)
            response_res = response_json.get("response", [])[0]
            # print(response_res, "++++++")

            planet_considered = response_res["planet_considered"]
            planet_location = response_res["planet_location"]
            planet_native_location = response_res["planet_native_location"]
            planet_zodiac = response_res["planet_zodiac"]
            zodiac_lord = response_res["zodiac_lord"]
            zodiac_lord_location = response_res["zodiac_lord_location"]
            zodiac_lord_house_location = response_res["zodiac_lord_house_location"]
            zodiac_lord_strength = response_res["zodiac_lord_strength"]
            gayatri_mantra = response_res["gayatri_mantra"]
            qualities_short = response_res["qualities_short"]


            return {"planet_considered":planet_considered, "planet_location":planet_location, "planet_native_location":planet_native_location, "planet_zodiac":planet_zodiac, "zodiac_lord":zodiac_lord, "zodiac_lord_location":zodiac_lord_location, "zodiac_lord_house_location":zodiac_lord_house_location,"zodiac_lord_strength":zodiac_lord_strength,"qualities_short":qualities_short,"gayatri_mantra":gayatri_mantra}
        else:
            print(f"Failed to fetch horoscope data. Status code: {response.status_code}")
            return {}
        
    except requests.exceptions.RequestException as e:
        print(f"Error while making API call: {e}")
        return {}



# Get Personal-Characteristics
# def get_per_charcterstics(year, month, day, hour, minute, birth_place_pin):
#     lat,lon = get_lat_long(birth_place_pin)
#     api_entity = "horoscope/personal-characteristics"
#     tz = 5.5
#     lang = "en"

#     try:
#         response = requests.get(f"{VEDIC_BASE_API}/{api_entity}?dob={day}/{month}/{year}&tob={hour}:{minute}&lat={lat}&lon={lon}&tz={tz}&api_key={API_KEY}&lang={lang}")

#         print(response)
#         if response.status_code == 200:
#             response_json = response.json()

#             # print(response_json)
#             response_res = response_json.get("response", [])
#             # print(response_res, "++++++")
#             filer_result = ["personal Charaterstics =>"]
#             for rec in response_res:
#                 filter_dict = {}
#                 filter_dict["current_house"] =  rec["current_house"]
#                 filter_dict["verbal_location"] =  rec["verbal_location"]
#                 filter_dict["current_zodiac"] =  rec["current_zodiac"]
#                 filter_dict["lord_of_zodiac"] =  rec["lord_of_zodiac"]
#                 filter_dict["lord_zodiac_location"] =  rec["lord_zodiac_location"]
#                 filter_dict["lord_house_location"] =  rec["lord_house_location"]
#                 filter_dict["lord_strength"] =  rec["lord_strength"]
#                 filer_result.append(filter_dict)
#             return filer_result
#         else:
#             print(f"Failed to fetch horoscope data. Status code: {response.status_code}")
#             return {}
        
#     except requests.exceptions.RequestException as e:
#         print(f"Error while making API call: {e}")
#         return {}



# Get Choghadiya Muhurta
def get_current_chog_muhurat(response):
    current_time = datetime.now()
    print(current_time)
    for muhurat_list in [response.get('day'), response.get('night')]:
        if muhurat_list:
            for muhurat in muhurat_list:
                start_time = datetime.strptime(muhurat['start'], "%a %b %d %Y %I:%M:%S %p")
                end_time = datetime.strptime(muhurat['end'], "%a %b %d %Y %I:%M:%S %p")

                if start_time <= current_time <= end_time:
                    return {"muhurat":muhurat['muhurat'], "start_time":muhurat['start'], "end_time":muhurat['end'], "type":muhurat["type"]}

    return None


def get_chog_muhurta():
    current_date, current_time = get_current_date_time()
    coordinates = get_current_location()
    tz = 5.5
    lang = "en"
    api_rise_entity = "panchang/choghadiya-muhurta"

    try:
        response = requests.get(f"{VEDIC_BASE_API}/{api_rise_entity}?api_key={API_KEY}&date={current_date}&tz={tz}&lat={coordinates[0]}&lon={coordinates[1]}&time={current_time}&lang={lang}")

        # print(response)
        if response.status_code == 200:

            response_json = response.json()
            response_res = response_json.get("response", [])

            # print(response_res, "++++++")
            curr_time_in_12_form = convert_24_to_12_hour(current_time)
            current_mahurat = get_current_chog_muhurat(response_res)
            return {f"Choghadiya Muhurta => current time is {curr_time_in_12_form} ":current_mahurat}
        else:
            print(f"Failed to fetch horoscope data. Status code: {response_res.status_code}")
            return {}
    except requests.exceptions.RequestException as e:
        print(f"Error while making API call: {e}")
        return {}



# Get Hora-Mahurata
def get_current_hora_muhurat(response):
    current_time = datetime.now()
    for hora in response['horas']:
        start_time = datetime.strptime(hora['start'], "%a %b %d %Y %I:%M:%S %p")
        end_time = datetime.strptime(hora['end'], "%a %b %d %Y %I:%M:%S %p")

        if start_time <= current_time <= end_time:
            return hora

    return None


def get_hora_muhurta():
    current_date, current_time = get_current_date_time()
    coordinates = get_current_location()
    tz = 5.5
    lang = "en"
    api_rise_entity = "panchang/hora-muhurta"

    try:
        response = requests.get(f"{VEDIC_BASE_API}/{api_rise_entity}?api_key={API_KEY}&date={current_date}&tz={tz}&lat={coordinates[0]}&lon={coordinates[1]}&time={current_time}&lang={lang}")

        # print(response)
        if response.status_code == 200:

            response_json = response.json()
            response_res = response_json.get("response", [])

            # print(response_res, "++++++")
            curr_time_in_12_form = convert_24_to_12_hour(current_time)
            current_mahurat = get_current_hora_muhurat(response_res)
            return {f"Hora Muhurta => current time is {curr_time_in_12_form} ":current_mahurat}
        else:
            print(f"Failed to fetch horoscope data. Status code: {response_res.status_code}")
            return {}
    except requests.exceptions.RequestException as e:
        print(f"Error while making API call: {e}")
        return {}


# Get Moon Phase
def get_moon_phase():
    current_date, current_time = get_current_date_time()
    tz = 5.5
    lang = "en"
    api_rise_entity = "panchang/moon-phase"

    try:
        response = requests.get(f"{VEDIC_BASE_API}/{api_rise_entity}?api_key={API_KEY}&date={current_date}&tz={tz}&lang={lang}")

        # print(response)
        if response.status_code == 200:

            response_json = response.json()
            response_res = response_json.get("response", [])

            # print(response_res, "response_res")
            
            bot_response = response_res["bot_response"]
            luminance = response_res["luminance"]
            phase = response_res["phase"]
            paksha = response_res["paksha"]
            state = response_res["state"]
            date = response_res["date"]
            
            return {"Moon Phase =>": phase, "response": bot_response, "luminance":luminance, "paksha":paksha, "state":state, "date":date}
        else:
            print(f"Failed to fetch horoscope data. Status code: {response_res.status_code}")
            return {}
    except requests.exceptions.RequestException as e:
        print(f"Error while making API call: {e}")
        return {}



# Get Solar/Sun noon
def get_solar_noon():
    current_date, current_time = get_current_date_time()
    coordinates = get_current_location()
    tz = 5.5
    lang = "en"
    api_rise_entity = "panchang/solarnoon"

    try:
        response = requests.get(f"{VEDIC_BASE_API}/{api_rise_entity}?api_key={API_KEY}&date={current_date}&tz={tz}&lat={coordinates[0]}&lon={coordinates[1]}&time={current_time}&lang={lang}")

        # print(response)
        if response.status_code == 200:

            response_json = response.json()
            response_res = response_json.get("response", [])

            # print(response_res, "response_res")    
            sun_noon = response_res["sun_noon"]
            bot_response = response_res["bot_response"]
            
            return {"Sun noon =>": sun_noon, "bot_response":bot_response}
        else:
            print(f"Failed to fetch horoscope data. Status code: {response_res.status_code}")
            return {}
    except requests.exceptions.RequestException as e:
        print(f"Error while making API call: {e}")
        return {}


# Get Retrogrades each-planet
def get_retrogrades(planet="Sun"):
    planet = planet
    lang = "en"
    api_rise_entity = "panchang/retrogrades"

    try:
        response = requests.get(f"{VEDIC_BASE_API}/{api_rise_entity}?api_key={API_KEY}&year={datetime.now().date().year}&planet={planet}&lang={lang}")

        print(response)
        if response.status_code == 200:

            response_json = response.json()
            response_res = response_json.get("response", [])

            print(response_res, "response_res")
            
            bot_response = response_res["bot_response"]
            dates = response_res["dates"]
            
            return {"retrogrades for {planet} =>":bot_response,  "dates": dates}
        else:
            print(f"Failed to fetch horoscope data. Status code: {response_res.status_code}")
            return {}
    except requests.exceptions.RequestException as e:
        print(f"Error while making API call: {e}")
        return {}


# Get BioRhythm
def get_bio_rthythm(year, month, day):
    lang = "en"
    api_rise_entity = "prediction/biorhythm"

    try:
        response = requests.get(f"{VEDIC_BASE_API}/{api_rise_entity}?dob={day}/{month}/{year}&api_key={API_KEY}&lang={lang}")

        print(response)
        if response.status_code == 200:

            response_json = response.json()
            response_res = response_json.get("response", [])

            print(response_res, "response_res")

            
            return {"BioRhythm =>": response_res}
        else:
            print(f"Failed to fetch horoscope data. Status code: {response_res.status_code}")
            return {}
    except requests.exceptions.RequestException as e:
        print(f"Error while making API call: {e}")
        return {}



# Gem details
def get_gem_details(gem):
    gem = gem
    lang = "en"
    api_rise_entity = "utilities/gem-details"

    try:
        response = requests.get(f"{VEDIC_BASE_API}/{api_rise_entity}?gem={gem}&lang={lang}&api_key={API_KEY}")

        # print(response)
        if response.status_code == 200:

            response_json = response.json()
            response_res = response_json.get("response", [])

            # print(response_res, "response_res")
            
            name = response_res["response"]["name"]
            gem = response_res["response"]["gem"]
            planet = response_res["response"]["planet"]
            good_results = response_res["response"]["good_results"]
            diseases_cure = response_res["response"]["diseases_cure"]
            finger = response_res["response"]["finger"]
            metal = response_res["response"]["metal"]
            
            return {"gem details =>":name,  "gem": gem, "planet":planet, "good_results":good_results, "diseases_cure":diseases_cure, "finger":finger, "metal":metal}
        else:
            print(f"Failed to fetch horoscope data. Status code: {response_res.status_code}")
            return {}
    except requests.exceptions.RequestException as e:
        print(f"Error while making API call: {e}")
        return {}


# Get Nakshatra Vastu Details
def get_nakshatra_vastu(nakshatra_no):
    nakshatra_no = nakshatra_no
    lang = "en"
    api_rise_entity = "utilities/nakshatra-vastu-details"

    try:
        response = requests.get(f"{VEDIC_BASE_API}/{api_rise_entity}?nakshatra={nakshatra_no}&lang={lang}&api_key={API_KEY}")

        # print(response)
        if response.status_code == 200:

            response_json = response.json()
            response_res = response_json.get("response", [])

            # print(response_res, "response_res")
            
            Nakshatra = response_res["Nakshatra"]
            Lord = response_res["Lord"]
            Favorable_Direction = response_res["Favorable_Direction"]
            Avoidance = response_res["Avoidance"]
            Weight = response_res["Weight"]
            Entrance_to_Avoid = response_res["Entrance_to_Avoid"]
            Sentence = response_res["Sentence"]
            Room_Locations = response_res["Room_Locations"]
            
            return {"Nakshatra details =>":Nakshatra,  "Lord": Lord, "Favorable_Direction":Favorable_Direction, "Avoidance":Avoidance, "Weight":Weight, "Entrance_to_Avoid":Entrance_to_Avoid, "Sentence":Sentence, "Room_Locations":Room_Locations}
        else:
            print(f"Failed to fetch horoscope data. Status code: {response_res.status_code}")
            return {}
    except requests.exceptions.RequestException as e:
        print(f"Error while making API call: {e}")
        return {}


# Get Day Number
def get_day_no(year, month, day):
    lang = "en"
    api_rise_entity = "prediction/day-number"

    try:
        response = requests.get(f"{VEDIC_BASE_API}/{api_rise_entity}?dob={day}/{month}/{year}&api_key={API_KEY}&lang={lang}")

        # print(response)
        if response.status_code == 200:

            response_json = response.json()
            response_res = response_json.get("response", [])

            # print(response_res, "response_res")
            
            return {"day number =>": response_res}
        else:
            print(f"Failed to fetch horoscope data. Status code: {response_res.status_code}")
            return {}
    except requests.exceptions.RequestException as e:
        print(f"Error while making API call: {e}")
        return {}
    

# Get Numerology details
def get_numerology(year, month, day):
    lang = "en"
    name = "human"
    api_rise_entity = "prediction/numerology"

    try:
        response = requests.get(f"{VEDIC_BASE_API}/{api_rise_entity}?name={name}&date={day}/{month}/{year}&api_key={API_KEY}&lang={lang}")

        # print(response)
        if response.status_code == 200:

            response_json = response.json()
            response_res = response_json.get("response", [])

            # print(response_res, "response_res")
            destiny = response_res["destiny"]["meaning"]
            destiny_no = response_res["destiny"]["number"]
            personality = response_res["personality"]["meaning"]
            personality_no = response_res["personality"]["number"]
            attitude = response_res["attitude"]["meaning"]
            attitude_no = response_res["attitude"]["number"]
            character = response_res["character"]["meaning"]
            character_no = response_res["character"]["number"]
            soul = response_res["soul"]["meaning"]
            soul_no = response_res["soul"]["number"]
            agenda = response_res["agenda"]["meaning"]
            agenda_no = response_res["agenda"]["number"]
            purpose = response_res["purpose"]["meaning"]
            purpose_no = response_res["purpose"]["number"]
            
            return {"Numerology => , destiny":destiny, "destiny_no":destiny_no ,"personality":personality,"personality_no":personality_no, "attitude":attitude, "attitude_no":attitude_no, "character":character, "character_no":character_no,"soul":soul, "soul_no":soul_no ,"agenda":agenda, "agenda_no":agenda_no,"purpose":purpose, "purpose_no":purpose_no}
        else:
            print(f"Failed to fetch horoscope data. Status code: {response_res.status_code}")
            return {}
    except requests.exceptions.RequestException as e:
        print(f"Error while making API call: {e}")
        return {}

    

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
    global questions, df, userLanguage
    
    detect_lang_user = detect_hinglish(question)

    # detect_lang_user = detect(question)
    print(detect_lang_user, "detect_lang_user ++")
    
    if detect_lang_user == "hi":
        translated_text = Translator.translate_text(question, from_language='auto', to_language='en', translator='google')
        # translated_text = GoogleTranslator(source='auto', target='en').translate(question)
        print(translated_text, "convert question ++")
        userLanguage = "hi"
        text = cnvrtLowerCase(removeHtmlTag(removeUrls(removePunctuation(removeQuatation(translated_text)))))
        print(text, "text")
    elif detect_lang_user == "Hinglish":
        # translated_text = Translator.translate_text(question, from_language='auto', to_language='hi', translator='google')
        print(question, "question language text...")
        # text = GoogleTranslator(source='auto', target='en').translate(question)
        text = Translator.translate_text(question, from_language='auto', to_language='en', translator='google')
        print(text, "convert question hinglish to english ++")
        translated_text = cnvrtLowerCase(removeHtmlTag(removeUrls(removePunctuation(removeQuatation(question)))))
        userLanguage = "Hinglish"
        text = cnvrtLowerCase(removeHtmlTag(removeUrls(removePunctuation(removeQuatation(text)))))
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
        if similarities[1] > .90:
            print(df["Answer"][similarities[0]])
            if userLanguage == "hi":
                translated_text = Translator.translate_text(df["Answer"][similarities[0]],from_language='auto', to_language='hi', translator='google')
                # translated_text = GoogleTranslator(source='auto', target='hi').translate(df["Answer"][similarities[0]])
                return {"answer":translated_text}
            elif userLanguage == "Hinglish":
                translated_text = Translator.translate_text(df["Answer"][similarities[0]],from_language='auto', to_language='hi', translator='google')
                # translated_text = GoogleTranslator(source='auto', target='hi').translate(df["Answer"][similarities[0]])
                roman_text = hindi_to_roman(translated_text)
                return {"answer":roman_text}
            else:
                return {"answer":df["Answer"][similarities[0]]}
        else:
            print("llama model running......")

            def generate_question(translated_text, entity=None , age=None):
                """Generate the appropriate question based on age."""
                print(entity, "entity in generate_question")
                
                vedic_astrological_signs = radical_no = horoscope_data = lagna_lord = birth_chart = nakshatra = tithi_yoga = kundli_signs = moon_rising_set = sun_rising_set = mangal_dosh = kaalsarp_dosh = manglik_dosh = pitra_dosh = mahadasha = antardasha = chardasha = chardasha_main = yogini = sade_sati = friend_planets = numero_table = varshapal_details = ascendant_report = planet_report = chog_muhurta = hora_muhurta = moon_phase = solar_noon = retrogrades = biorhythm = day_no = numerology = gem_details = nakshatra_vastu = ""
                
                
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
                if "antardasha" in entity:
                    antardasha = get_antardasha(item.year,item.month,item.day,item.hour,item.minute,item.birth_place_pin)
                if "chardasha" in entity:
                    chardasha = get_chardasha(item.year,item.month,item.day,item.hour,item.minute,item.birth_place_pin)
                if "chardasha_main" in entity:
                    chardasha_main = get_chardasha_main(item.year,item.month,item.day,item.hour,item.minute,item.birth_place_pin)
                if "yogini" in entity:
                    yogini = get_yogini(item.year,item.month,item.day,item.hour,item.minute,item.birth_place_pin)
                if "sade_sati" in entity:
                    sade_sati = get_sade_sati(item.year,item.month,item.day,item.hour,item.minute,item.birth_place_pin)
                if "friend_planets" in entity:
                    friend_planets = get_friend_planets(item.year,item.month,item.day,item.hour,item.minute,item.birth_place_pin)
                if "numero_table" in entity:
                    numero_table = get_numero_table(item.year,item.month,item.day,item.hour,item.minute,item.birth_place_pin)
                if "varshapal_details" in entity:
                    varshapal_details = get_varshapal_details(item.year,item.month,item.day,item.hour,item.minute,item.birth_place_pin)
                if "ascendant_report" in entity:
                    ascendant_report = get_ascendant_report(item.year,item.month,item.day,item.hour,item.minute,item.birth_place_pin)
                if "planet_report" in entity:
                    planet = get_planet_from_text(translated_text)
                    planet_report = get_planets_report(item.year,item.month,item.day,item.hour,item.minute,item.birth_place_pin, planet)
                # if "personal_characteristics" in entity:
                #     per_charcterstics = get_per_charcterstics(item.year,item.month,item.day,item.hour,item.minute,item.birth_place_pin)
                if "chog_muhurta" in entity:
                    chog_muhurta = get_chog_muhurta()
                if "hora_muhurta" in entity:
                    hora_muhurta = get_hora_muhurta()
                if "moon_phase" in entity:
                    moon_phase = get_moon_phase()
                if "solar_noon" in entity:
                    solar_noon = get_solar_noon()
                if "retrogrades" in entity:
                    planet = get_planet_from_text(translated_text)
                    retrogrades = get_retrogrades(planet)
                if "biorhythm" in entity:
                    biorhythm = get_bio_rthythm(item.year,item.month,item.day)
                if "day_no" in entity:
                    day_no = get_day_no(item.year,item.month,item.day)
                if "numerology" in entity:
                    numerology = get_numerology(item.year,item.month,item.day)
                if "gem_details" in entity:
                    gem = get_gem_from_text(translated_text)
                    gem_details = get_gem_details(gem)
                if "nakshatra_vastu" in entity:
                    nakshatra_vastu_no = get_nakshatra_vastu_no(translated_text)
                    nakshatra_vastu = get_nakshatra_vastu(nakshatra_vastu_no)


                if vedic_astrological_signs or radical_no or horoscope_data or tithi_yoga or kundli_signs or moon_rising_set or sun_rising_set or mangal_dosh or kaalsarp_dosh or manglik_dosh or pitra_dosh or mahadasha or antardasha or chardasha or chardasha_main or yogini or sade_sati or friend_planets or numero_table or varshapal_details or ascendant_report or planet_report or chog_muhurta or hora_muhurta or moon_phase or solar_noon or retrogrades or biorhythm or day_no or numerology or gem_details or nakshatra_vastu:
                    if userLanguage == "Hinglish":
                        base_question = (
                        f"Only act as an astrologer and do not reply to questions other than astrology. Give answer in hinglish language. "
                        f"this is my details {vedic_astrological_signs,radical_no,horoscope_data, tithi_yoga, kundli_signs,moon_rising_set, sun_rising_set, mangal_dosh, kaalsarp_dosh, manglik_dosh, pitra_dosh, mahadasha, antardasha, chardasha, chardasha_main, yogini, sade_sati, friend_planets,numero_table,varshapal_details,ascendant_report, planet_report,chog_muhurta, hora_muhurta, moon_phase, solar_noon, retrogrades, biorhythm, day_no, numerology, gem_details, nakshatra_vastu} ."
                        f"Let's say the question is '{translated_text}'. "
                    )
                    else:
                        base_question = (
                            f"Only act as an astrologer and do not reply to questions other than astrology. "
                            f"this is my details {vedic_astrological_signs,radical_no,horoscope_data, tithi_yoga, kundli_signs,moon_rising_set, sun_rising_set, mangal_dosh, kaalsarp_dosh, manglik_dosh, pitra_dosh, mahadasha, antardasha, chardasha, chardasha_main, yogini, sade_sati, friend_planets,numero_table,varshapal_details,ascendant_report, planet_report,chog_muhurta, hora_muhurta, moon_phase, solar_noon, retrogrades, biorhythm, day_no, numerology, gem_details, nakshatra_vastu} ."
                            f"Let's say the question is '{translated_text}'. "
                        )
                else:
                    if not is_greeting(translated_text):
                        print("Inn is_greeting")
                        if userLanguage == "Hinglish":
                            base_question = (
                            f"Only act as an astrologer and do not reply to questions other than astrology. Give answer in hinglish language. "
                            f"this is my details  {get_horoscope_data(item.year,item.month,item.day,item.hour,item.minute,item.birth_place_pin)} "
                            f"Let's say the question is '{translated_text}'. "
                        )
                        else:
                            base_question = (
                                f"Only act as an astrologer and do not reply to questions other than astrology. "
                                f"this is my details  {get_horoscope_data(item.year,item.month,item.day,item.hour,item.minute,item.birth_place_pin)} "
                                f"Let's say the question is '{translated_text}'. "
                            )
                    else:
                        if userLanguage == "Hinglish":
                            base_question = (
                                    f"Only act as an astrologer and do not reply to questions other than astrology. Give answer in hinglish language. "
                                    # f"this is my details  {get_horoscope_data(item.year,item.month,item.day,item.hour,item.minute,item.birth_place_pin)} "
                                    f"Let's say the question is '{translated_text}'. "
                                )
                        else:
                            base_question = (
                                    f"Only act as an astrologer and do not reply to questions other than astrology. "
                                    # f"this is my details  {get_horoscope_data(item.year,item.month,item.day,item.hour,item.minute,item.birth_place_pin)} "
                                    f"Let's say the question is '{translated_text}'. "
                                )

                if age < 15:
                    print(base_question + "Considering my age is under 15, please give an answer in 40 to 60 words only.")
                    return base_question + "Considering my age is under 15, please give an answer in 40 to 60 words only."
                elif age > 50:
                    print(base_question + "Considering my age is greater than 50, please give an answer in 40 to 60 words only.")
                    return base_question + "Considering my age is greater than 50, please give an answer in 40 to 60 words only."
                else:
                    print(base_question + "please give an answer in 40 to 60 words only.")
                    return base_question + "please give an answer in 40 to 60 words only."
                
            
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
                # Define keywords and entities
                keywords = {
                    "zodiac_sign": [
                        "zodiac sign", "zodiac_sign", "zodaic sign", "zodaic", "zodic", "zodac", "zodiac" ,"sun sign", "sun-sign", "lagna sign", "moon sign", "moon-sign","sun sin", "sunsign", "sunsin", "moonsign", "moonsin","moon sin", "astrological sign", "aries", "taurus", "gemini",
                        "cancer", "leo", "virgo", "libra", "scorpio", "sagittarius", "capricorn",
                        "aquarius", "pisces", "chandra rashi", "chandra lagna", "rising sign", "ascendant", "ascendant sign", "joint sign"
                    ],
                    "house_planets": [
                        "house_planets", "house", "houses","bhava", "planet", "planat", "planets", "planetary","graha", "sun", "moon", "mars", "mercury", "jupiter", "jupyter" ,"venus","saturn", "degree", "degre", "digri", "ketu", "leadership", "peace", "energy", "strength", "communication", "intellect", "business", "wisdom", "wealth", "children", "relationship", "beauty", "love", "creativity","hard work", "struggles", "struggle", "illusions", "desires", "spirituality", "past", "marriage", "relation-ship", "relation", "romance", "mind", "luxury", "finance"," achievement", "growth", "knowledge", "swabhav", "savbhaav"
                    ],
                    "kundli_signs":["kundli_signs", "gana", "yoni", "vasya", "nadi", "varna","paya","tatva", "life stone", "life-stone", "lucky stone", "lucky-stone", "horoscope", "kundli signs","kundli sign", "kundli-sign", "kundly", "kundle", "kundlee", "kundli","kundlie","birth chart", "birth", "signs", "natal chart", "birth_chart", "horoscope chart", "rashi", "rasi"],

                    "radical":["radical", "radicals", "life path number", "path number", "path no" ,"destiny number", "destiny no"],
                    
                    "tithi_yoga": [
                        "tithi_yoga", "yoga", "raj yoga", "raj", "dhan yoga", "gaja kesari yoga", "parivartana yoga","yoga","yog",
                        "vipareeta yoga", "laxmi yoga", "chandra mangala yoga", "karana", "yog","tithi", "tithi number", "tithi no","lunar_month", "lunar", "lunaar","vara", "varaa","rahukaal", "rahukal", "rahu","nakshatra", "naksatra", "naksatraa", "nakstra", "naksatar","karan","gulika","sun position", "moon position", "rasee","rashee", "panchang", "panchaang"
                    ],
                    
                    "moon_rising_set":["moon_rising_set", "moon rise", "moon set", "moon rice", "mon rice", "moon sets", "moon rising", "moon risings","mon rising", "moon ricing","mon rise"],
                    
                    "sun_rising_set":["sun_rising_set", "sun rise", "sun set", "sun rice", "san rice", "sun sets", "sun rising", "sun risings","san rising", "sun ricing","san rise"],
                    
                    "mangal_dosh":["mangal_dosh", "mangal dosh", "mangal dosha", "mangal dos", "mangal", "mangel", "mangel dos", "mangel dosh", "dosha" ,"dosh"],
                    
                    "kaalsarp_dosh": ["kaalsarp_dosh", "kaalsarp dosh", "kaalsarp dosha", "kaalsarp dos", "kaalsarp", "kalsarp", "kalsarp dos", "kalsarp", "kalsarp dosh"],

                    "manglik_dosh" : ["manglik_dosh", "manglik dosh", "manglik dosha", "manglik dos", "manglik", "manglek", "manglek dos", "manglek dosh"],

                    "pitra_dosh": ["pitra_dosh", "pitra dosh", "pitra dosha", "pitra dos", "pitra", "pitar", "piter", "pitraa","pitar dos", "pitar dosh"],
                    
                    "mahadasha": ["mahadasha", "mahadasa", "mahdasa", "mahdasha", "mahaadasha", "maha dasha", "maha dasa", "events"],
                    
                    "antardasha": ["antardasha", "antardasa", "antardashaa", "antardasaa", "anterdasha", "anterdasa", "anterdasaa", "anterdashaa"],
                    
                    "chardasha": ["chardasha", "chardashaa", "chardasa", "chardasaa", "chaardasa",  "chaardasaa", "chaardasha"],
                    
                    "chardasha_main": ["chardasha_main", "chardasha main", "chardasha main","chardasha-main", "chaardasha main", "chaardasha-main", "chardsha main", "chaardasaa main", "main chardasha", "main chardasa", "char dasha main", "char dasa main"],
                    
                    "yogini": ["yogini", "yogni", "yoogini", "yogne", "yognee", "yognie", "yoogni", "yog dasha", "yogini dasha", "yog", "yoog"],
                    
                    "sade_sati": ["sade_sati", "sade sati", "sade saati", "saade sati", "saade saati", "sade saty", "sade sateey", "sade satey", "sade-sati", "sade-saty","sadesati", "sati"],
                    
                    "friend_planets":["friend_planets", "friendship_planets","friendship", "friend", "friends", "friend planet", "friend planets", "friends planets", "planets friends", "planet friend", "planet friends", "enemies", "enemy"],
                    
                    "numero_table":["numero_table", "numero", "numero table", "favorite color", "favorite day", "favorite god", "favorite mantra", "favorite metal", "favorite stone", "favorite substone"],
                    
                    "varshapal_details":["varshapal_details", "varshapal", "varshpal", "muntha", "dinratri", "trirashi", "ayanamsaa", "varsha"],
                    
                    "ascendant_report":["ascendant_report", "ascendant report", "lagna report", "rising report"],
                    
                    "planet_report":["planet_report", "sun report", "moon report", "mercury report", "venus report", "mars report", "saturn report", "jupiter report", "jupyter report", "rahu report", "ketu report"],
                    
                    # "personal_characteristics":["personal_characteristics", "personal characteristics", "characteristics"],
                    
                    "chog_muhurta":["chog_muhurta", "choghadiya_muhurta", "choghadiya muhurta", "choghadiya-muhurta", "choghadiya", "chog muhurta", "chog mahurta", "muhurat"],
                    
                    "hora_muhurta":["hora_muhurta", "hora muhurta", "hora-muhurta", "hora mahurta", "hora mahurat", "mahurat", "mohrat","muhurta", "muhurta", "mahurta", "hora mohurat", "hora muhurat", "hora muhurata", "hora-mohrat", "hora-muhurta"],
                    
                    "moon_phase":["moon_phase", "moon phase", "moon-phase","moon phese", "phase", "moon luminance", "luminance", "paksha"],
                    
                    "solar_noon":["solar_noon", "solar noon", "sun noon", "sun-noon" ,"sun non"],
                    
                    "retrogrades":["retrogrades", "retrograde", "retro grades", "retro grade" , "retro-grades", "retro-grade"],
                    
                    "biorhythm":["biorhythm", "bio rhythm", "bio-rhythm", "biorithm" , "biorythm", "retro-grade", "physical", "emotional", "emotion", "emotions","intellectual"],
                    
                    "day_no": ["day_no", "day no", "days no", "day-no" , "days-no", "day number", "day numbers"],
                    
                    "numerology": ["numerology", "numero logy", "numrology", "numero-logy"],
                    
                    "gem_details":["gem_details", "gem details", "gems details", "gems detail" , "gems-detail", "gems-details","gem-detail", "gem-details", "gems", "gem", "diseases", "health", "finger", "metal"],
                    
                    "nakshatra_vastu":["nakshatra_vastu", "nakshatra vastu", "naksatra vastu", "vastu"],
                    
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

 
                question_modified = generate_question(translated_text, entity, age)
                response = chain.invoke({"context": memory.load_memory_variables({})["history"], "question": question_modified})
                result = response["text"]

            except Exception as e:
                print(f"Model invocation failed with error: {e}")
            
            response = result

            print(response, "+++")
            if userLanguage == "hi":
                if "positive interpretation" in response or "positive prediction" in response:
                    response = response[response.index("positive")+26:]
                    translated_text = Translator.translate_text(response, from_language='auto', to_language='hi', translator='google')
                    # translated_text = GoogleTranslator(source='auto', target='hi').translate(response)
                    print(userLanguage, "userLanguage", translated_text, "translated_text")
                    return {"answer":translated_text.replace("\n", " ")}
                
                elif "Based on your birth chart" in response or "Based on your birth details" in response or "Based on your Kundli" in response:
                    translated_text = Translator.translate_text(response, from_language='auto', to_language='hi', translator='google')
                    # translated_text = GoogleTranslator(source='auto', target='hi').translate(response)
                    print(userLanguage, "userLanguage", translated_text, "translated_text")
                    return {"answer":translated_text[translated_text.index(",")+2:].replace("\n", " ")}
                
                else:
                    translated_text = Translator.translate_text(response, from_language='auto', to_language='hi', translator='google')
                    # translated_text = GoogleTranslator(source='auto', target='hi').translate(response)
                    print(userLanguage, "userLanguage", translated_text, "translated_text")
                    return {"answer":translated_text.replace("\n", " ")}
                
            elif userLanguage == "Hinglish":
                print(response, "response in hinglish language +++")
                if "positive interpretation" in response or "positive prediction" in response:
                    response = response[response.index("positive")+26:]
                    # translated_text = Translator.translate_text(response, from_language='auto', to_language='hi', translator='google')
                    # translated_text = GoogleTranslator(source='auto', target='hi').translate(response)
                    # print(translated_text, "translated_text before apply hindi_to_roman")
                    # roman_text = hindi_to_roman(translated_text)
                    # print(roman_text)
                    # print(userLanguage, "userLanguage", roman_text, "roman_text")
                    return {"answer": response}
                
                elif "Based on your birth chart" in response or "Based on your birth details" in response or "Based on your Kundli" in response:
                    response = response[response.index(",")+2:]
                    # translated_text = Translator.translate_text(response, from_language='auto', to_language='hi', translator='google')
                    # translated_text = GoogleTranslator(source='auto', target='hi').translate(response)
                    # print(translated_text, "translated_text before apply hindi_to_roman")
                    # roman_text = hindi_to_roman(translated_text)
                    # print(userLanguage, "userLanguage", roman_text, "roman_text")
                    return {"answer":response}

                else:
                    # translated_text = Translator.translate_text(response, from_language='auto', to_language='hi', translator='google')
                    # translated_text = GoogleTranslator(source='auto', target='hi').translate(response)
                    # print(translated_text, "translated_text before apply hindi_to_roman")
                    # roman_text = hindi_to_roman(translated_text)
                    # print(userLanguage, "userLanguage", roman_text, "roman_text")

                    filter_response = remove_ques_from_ans(question,response)
                    return {"answer": filter_response}
                
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
        if userLanguage == "hi":
            return {"answer":"इस प्रश्न का सही और स्पष्ट उत्तर देने के लिए मुझे थोड़ा और समय या अधिक शोध की आवश्यकता होगी। मैं निश्चित रूप से सबसे अच्छा उत्तर प्रस्तुत करूंगा। आपकी समझ और विश्वास के लिए धन्यवाद"}
        elif userLanguage == "Hinglish":
            return {"answer":"Is prashn ka sahi aur spasht uttar dene ke liye mujhe thoda aur samay ya adhik research karni hogi. Main iska uttam uttar zarur prastut karunga. Dhanyavaad aapki samajh aur vishwas ke liye"}
        else:
            return {"answer":"To give a correct and clear answer to this question, I will need a little more time or more research. I will definitely present the best answer. Thank you for your understanding and trust"}



@app.post("/palmistry")
async def palmistry(file: UploadFile = File(...)):
    try:
        # Save uploaded file to a temporary directory
        temp_dir = "./palmistry/code/input"
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
        detected(net, path_to_warped_image_clean, path_to_palmline_image, resize_value)

        # Step 3: Line classification
        lines = classify(path_to_palmline_image)

        # Step 4: Length measurement
        im, contents = measure(path_to_warped_image_mini, lines)

        # Step 5: Save result
        save_result(im, contents, resize_value, path_to_result)
        # os.remove(f"{temp_dir}/{file.filename}")
        
        # return JSONResponse(status_code=200, content={"message": "Palmistry analysis completed.", "result": contents})
        return FileResponse(path="./palmistry/code/results/result.jpg", media_type="application/octet-stream", filename="result.jpg")

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", reload=True)