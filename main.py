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
    print(text, "text in detect_hinglish")
    hindi_words = ['agar', 'jab','kab' ,'isliye', 'jabki', 'kyun', 'par', 'hogi' ,'phir', 'kaise', 'bas', 'hai', 'kya', 'apni' ,'koi', 'kis', 'mera', 'meri','sabhi', 'magar', 'aur', 'toh', 'lekin', 'kuch', 'kisne', 'jise', 'tum', 'he']  # Add more transliterated Hindi words
    hinglish = [word for word in hindi_words if word.lower() in text.split()]
    print(hinglish, "hinglish +++++++++")
    if len(hinglish) > 0:
        return "Hinglish"
    else:
        return detect(text)

def hindi_to_roman(hindi_text):
    # Transliterate from Devanagari (Hindi) to Roman
    roman_text = sanscript.transliterate(hindi_text, sanscript.DEVANAGARI, sanscript.ITRANS)
    roman_text_lower = roman_text.lower()
    roman_text_fresh_wrd = [word[0:-1] if word[-1] == "a" or word == "mem" else word for word in roman_text_lower.split()]
    print(roman_text_fresh_wrd, "roman_text_fresh_wrd after modify")
    return " ".join(roman_text_fresh_wrd)

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


    # Get radical Lagna number
    jd = swe.julday(int(year), int(month), int(day), int(hour) + int(minute) / 60.0)
    lagna = calculate_lagna(jd, birth_place_pin[0], birth_place_pin[1])
    zodiac_info = get_zodiac_info(lagna)

    print(zodiac_info, "zodiac_info +++++++=====")
    
    return formatted_planets_data, zodiac_info


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
        translated_text = Translator.translate_text(question, from_language='auto', to_language='en', translator='google')
        print(translated_text, "convert question ++")
        userLanguage = "hi"
        text = cnvrtLowerCase(removeHtmlTag(removeUrls(removePunctuation(removeQuatation(translated_text)))))
        print(text, "text")
    elif detect_lang_user == "Hinglish":
        translated_text = Translator.translate_text(question, from_language='auto', to_language='hi', translator='google')
        translated_text = Translator.translate_text(question, from_language='auto', to_language='en', translator='google')
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
        if similarities[1] > .90:
            print(df["Answer"][similarities[0]])
            if userLanguage == "hi":
                translated_text = Translator.translate_text(df["Answer"][similarities[0]],from_language='auto', to_language='hi', translator='google')
                return {"answer":translated_text}
            elif userLanguage == "Hinglish":
                translated_text = Translator.translate_text(df["Answer"][similarities[0]], from_language='auto', to_language='hi', translator='google')
                roman_text = hindi_to_roman(roman_text)
                return {"answer":translated_text}
            else:
                return {"answer":df["Answer"][similarities[0]]}
        else:
            print("llama model running......")

            def generate_question(translated_text, horoscope_data, radical_no_with_lagna, item, age):
                """Generate the appropriate question based on age."""
                base_question = (
                    f"Only act as an astrologer and do not reply to questions other than astrology. "
                    f"Let's say the question is '{translated_text}'. "
                    f"This is my BirthChart details={horoscope_data}. "
                    f"{radical_no_with_lagna}. "
                    # f"This is my birthdate=[{item.day},{item.month},{item.year}, {item.hour}:{item.minute}, {item.birth_place_pin}]. "
                )
                if age < 15:
                    print(base_question + "Considering my age is under 15 according to my kundli, please give a positive answer in 50 to 60 words only.")
                    return base_question + "Considering my age is under 15 according to my kundli, please give a positive answer in 50 to 60 words only."
                elif age > 50:
                    print(base_question + "Considering my age is greater than 50 according to my kundli, please give a positive answer in 50 to 60 words only.")
                    return base_question + "Considering my age is greater than 50 according to my kundli, please give a positive answer in 50 to 60 words only."
                else:
                    print(base_question + "According to my kundli, please give a positive answer in 50 to 60 words only.")
                    return base_question + "According to my kundli, please give a positive answer in 50 to 60 words only."
                
            
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
            
            print("horoscope_data running...",item.year,item.month,item.day,item.hour,item.minute,item.birth_place_pin)
            horoscope_data, radical_no_with_lagna  = get_horoscope_data(item.year,item.month,item.day,item.hour,item.minute,item.birth_place_pin)
            # print(horoscope_data, "horoscope_data +++++")
            # response = predict_category(text, horoscope_data)
            # response = horoscope_data
            
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
                # Convert greeting words to a set for O(1) lookup time
                match_greeting_words = {"heloo", "hello", "hey", "heyy" , "namaste", "namastee", "hy", "heey", "hi", "hii", "hiii"}

                # Split the translated text into words and check for greetings
                words_in_text = translated_text.split()

                # Check if any word in the translated text matches a greeting word using set lookup
                if any(word in match_greeting_words for word in words_in_text):
                    print("greetings")
                    # Call the model only if greeting is found
                    response = chain.invoke({"context": memory.load_memory_variables({})["history"], "question": question})
                    result = response["text"]
                    print(result, "result response[text] ##########")
                else:
                    print("not greeting")
                    # Generate the question and invoke model only for non-greeting text
                    question = generate_question(translated_text, horoscope_data, radical_no_with_lagna, item, age)
                    response = chain.invoke({"context": memory.load_memory_variables({})["history"], "question": question})
                    result = response["text"]
                    print(result, "result response[text] ##########")

            except Exception as e:
                print(f"Model invocation failed with error: {e}")

            response = result

            print(response, "+++")
            if userLanguage == "hi":
                if "positive interpretation" in response or "positive prediction" in response:
                    response = response[response.index("positive")+26:]
                    translated_text = Translator.translate_text(response, from_language='auto', to_language='hi', translator='google')
                    print(userLanguage, "userLanguage", translated_text, "translated_text")
                    return {"answer":translated_text}
                
                elif "Based on your birth chart" in response:
                    translated_text = Translator.translate_text(response, from_language='auto', to_language='hi', translator='google')
                    print(userLanguage, "userLanguage", translated_text, "translated_text")
                    return {"answer":translated_text[translated_text.index(",")+2:]}
                
                else:
                    translated_text = Translator.translate_text(response, from_language='auto', to_language='hi', translator='google')
                    print(userLanguage, "userLanguage", translated_text, "translated_text")
                    return {"answer":translated_text}
                
            elif userLanguage == "Hinglish":
                if "positive interpretation" in response or "positive prediction" in response:
                    response = response[response.index("positive")+26:]
                    translated_text = Translator.translate_text(response, from_language='auto', to_language='hi', translator='google')
                    roman_text = hindi_to_roman(translated_text)
                    print(roman_text)
                    print(userLanguage, "userLanguage", roman_text, "roman_text")
                    return {"answer": roman_text}
                
                elif "Based on your birth chart" in response:
                    response = response[response.index(",")+2:]
                    translated_text = Translator.translate_text(response, from_language='auto', to_language='hi', translator='google')
                    roman_text = hindi_to_roman(translated_text)
                    print(userLanguage, "userLanguage", roman_text, "roman_text")
                    return {"answer":roman_text}

                else:
                    translated_text = Translator.translate_text(response, from_language='auto', to_language='hi', translator='google')
                    roman_text = hindi_to_roman(translated_text)
                    print(userLanguage, "userLanguage", roman_text, "roman_text")
                    return {"answer":roman_text}
                
            else:
                # User by-default language is english
                
                if "positive interpretation" in response or "positive prediction" in response:
                    response = response[response.index("positive")+26:]
                    print(userLanguage, "userLanguage", response, "response")
                    return {"answer":response}
                elif "Based on your birth chart" in response:
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