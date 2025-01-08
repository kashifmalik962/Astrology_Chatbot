# # transliteration_dict = {}

# # with open("Hindi - Word Transliteration Pairs 1.txt", "r") as file:
# #     for line in file:
# #         # Strip any leading/trailing whitespace characters from the line
# #         line = line.strip()
# #         words = line.split()
# #         # print(line)
# #         if len(words) == 2:  # Ensure the line contains exactly two words
# #             transliterated_word = words[0]
# #             hindi_word = words[1]
            
# #             # Add the pair to the dictionary
# #             transliteration_dict[hindi_word] = transliterated_word


# # txt = "यदि आप विशेष रूप से मशीन लर्निंग का उपयोग करके हिंदी पाठ को हिंग्लिश में अनुवाद करना चाहते हैं, तो आपको या तो mBART जैसे बहुभाषी मॉडल का उपयोग करना होगा और इसे हिंग्लिश कॉर्पस पर ठीक करना होगा या ट्रांसफॉर्मर-आधारित मॉडल का लाभ उठाना होगा जो आपको भाषाओं को मिलाने के लिए अनुकूलित टोकनाइजेशन रणनीतियों को लागू करने की अनुमति देता है।"

# # translate_hing = []

# # for word in txt.split():
# #     if word in transliteration_dict.keys():
# #         translate_hing.append(transliteration_dict[word])

# # translate_hing = " ".join(translate_hing)
# # print(translate_hing)



# from indic_transliteration import sanscript
# from indic_transliteration.sanscript import transliterate

# impove_roman_word_dict = {"apa":"aap", "himdi": "hindi", "himglisha": "hinglish", "mem":"me", "haim|":"hain", "haim,":"hain","anuvada":"anuvaad", "vishesha":"vishesh","rupa":'roop', "mashina":"machine", "larnimga":"learning", "upayoga":"upyog", "apako":"aapko", "maॉdala":"model", "aura":"aur","para":"par", "thika":"thik",
#                "tramsaphaॉrmara":"transformer","adharita":"aadharit", "labha":"labh", "anukulita":"anukulit", "hai|":"hai", "eka":"ek", "majabuta":"majbut", "upakarana":"upkaaran","dizaina":"design","yaha.n":"yahan", "isaka":"iska"}

# fresh_words = []

# # Input text in Hindi
# hindi_text = "यह एक मजबूत उपकरण है जिसे विशेष रूप से भारतीय भाषाओं के लिए लिप्यंतरण को संभालने के लिए डिज़ाइन किया गया है। यदि आपकी समस्या हिंदी को हिंग्लिश में बदलने से संबंधित है, तो यह उपकरण अत्यधिक प्रभावी हो सकता है। यहाँ बताया गया है कि आप इसका उपयोग कैसे कर सकते हैं और इसे अपनी आवश्यकताओं के अनुसार कैसे अनुकूलित कर सकते हैं"

# # Convert Hindi (Devanagari) to Hinglish (ITRANS)
# hinglish_text = transliterate(hindi_text, sanscript.DEVANAGARI, sanscript.ITRANS)

# for word in hinglish_text.lower().split():
#     if word in impove_roman_word_dict.keys():
#         fresh_words.append(impove_roman_word_dict[word])
#     else:
#         fresh_words.append(word)


# fresh_word_str = " ".join(fresh_words)

# print("Hinglish Text:", fresh_word_str)



from deep_translator import GoogleTranslator
import spacy
from concurrent.futures import ThreadPoolExecutor

nlp = spacy.load("en_core_web_sm")

# Translator with caching
translator_cache = {}

def translate_with_cache(text):
    if text not in translator_cache:
        translator_cache[text] = GoogleTranslator(source='auto', target='hi').translate(text)
    return translator_cache[text]

def translate_batch(texts):
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(translate_with_cache, texts))
    return dict(zip(texts, results))

def hinglishConverter(english):
    doc = nlp(english)
    english_nouns = {token.text for token in doc if token.pos_ == "NOUN"}

    # Prepare batch for translation
    batch = [english] + list(english_nouns)

    # Translate in parallel
    translations = translate_batch(batch)

    # Replace translated nouns with their original English form
    hinglish = translations[english]
    for noun in english_nouns:
        hinglish = hinglish.replace(translations[noun], noun)

    return hinglish


# Test the function
english = """On July 18, 1953, Presley first went to the Memphis Recording Service at the Sun Record Company, now commonly known as Sun Studio.[2] He paid $3.98 to record the first of two double-sided demo acetates, "My Happiness" and "That's When Your Heartaches Begin"."""
hinglish = hinglishConverter(english)
print("Hinglish translation:", hinglish)
