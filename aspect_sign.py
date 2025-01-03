# import swisseph as swe
# import datetime

# # Function to calculate the Ascendant and Zodiac sign
# def get_ascendant_and_zodiac(date_of_birth, latitude, longitude):
#     # Convert birthdate to Julian Date
#     birthdate = datetime.datetime.strptime(date_of_birth, "%Y-%m-%d %H:%M:%S")
#     jd_ut = swe.julday(birthdate.year, birthdate.month, birthdate.day,
#                        birthdate.hour + birthdate.minute / 60 + birthdate.second / 3600)
    
#     # Convert latitude and longitude to float
#     latitude = float(latitude)
#     longitude = float(longitude)
    
#     # Calculate the Ascendant and Zodiac Sign
#     houses, _ = swe.houses(jd_ut, latitude, longitude, b'A')  # Placidus system
#     ascendant = houses[0]  # Ascendant is the first element
#     zodiac_sign = get_zodiac_sign(ascendant)
    
#     return ascendant, zodiac_sign, jd_ut

# # Function to determine the Zodiac Sign from Ascendant
# def get_zodiac_sign(ascendant):
#     zodiac_signs = [
#         "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
#         "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
#     ]
#     return zodiac_signs[int(ascendant // 30)]

# # Function to determine Nakshatra from the Moon's position
# def get_nakshatra(jd_ut):
#     moon_pos = swe.calc_ut(jd_ut, swe.MOON)[0][0]  # Get the position of the Moon
#     nakshatras = [
#         "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
#         "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purvaphalguni", "Uttara Phalguni",
#         "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
#         "Mula", "Purvashada", "Uttara Ashada", "Shravana", "Dhanishta",
#         "Shatabhisha", "Purvabhadrapada", "Uttara Bhadrapada", "Revati"
#     ]
#     nakshatra_index = int((moon_pos % 30) / 13.3333)  # Calculate Nakshatra index
#     return nakshatras[nakshatra_index]

# # Function to dynamically generate Kundli details
# def get_dynamic_kundli_details(ascendant, nakshatra, zodiac_sign):
#     kundli = {
#         "Ascendant Sign": get_zodiac_sign(ascendant),
#         "Nakshatra": nakshatra,
#     }

#     # Dynamic Gana based on Nakshatra
#     if nakshatra in ["Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira"]:
#         kundli["Gana"] = "Deva Gana"
#     elif nakshatra in ["Ardra", "Punarvasu", "Pushya", "Ashlesha", "Magha"]:
#         kundli["Gana"] = "Manushya Gana"
#     else:
#         kundli["Gana"] = "Rakshasa Gana"
    
#     # Dynamic Yoni based on Nakshatra
#     if nakshatra in ["Ashwini", "Bharani", "Krittika"]:
#         kundli["Yoni"] = "Horse"
#     elif nakshatra in ["Rohini", "Mrigashira"]:
#         kundli["Yoni"] = "Elephant"
#     else:
#         kundli["Yoni"] = "Cat"

#     # Dynamic Vasya based on Zodiac Sign
#     vasya_map = {
#         "Aries": "Vasu Vasya", "Taurus": "Uttara Vasya", "Gemini": "Tungabhadra Vasya",
#         "Cancer": "Vasu Vasya", "Leo": "Vasu Vasya", "Virgo": "Uttara Vasya",
#         "Libra": "Vasu Vasya", "Scorpio": "Tungabhadra Vasya", "Sagittarius": "Vasu Vasya",
#         "Capricorn": "Uttara Vasya", "Aquarius": "Tungabhadra Vasya", "Pisces": "Vasu Vasya"
#     }
#     kundli["Vasya"] = vasya_map.get(zodiac_sign, "Vasu Vasya")

#     # Dynamic Nadi based on Nakshatra
#     nadi_map = {
#         "Ashwini": "Adi Nadi", "Bharani": "Madhya Nadi", "Krittika": "Antya Nadi",
#         "Rohini": "Adi Nadi", "Mrigashira": "Madhya Nadi", "Ardra": "Antya Nadi"
#     }
#     kundli["Nadi"] = nadi_map.get(nakshatra, "Adi Nadi")

#     # Dynamic Varna based on Zodiac Sign
#     varna_map = {
#         "Aries": "Brahmin", "Taurus": "Kshatriya", "Gemini": "Vaishya", "Cancer": "Shudra",
#         "Leo": "Brahmin", "Virgo": "Kshatriya", "Libra": "Vaishya", "Scorpio": "Shudra",
#         "Sagittarius": "Brahmin", "Capricorn": "Kshatriya", "Aquarius": "Vaishya", "Pisces": "Shudra"
#     }
#     kundli["Varna"] = varna_map.get(zodiac_sign, "Brahmin")

#     # Dynamic Paya based on Nakshatra
#     paya_map = {
#         "Ashwini": "Kshatriya Paya", "Bharani": "Brahmin Paya", "Krittika": "Shudra Paya",
#         "Rohini": "Vaishya Paya", "Mrigashira": "Kshatriya Paya", "Ardra": "Brahmin Paya"
#     }
#     kundli["Paya"] = paya_map.get(nakshatra, "Kshatriya Paya")

#     # Dynamic Tatva based on Ascendant
#     tatva_map = {
#         "Aries": "Fire", "Taurus": "Earth", "Gemini": "Air", "Cancer": "Water",
#         "Leo": "Fire", "Virgo": "Earth", "Libra": "Air", "Scorpio": "Water",
#         "Sagittarius": "Fire", "Capricorn": "Earth", "Aquarius": "Air", "Pisces": "Water"
#     }
#     kundli["Tatva"] = tatva_map.get(zodiac_sign, "Water")

#     # Dynamic Life Stone based on Nakshatra
#     kundli["Life Stone"] = "Pearl"  # Could be calculated dynamically based on Nakshatra

#     # Dynamic Lucky Stone based on Zodiac Sign
#     lucky_stones = {
#         "Aries": "Ruby", "Taurus": "Emerald", "Gemini": "Agate", "Cancer": "Pearl",
#         "Leo": "Ruby", "Virgo": "Sapphire", "Libra": "Opal", "Scorpio": "Garnet",
#         "Sagittarius": "Topaz", "Capricorn": "Garnet", "Aquarius": "Amethyst", "Pisces": "Aquamarine"
#     }
#     kundli["Lucky Stone"] = lucky_stones.get(zodiac_sign, "Moonstone")

#     # Dynamic Fortune Stone based on Nakshatra
#     kundli["Fortune Stone"] = "Emerald"  # Example, could be changed based on Nakshatra

#     # Name Start based on Nakshatra
#     name_start_map = {
#         "Ashwini": ["Ke", "Ko", "Ha", "Hi"], "Bharani": ["La", "Le", "Li", "Lu"],
#         "Krittika": ["A", "E", "U", "I"], "Rohini": ["O", "Vo", "Va", "Ve"]
#     }
#     kundli["Name Start"] = name_start_map.get(nakshatra, ["Ma", "Me", "Mi", "Mu"])

#     return kundli

# # Main function to get user input and display Kundli
# def main():
#     # Example: Get Ascendant and Zodiac Sign from birth details
#     ascendant, zodiac_sign, jd_ut = get_ascendant_and_zodiac("2001-07-15 21:05:00", "26.7658", "83.0834")
    
#     # Get Nakshatra based on Moon's position
#     nakshatra = get_nakshatra(jd_ut)
    
#     # Get dynamic Kundli details based on Nakshatra and Ascendant
#     kundli_details = get_dynamic_kundli_details(ascendant, nakshatra, zodiac_sign)
    
#     # Display the Kundli details
#     print("\nYour Dynamic Kundli Details:")
#     for key, value in kundli_details.items():
#         print(f"{key}: {value}")

# if __name__ == "__main__":
#     main()



def check_user_question_tone():
    match_greeting_words = ["heloo", "hello", "hey", "namaste", "namastee", "hy", "heey" ,"hi", "hii", "hiii"]
    txt = "heloo hello hey namaste namastee hy heey hi hii hiii who"
    # new_txt = txt.split()
    for word in txt.split():
        if word in match_greeting_words:
            print("greetings")
        else:
            print("not greeting")



check_user_question_tone()