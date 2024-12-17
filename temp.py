# from transformers import AutoModelForCausalLM, AutoTokenizer

# # Load the model and tokenizer (using the correct identifier)
# model_name = "llama-2-7b-chat.ggmlv3.q8_0.bin"  # Replace with the actual model identifier

# model = AutoModelForCausalLM.from_pretrained(model_name, use_auth_token='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')
# tokenizer = AutoTokenizer.from_pretrained(model_name)

# # Generate text
# prompt = "What is the capital of France?"
# input_ids = tokenizer(prompt, return_tensors="pt").input_ids

# # Generate text
# output = model.generate(input_ids, max_new_tokens=50)
# generated_text = tokenizer.decode(output[0], skip_special_tokens=True)

# print(generated_text)



from vedicastro import VedicAstro

# Define birth details and settings (customize with user input or default)
year = 1992
month = 1
day = 2
hour = 6
minute = 40
second = 0
utc = 5.5  # UTC offset for the time zone
latitude = 28.6139  # Example: Delhi latitude
longitude = 77.2090  # Example: Delhi longitude
ayanamsa = "Lahiri"
house_system = "Placidus"
return_style = "json"

def get_horoscope_data():
    # Initialize Vedic Horoscope Data
    horoscope = VedicAstro.VedicHoroscopeData(
        year, month, day, hour, minute, second,
        utc, latitude, longitude, ayanamsa, house_system
    )
    
    # Generate Chart
    chart = horoscope.generate_chart()

    # Extract details
    planets_data = horoscope.get_planets_data_from_chart(chart)
    houses_data = horoscope.get_houses_data_from_chart(chart)

    return {
        "planets_data": planets_data,
        "houses_data": houses_data,
    }

def predict_category(category, horoscope_data):
    # Process horoscope data for predictions
    houses_data = horoscope_data['houses_data']

    print(houses_data, "houses_data data ++")

    # Map category to astrological insights
    if category.lower() in ["love", "marriage", "love marriage","romance"]:
        # Use 7th house insights for relationships and marriage
        seventh_house = next(h for h in houses_data if h.HouseNr == 7)
        return (
            f"✨ Love & Marriage Prediction: Your 7th house, which governs relationships and marriage, is in {seventh_house.Rasi}. "
            f"This house is ruled by {seventh_house.RasiLord}, the planet of love and beauty. "
            f"The Nakshatra in this house is {seventh_house.Nakshatra}, which is ruled by {seventh_house.NakshatraLord}, "
            f"indicating strong emotional connections and potential for a meaningful partnership. "
            f"With {seventh_house.SubLord} as the Sub-lord, there may be a connection with someone who shares deep values, "
            f"possibly leading to a life-changing commitment."
        )

    elif category.lower() in ["wealth", "income", "finance", "lottery", "bussiness","riche", "rich"]:
        # Use 2nd and 11th house for wealth
        second_house = next(h for h in houses_data if h.HouseNr == 2)
        eleventh_house = next(h for h in houses_data if h.HouseNr == 11)
        return (
            f"💰 Wealth Prediction: Your 2nd house, representing material possessions and wealth, is in {second_house.Rasi}, "
            f"ruled by {second_house.RasiLord}, the planet of luxury. This suggests a strong potential for wealth accumulation. "
            f"The Nakshatra in this house is {second_house.Nakshatra}, ruled by {second_house.NakshatraLord}, "
            f"indicating prosperity in your career or business. The 11th house of gains is in {eleventh_house.Rasi}, "
            f"ruled by {eleventh_house.RasiLord}, with Nakshatra {eleventh_house.Nakshatra}. This is a favorable position for "
            f"financial success and unexpected gains! Stay open to new opportunities, and you may witness wealth flow in unexpected ways."
        )

    elif category.lower() in ["career","job","trade","work", "profession", "occupation"]:
        # Use 10th house insights for career
        tenth_house = next(h for h in houses_data if h.HouseNr == 10)
        return (
            f"🚀 Career Prediction: Your 10th house, which represents career and profession, is in {tenth_house.Rasi}, "
            f"ruled by {tenth_house.RasiLord}, the planet of discipline and structure. This house suggests strong career potential. "
            f"The Nakshatra in this house is {tenth_house.Nakshatra}, ruled by {tenth_house.NakshatraLord}, indicating success "
            f"through determination and hard work. The Sub-lord, {tenth_house.SubLord}, may guide you to career opportunities that align "
            f"with your deeper purpose. Keep pushing forward, your career path looks promising!"
        )

    elif category.lower() in ["family", "relatives"]:
        # Use 4th house insights for family and home
        fourth_house = next(h for h in houses_data if h.HouseNr == 4)
        return (
            f"🏡 Family Prediction: Your 4th house, which governs home, family, and emotional well-being, is in {fourth_house.Rasi}. "
            f"This house is ruled by {fourth_house.RasiLord}, the planet of comfort and nurturing. "
            f"The Nakshatra in this house is {fourth_house.Nakshatra}, ruled by {fourth_house.NakshatraLord}, "
            f"indicating a deep emotional connection with family. Your home life will be a source of comfort and stability. "
            f"With {fourth_house.SubLord} as the Sub-lord, your relationships with family may grow closer in the coming months."
        )

    elif category.lower() in ["friends", "friend", "neighbour"]:
        # Use 11th house for friendships and social networks
        eleventh_house = next(h for h in houses_data if h.HouseNr == 11)
        return (
            f"👫 Friendships Prediction: Your 11th house, representing friendships, networks, and social connections, is in {eleventh_house.Rasi}. "
            f"This house is ruled by {eleventh_house.RasiLord}, the planet of success and social recognition. "
            f"The Nakshatra in this house is {eleventh_house.Nakshatra}, ruled by {eleventh_house.NakshatraLord}, "
            f"indicating the potential for strong social bonds and beneficial connections. "
            f"With {eleventh_house.SubLord} as the Sub-lord, your social circle may expand, bringing new friendships and alliances."
        )

    elif category.lower() in ["health", "fitness", "strength", "healthy", "stamina"]:
        # Use 6th house for health and well-being
        sixth_house = next(h for h in houses_data if h.HouseNr == 6)
        return (
            f"💪 Health Prediction: Your 6th house, which governs health and daily routines, is in {sixth_house.Rasi}. "
            f"This house is ruled by {sixth_house.RasiLord}, the planet of service and discipline. "
            f"The Nakshatra in this house is {sixth_house.Nakshatra}, ruled by {sixth_house.NakshatraLord}, "
            f"indicating a period of focus on improving your health and well-being. "
            f"With {sixth_house.SubLord} as the Sub-lord, a disciplined approach to your lifestyle will benefit you greatly."
        )

    elif category.lower() in ["spirituality", "inner peace", "peace"]:
        # Use 12th house for spirituality and inner peace
        twelfth_house = next(h for h in houses_data if h.HouseNr == 12)
        return (
            f"🌙 Spirituality Prediction: Your 12th house, which governs spirituality, isolation, and the subconscious, is in {twelfth_house.Rasi}. "
            f"This house is ruled by {twelfth_house.RasiLord}, the planet of mysticism and transcendence. "
            f"The Nakshatra in this house is {twelfth_house.Nakshatra}, ruled by {twelfth_house.NakshatraLord}, "
            f"indicating a strong connection to your inner self and spiritual practices. "
            f"With {twelfth_house.SubLord} as the Sub-lord, this is a good time for introspection and spiritual growth."
        )

    elif category.lower() in ["education", "learning", "training", "knowledge", "schooling", "school", "learn", "collage", "university"]:
        # Use 5th house for education and knowledge
        fifth_house = next(h for h in houses_data if h.HouseNr == 5)
        return (
            f"📚 Education Prediction: Your 5th house, which governs learning, creativity, and intelligence, is in {fifth_house.Rasi}. "
            f"This house is ruled by {fifth_house.RasiLord}, the planet of knowledge and wisdom. "
            f"The Nakshatra in this house is {fifth_house.Nakshatra}, ruled by {fifth_house.NakshatraLord}, "
            f"indicating an excellent period for academic and intellectual growth. "
            f"With {fifth_house.SubLord} as the Sub-lord, you may excel in your studies or creative endeavors."
        )

    elif category.lower() in ["travel", "journey", "tour", "trip", "picnic"]:
        # Use 9th house for travel and exploration
        ninth_house = next(h for h in houses_data if h.HouseNr == 9)
        return (
            f"🌍 Travel Prediction: Your 9th house, which governs long-distance travel, higher learning, and philosophy, is in {ninth_house.Rasi}. "
            f"This house is ruled by {ninth_house.RasiLord}, the planet of expansion and exploration. "
            f"The Nakshatra in this house is {ninth_house.Nakshatra}, ruled by {ninth_house.NakshatraLord}, "
            f"indicating the potential for travel or a journey that will broaden your horizons. "
            f"With {ninth_house.SubLord} as the Sub-lord, new opportunities for personal exploration are on the horizon."
        )

    elif category.lower() in ["children", "kids", "boys and girls", "boys", "girl"]:
        # Use 5th house for children and creativity
        fifth_house = next(h for h in houses_data if h.HouseNr == 5)
        return (
            f"👶 Children Prediction: Your 5th house, which governs children, creativity, and intelligence, is in {fifth_house.Rasi}. "
            f"This house is ruled by {fifth_house.RasiLord}, the planet of fertility and creativity. "
            f"The Nakshatra in this house is {fifth_house.Nakshatra}, ruled by {fifth_house.NakshatraLord}, "
            f"indicating growth and potential in the area of family and children. "
            f"With {fifth_house.SubLord} as the Sub-lord, there may be blessings or opportunities related to children in the near future."
        )

    elif category.lower() in ["personal growth", "improvement", "development", "maturity", "empowerment"]:
        # Use 8th house for transformation and personal growth
        eighth_house = next(h for h in houses_data if h.HouseNr == 8)
        return (
            f"🌀 Personal Growth Prediction: Your 8th house, which governs transformation, change, and deep psychological insight, is in {eighth_house.Rasi}. "
            f"This house is ruled by {eighth_house.RasiLord}, the planet of regeneration and depth. "
            f"The Nakshatra in this house is {eighth_house.Nakshatra}, ruled by {eighth_house.NakshatraLord}, "
            f"indicating a powerful period of self-transformation and growth. "
            f"With {eighth_house.SubLord} as the Sub-lord, you may go through profound inner changes that help you become the best version of yourself."
        )

    elif category.lower() in ["success", "achievement"]:
        # Use 10th house for success and career achievements
        tenth_house = next(h for h in houses_data if h.HouseNr == 10)
        return (
            f"🏆 Success Prediction: Your 10th house, which governs career and achievements, is in {tenth_house.Rasi}. "
            f"This house is ruled by {tenth_house.RasiLord}, the planet of discipline and structure. "
            f"The Nakshatra in this house is {tenth_house.Nakshatra}, ruled by {tenth_house.NakshatraLord}, "
            f"indicating a period of hard work and achievement. "
            f"With {tenth_house.SubLord} as the Sub-lord, your dedication will pay off and bring success in your professional life."
        )

    elif category.lower() in ["mental well-being", "emotional health", "mental health", "psychological balance"]:
        # Use 6th house for mental health
        sixth_house = next(h for h in houses_data if h.HouseNr == 6)
        return (
            f"🧠 Mental Well-being Prediction: Your 6th house, governing health and wellness, is in {sixth_house.Rasi}. "
            f"Ruled by {sixth_house.RasiLord}, the planet of discipline and service, this house suggests a need for balance in your mental health. "
            f"The Nakshatra in this house is {sixth_house.Nakshatra}, ruled by {sixth_house.NakshatraLord}, "
            f"indicating a focus on maintaining mental clarity and peace of mind. "
            f"With {sixth_house.SubLord} as the Sub-lord, try to incorporate stress-reduction techniques in your routine."
        )

    elif category.lower() in ["social life", "life", "social", "social activity","community", "society"]:
        # Use 11th house for social life
        eleventh_house = next(h for h in houses_data if h.HouseNr == 11)
        return (
            f"🌐 Social Life Prediction: Your 11th house, representing social networks, friends, and public life, is in {eleventh_house.Rasi}. "
            f"Ruled by {eleventh_house.RasiLord}, the planet of gains and success, this suggests a vibrant social life. "
            f"The Nakshatra in this house is {eleventh_house.Nakshatra}, ruled by {eleventh_house.NakshatraLord}, "
            f"indicating connections with influential people or social circles. "
            f"With {eleventh_house.SubLord} as the Sub-lord, expect exciting social events and interactions."
        )

    elif category.lower() == "harmony":
        # Use 7th house for harmony in relationships
        seventh_house = next(h for h in houses_data if h.HouseNr == 7)
        return (
            f"🎵 Harmony Prediction: Your 7th house, representing marriage and relationships, is in {seventh_house.Rasi}. "
            f"Ruled by {seventh_house.RasiLord}, the planet of love and balance, this suggests a harmonious relationship period. "
            f"The Nakshatra in this house is {seventh_house.Nakshatra}, ruled by {seventh_house.NakshatraLord}, "
            f"indicating peaceful and loving connections with your partner. "
            f"With {seventh_house.SubLord} as the Sub-lord, this is a great time for building or enhancing harmony in your relationships."
        )

    return "Category not recognized. Please enter a valid category."



def chatbot():
    print("Welcome to the Vedic Astrology Chatbot!")
    print("""You can ask about your Marriage Family Friends Health Spirituality Education Travel Children 
        Personal Growth Success Mental Well-being Social Life Harmony.""")
    
    user_input = input("What would you like to know about? ").strip()
    
    # Get horoscope data
    horoscope_data = get_horoscope_data()
    
    print(horoscope_data, "horoscope_data +++")

    # Predict based on user input
    response = predict_category(user_input, horoscope_data)
    
    print(response)

# Run the chatbot
if __name__ == "__main__":
    chatbot()



# from transformers import AutoModelForCausalLM, AutoTokenizer

# model_name = "meta-llama"  # Adjust with the actual model path

# # Load the tokenizer and model
# try:
#     tokenizer = AutoTokenizer.from_pretrained(model_name)
    
#     # Assign padding token if not set
#     if tokenizer.pad_token is None:
#         tokenizer.pad_token = tokenizer.eos_token
    
#     model = AutoModelForCausalLM.from_pretrained(model_name)
#     model.generation_config.pad_token_id = tokenizer.pad_token_id
#     print("Model loaded successfully.")
# except Exception as e:
#     print(f"Error loading model: {e}")
#     exit()

# # Input prompt for testing
# prompt = "Write a detailed essay about the importance of friendship."

# try:
#     print("Try block run")
#     # Tokenize input with padding and truncation
#     inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True)
#     input_ids = inputs["input_ids"]
#     attention_mask = inputs["attention_mask"]

#     print("Generate output")
#     # Generate output
#     outputs = model.generate(
#         input_ids=input_ids,
#         attention_mask=attention_mask,
#         max_length=50,
#         num_return_sequences=1,
#         do_sample=True,         # Enable sampling
#         temperature=0.6,        # Adjust creativity level
#         top_p=0.9               # Enable nucleus sampling
#     )

#     print("Generate response..")
#     response = tokenizer.decode(outputs[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)
#     print(response)
# except Exception as e:
#     print(f"Error generating response: {e}")
