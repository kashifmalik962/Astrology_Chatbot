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
import requests


class Item(BaseModel):
    year:str=None
    month:str=None
    day:str=None
    hour:str=None
    minute:str=None
    birth_place:str=None



utc = 5.5  # UTC offset for the time zone
latitude = 28.6139  # Example: Delhi latitude
longitude = 77.2090  # Example: Delhi longitude
ayanamsa = "Lahiri"
house_system = "Placidus"
return_style = "json"


def detect_hinglish(text):
    print(text, "text in detect_hinglish")
    hindi_words = ['agar', 'jab','kab' ,'isliye', 'jabki', 'kyun', 'par', 'hogi' ,'phir', 'kaise', 'bas', 'hai', 'kya', 'apni' ,'koi', 'kis', 'mera', 'meri','Meri' ,'sabhi', 'magar', 'aur', 'toh', 'lekin', 'kuch', 'kisne', 'jise', 'tum', 'he']  # Add more transliterated Hindi words
    hinglish = [word for word in hindi_words if word in text.split()]
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


def get_lat_long(location_name):
    geolocator = Nominatim(user_agent="geopy_example",timeout=10)
    location = geolocator.geocode(location_name)

    if location:
        latitude, longitude = location.latitude, location.longitude
        return latitude, longitude
    else:
        return 28.7041, 77.1025

def get_horoscope_data(year,month,day,hour,minute,birth_place):
    birth_place = get_lat_long(birth_place)
    
    # Initialize Vedic Horoscope Data
    horoscope = VedicAstro.VedicHoroscopeData(
        int(year), int(month), int(day), int(hour), int(minute), 0,
        utc, int(birth_place[0]), int(birth_place[1]), ayanamsa, house_system
    )
    
    # Generate Chart
    chart = horoscope.generate_chart()

    # Extract details
    planets_data = horoscope.get_planets_data_from_chart(chart)
    houses_data = horoscope.get_houses_data_from_chart(chart)

    # print("planets_data", planets_data,"houses_data", houses_data)
    
    planets_houses_data = {
        "planets_data": planets_data,
        "houses_data": houses_data,
    }
    
    # Convert planets and houses data to dictionaries
    planets_data_list = [i._asdict() for i in planets_houses_data["planets_data"]]
    houses_data_list = [i._asdict() for i in planets_houses_data["houses_data"]]

    # Organize the data into dictionaries
    final_data = [{"planets_data": planets_data_list}, {"houses_data": houses_data_list}]

    # Format the planets data with house and rasi information
    def format_planets_data(planets_data):
        house_lookup = {house['HouseNr']: house['Rasi'] for house in planets_data[1]['houses_data']}
        return [f"{planet['Object']}: House {planet['HouseNr']} ({house_lookup.get(planet['HouseNr'], 'Unknown')}{', Retrograde' if planet['isRetroGrade'] else ''})"
                for planet in planets_data[0]['planets_data']]

    # Print formatted planet information
    formatted_planets_data = format_planets_data(final_data)
    return formatted_planets_data


# def predict_category(category, horoscope_data):
#     # Process horoscope data for predictions
#     houses_data = horoscope_data['houses_data']

#     # Map category to astrological insights
#     if category.lower() in ["love", "marriage", "love marriage","romance"]:
#         # Use 7th house insights for relationships and marriage
#         seventh_house = next(h for h in houses_data if h.HouseNr == 7)
#         return (
#             f"{year}-{month}-{day} {hour}:{minute}:{second} latitude={latitude} longitude={longitude}"
#             f"✨ Love & Marriage Prediction: Your 7th house, which governs relationships and marriage, is in {seventh_house.Rasi}. "
#             f"This house is ruled by {seventh_house.RasiLord}, the planet of love and beauty. "
#             f"The Nakshatra in this house is {seventh_house.Nakshatra}, which is ruled by {seventh_house.NakshatraLord}, "
#             f"indicating strong emotional connections and potential for a meaningful partnership. "
#             f"With {seventh_house.SubLord} as the Sub-lord, there may be a connection with someone who shares deep values, "
#             f"possibly leading to a life-changing commitment."
#         )

#     elif category.lower() in ["wealth", "income", "finance", "lottery", "bussiness","riche", "rich"]:
#         # Use 2nd and 11th house for wealth
#         second_house = next(h for h in houses_data if h.HouseNr == 2)
#         eleventh_house = next(h for h in houses_data if h.HouseNr == 11)
#         return (
#             f"{year}-{month}-{day} {hour}:{minute}:{second} latitude={latitude} longitude={longitude}"
#             f"💰 Wealth Prediction: Your 2nd house, representing material possessions and wealth, is in {second_house.Rasi}, "
#             f"ruled by {second_house.RasiLord}, the planet of luxury. This suggests a strong potential for wealth accumulation. "
#             f"The Nakshatra in this house is {second_house.Nakshatra}, ruled by {second_house.NakshatraLord}, "
#             f"indicating prosperity in your career or business. The 11th house of gains is in {eleventh_house.Rasi}, "
#             f"ruled by {eleventh_house.RasiLord}, with Nakshatra {eleventh_house.Nakshatra}. This is a favorable position for "
#             f"financial success and unexpected gains! Stay open to new opportunities, and you may witness wealth flow in unexpected ways."
#         )

#     elif category.lower() in ["career","job","trade","work", "profession", "occupation"]:
#         # Use 10th house insights for career
#         tenth_house = next(h for h in houses_data if h.HouseNr == 10)
#         return (
#             f"{year}-{month}-{day} {hour}:{minute}:{second} latitude={latitude} longitude={longitude}"
#             f"🚀 Career Prediction: Your 10th house, which represents career and profession, is in {tenth_house.Rasi}, "
#             f"ruled by {tenth_house.RasiLord}, the planet of discipline and structure. This house suggests strong career potential. "
#             f"The Nakshatra in this house is {tenth_house.Nakshatra}, ruled by {tenth_house.NakshatraLord}, indicating success "
#             f"through determination and hard work. The Sub-lord, {tenth_house.SubLord}, may guide you to career opportunities that align "
#             f"with your deeper purpose. Keep pushing forward, your career path looks promising!"
#         )

#     elif category.lower() in ["family", "relatives"]:
#         # Use 4th house insights for family and home
#         fourth_house = next(h for h in houses_data if h.HouseNr == 4)
#         return (
#             f"{year}-{month}-{day} {hour}:{minute}:{second} latitude={latitude} longitude={longitude}"
#             f"🏡 Family Prediction: Your 4th house, which governs home, family, and emotional well-being, is in {fourth_house.Rasi}. "
#             f"This house is ruled by {fourth_house.RasiLord}, the planet of comfort and nurturing. "
#             f"The Nakshatra in this house is {fourth_house.Nakshatra}, ruled by {fourth_house.NakshatraLord}, "
#             f"indicating a deep emotional connection with family. Your home life will be a source of comfort and stability. "
#             f"With {fourth_house.SubLord} as the Sub-lord, your relationships with family may grow closer in the coming months."
#         )

#     elif category.lower() in ["friends", "friend", "neighbour"]:
#         # Use 11th house for friendships and social networks
#         eleventh_house = next(h for h in houses_data if h.HouseNr == 11)
#         return (
#             f"{year}-{month}-{day} {hour}:{minute}:{second} latitude={latitude} longitude={longitude}"
#             f"👫 Friendships Prediction: Your 11th house, representing friendships, networks, and social connections, is in {eleventh_house.Rasi}. "
#             f"This house is ruled by {eleventh_house.RasiLord}, the planet of success and social recognition. "
#             f"The Nakshatra in this house is {eleventh_house.Nakshatra}, ruled by {eleventh_house.NakshatraLord}, "
#             f"indicating the potential for strong social bonds and beneficial connections. "
#             f"With {eleventh_house.SubLord} as the Sub-lord, your social circle may expand, bringing new friendships and alliances."
#         )

#     elif category.lower() in ["health", "fitness", "strength", "healthy", "stamina"]:
#         # Use 6th house for health and well-being
#         sixth_house = next(h for h in houses_data if h.HouseNr == 6)
#         return (
#             f"{year}-{month}-{day} {hour}:{minute}:{second} latitude={latitude} longitude={longitude}"
#             f"💪 Health Prediction: Your 6th house, which governs health and daily routines, is in {sixth_house.Rasi}. "
#             f"This house is ruled by {sixth_house.RasiLord}, the planet of service and discipline. "
#             f"The Nakshatra in this house is {sixth_house.Nakshatra}, ruled by {sixth_house.NakshatraLord}, "
#             f"indicating a period of focus on improving your health and well-being. "
#             f"With {sixth_house.SubLord} as the Sub-lord, a disciplined approach to your lifestyle will benefit you greatly."
#         )

#     elif category.lower() in ["spirituality", "inner peace", "peace"]:
#         # Use 12th house for spirituality and inner peace
#         twelfth_house = next(h for h in houses_data if h.HouseNr == 12)
#         return (
#             f"{year}-{month}-{day} {hour}:{minute}:{second} latitude={latitude} longitude={longitude}"
#             f"🌙 Spirituality Prediction: Your 12th house, which governs spirituality, isolation, and the subconscious, is in {twelfth_house.Rasi}. "
#             f"This house is ruled by {twelfth_house.RasiLord}, the planet of mysticism and transcendence. "
#             f"The Nakshatra in this house is {twelfth_house.Nakshatra}, ruled by {twelfth_house.NakshatraLord}, "
#             f"indicating a strong connection to your inner self and spiritual practices. "
#             f"With {twelfth_house.SubLord} as the Sub-lord, this is a good time for introspection and spiritual growth."
#         )

#     elif category.lower() in ["education", "learning", "training", "knowledge", "schooling", "school", "learn", "collage", "university"]:
#         # Use 5th house for education and knowledge
#         fifth_house = next(h for h in houses_data if h.HouseNr == 5)
#         return (
#             f"{year}-{month}-{day} {hour}:{minute}:{second} latitude={latitude} longitude={longitude}"
#             f"📚 Education Prediction: Your 5th house, which governs learning, creativity, and intelligence, is in {fifth_house.Rasi}. "
#             f"This house is ruled by {fifth_house.RasiLord}, the planet of knowledge and wisdom. "
#             f"The Nakshatra in this house is {fifth_house.Nakshatra}, ruled by {fifth_house.NakshatraLord}, "
#             f"indicating an excellent period for academic and intellectual growth. "
#             f"With {fifth_house.SubLord} as the Sub-lord, you may excel in your studies or creative endeavors."
#         )

#     elif category.lower() in ["travel", "journey", "tour", "trip", "picnic"]:
#         # Use 9th house for travel and exploration
#         ninth_house = next(h for h in houses_data if h.HouseNr == 9)
#         return (
#             f"{year}-{month}-{day} {hour}:{minute}:{second} latitude={latitude} longitude={longitude}"
#             f"🌍 Travel Prediction: Your 9th house, which governs long-distance travel, higher learning, and philosophy, is in {ninth_house.Rasi}. "
#             f"This house is ruled by {ninth_house.RasiLord}, the planet of expansion and exploration. "
#             f"The Nakshatra in this house is {ninth_house.Nakshatra}, ruled by {ninth_house.NakshatraLord}, "
#             f"indicating the potential for travel or a journey that will broaden your horizons. "
#             f"With {ninth_house.SubLord} as the Sub-lord, new opportunities for personal exploration are on the horizon."
#         )

#     elif category.lower() in ["children", "kids", "boys and girls", "boys", "girl"]:
#         # Use 5th house for children and creativity
#         fifth_house = next(h for h in houses_data if h.HouseNr == 5)
#         return (
#             f"{year}-{month}-{day} {hour}:{minute}:{second} latitude={latitude} longitude={longitude}"
#             f"👶 Children Prediction: Your 5th house, which governs children, creativity, and intelligence, is in {fifth_house.Rasi}. "
#             f"This house is ruled by {fifth_house.RasiLord}, the planet of fertility and creativity. "
#             f"The Nakshatra in this house is {fifth_house.Nakshatra}, ruled by {fifth_house.NakshatraLord}, "
#             f"indicating growth and potential in the area of family and children. "
#             f"With {fifth_house.SubLord} as the Sub-lord, there may be blessings or opportunities related to children in the near future."
#         )

#     elif category.lower() in ["personal growth", "improvement", "development", "maturity", "empowerment"]:
#         # Use 8th house for transformation and personal growth
#         eighth_house = next(h for h in houses_data if h.HouseNr == 8)
#         return (
#             f"{year}-{month}-{day} {hour}:{minute}:{second} latitude={latitude} longitude={longitude}"
#             f"🌀 Personal Growth Prediction: Your 8th house, which governs transformation, change, and deep psychological insight, is in {eighth_house.Rasi}. "
#             f"This house is ruled by {eighth_house.RasiLord}, the planet of regeneration and depth. "
#             f"The Nakshatra in this house is {eighth_house.Nakshatra}, ruled by {eighth_house.NakshatraLord}, "
#             f"indicating a powerful period of self-transformation and growth. "
#             f"With {eighth_house.SubLord} as the Sub-lord, you may go through profound inner changes that help you become the best version of yourself."
#         )

#     elif category.lower() in ["success", "achievement"]:
#         # Use 10th house for success and career achievements
#         tenth_house = next(h for h in houses_data if h.HouseNr == 10)
#         return (
#             f"{year}-{month}-{day} {hour}:{minute}:{second} latitude={latitude} longitude={longitude}"
#             f"🏆 Success Prediction: Your 10th house, which governs career and achievements, is in {tenth_house.Rasi}. "
#             f"This house is ruled by {tenth_house.RasiLord}, the planet of discipline and structure. "
#             f"The Nakshatra in this house is {tenth_house.Nakshatra}, ruled by {tenth_house.NakshatraLord}, "
#             f"indicating a period of hard work and achievement. "
#             f"With {tenth_house.SubLord} as the Sub-lord, your dedication will pay off and bring success in your professional life."
#         )

#     elif category.lower() in ["mental well-being", "emotional health", "mental health", "psychological balance"]:
#         # Use 6th house for mental health
#         sixth_house = next(h for h in houses_data if h.HouseNr == 6)
#         return (
#             f"{year}-{month}-{day} {hour}:{minute}:{second} latitude={latitude} longitude={longitude}"
#             f"🧠 Mental Well-being Prediction: Your 6th house, governing health and wellness, is in {sixth_house.Rasi}. "
#             f"Ruled by {sixth_house.RasiLord}, the planet of discipline and service, this house suggests a need for balance in your mental health. "
#             f"The Nakshatra in this house is {sixth_house.Nakshatra}, ruled by {sixth_house.NakshatraLord}, "
#             f"indicating a focus on maintaining mental clarity and peace of mind. "
#             f"With {sixth_house.SubLord} as the Sub-lord, try to incorporate stress-reduction techniques in your routine."
#         )

#     elif category.lower() in ["social life", "life", "social", "social activity","community", "society"]:
#         # Use 11th house for social life
#         eleventh_house = next(h for h in houses_data if h.HouseNr == 11)
#         return (
#             f"{year}-{month}-{day} {hour}:{minute}:{second} latitude={latitude} longitude={longitude}"
#             f"🌐 Social Life Prediction: Your 11th house, representing social networks, friends, and public life, is in {eleventh_house.Rasi}. "
#             f"Ruled by {eleventh_house.RasiLord}, the planet of gains and success, this suggests a vibrant social life. "
#             f"The Nakshatra in this house is {eleventh_house.Nakshatra}, ruled by {eleventh_house.NakshatraLord}, "
#             f"indicating connections with influential people or social circles. "
#             f"With {eleventh_house.SubLord} as the Sub-lord, expect exciting social events and interactions."
#         )

#     elif category.lower() == "harmony":
#         # Use 7th house for harmony in relationships
#         seventh_house = next(h for h in houses_data if h.HouseNr == 7)
#         return (
#             f"{year}-{month}-{day} {hour}:{minute}:{second} latitude={latitude} longitude={longitude}"
#             f"🎵 Harmony Prediction: Your 7th house, representing marriage and relationships, is in {seventh_house.Rasi}. "
#             f"Ruled by {seventh_house.RasiLord}, the planet of love and balance, this suggests a harmonious relationship period. "
#             f"The Nakshatra in this house is {seventh_house.Nakshatra}, ruled by {seventh_house.NakshatraLord}, "
#             f"indicating peaceful and loving connections with your partner. "
#             f"With {seventh_house.SubLord} as the Sub-lord, this is a great time for building or enhancing harmony in your relationships."
#         )

#     return "Category not recognized. Please enter a valid category."



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
    global questions, df, userLanguage,  year, month, day, hour , minute, second, birth_place
    
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
    print(userLanguage, "userLanguage +++++++++++++++++++++++++ ")
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
            
            def generate_question(translated_text, horoscope_data, item, age):
                """Generate the appropriate question based on age."""
                base_question = (
                    f"Only act as an astrologer and do not reply to questions other than astrology. "
                    f"Let's say the question is '{translated_text}'. "
                    f"This is my BirthChart details={horoscope_data}. "
                    f"This is my birthdate=[{item.day},{item.month},{item.year}, {item.hour}:{item.minute}, {item.birth_place}]. "
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
            
            print("horoscope_data running...",item.year,item.month,item.day,item.hour,item.minute,item.birth_place)
            horoscope_data = get_horoscope_data(item.year,item.month,item.day,item.hour,item.minute,item.birth_place)
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
            model = OllamaLLM(model="llama3.2", temperature=0.1, top_k=10, top_p=0.8)
            prompt = ChatPromptTemplate.from_template(template)
            memory = ConversationBufferMemory(input_key="question", memory_key="history")
            chain = LLMChain(llm=model, prompt=prompt, memory=memory)
            
            age = calculate_age(item.year)
            
            # Generate question and get response
            try:
                question = generate_question(translated_text, horoscope_data, item, age)
                response = chain.invoke({"context": memory.load_memory_variables({})["history"], "question": question})
                result = response["text"]
                print(result, "result response[text] ##########")
            except Exception as e:
                print(f"Model invocation failed with error: {e}")
            
            # if 15 > age:
            #     print(f"Only act as an astrologer and do not reply for question other than astrology, let say the question is '{translated_text}'. This is my BirthChart details={horoscope_data}. This is my birthdate=[{item.day},{item.month},{item.year}, {item.hour}:{item.minute}, {item.birth_place}]. Considering my age is under 15 according my kundli, please give positive answer in 50 to 60 words only")
            #     try:
            #         result = chain.invoke({"context":"", "question":f"Only act as an astrologer and do not reply for question other than astrology, let say the question is '{translated_text}'. This is my BirthChart details={horoscope_data}. This is my birthdate=[{item.day},{item.month},{item.year}, {item.hour}:{item.minute}, {item.birth_place}]. Considering my age is under 15 according my kundli, please give positive answer in 50 to 60 words only"})
            #     except Exception as e:
            #         print("Model is not Woring ",e)
            # elif 50 < age:
            #     print(f"Only act as an astrologer and do not reply for question other than astrology, let say the question is '{translated_text}'. This is my BirthChart details={horoscope_data}. This is my birthdate=[{item.day},{item.month},{item.year}, {item.hour}:{item.minute}, {item.birth_place}]. Considering my age greater then 50 according my kundli, please give positive answer in 50 to 60 words only")
            #     try:
            #         result = chain.invoke({"context":"", "question":f"Only act as an astrologer and do not reply for question other than astrology, let say the question is '{translated_text}'. This is my BirthChart details={horoscope_data}. This is my birthdate=[{item.day},{item.month},{item.year}, {item.hour}:{item.minute}, {item.birth_place}]. Considering my age greater then 50 according my kundli, please give positive answer in 50 to 60 words only"})
            #     except Exception as e:
            #         print("Model is not Woring ",e)
            # else:
            #     print(f"Only act as an astrologer and do not reply for question other than astrology, let say the question is '{translated_text}'. This is my BirthChart details={horoscope_data}. This is my birthdate=[{item.day},{item.month},{item.year}, {item.hour}:{item.minute}, {item.birth_place}]. According my kundli, please give positive answer in 50 to 60 words only")
            #     try:
            #         result = chain.invoke({"context":"", "question":f"Only act as an astrologer and do not reply for question other than astrology, let say the question is '{translated_text}'. This is my BirthChart details={horoscope_data}. This is my birthdate=[{item.day},{item.month},{item.year}, {item.hour}:{item.minute}, {item.birth_place}]. According my kundli, please give positive answer in 50 to 60 words only"})
            #     except Exception as e:
            #         print("Model is not Woring ",e)
            
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