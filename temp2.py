# from langdetect import detect

# print(detect("Geeksforgeeks is a computer science portal for geeks"))
# print(detect("Geeksforgeeks - это компьютерный портал для гиков"))
# print(detect("Geeksforgeeks es un portal informático para geeks"))
# print(detect("Geeksforgeeks是面向极客的计算机科学门户"))
# print(detect("Geeksforgeeks geeks के लिए एक कंप्यूटर विज्ञान पोर्टल है"))
# print(detect("Geeksforgeeksは、ギーク向けのコンピューターサイエンスポータルです。"))
# print(detect("विज्ञान"))


# from googletrans import Translator

# translator = Translator()
# translation = translator.translate("Geeksforgeeks is a computer science portal for geeks", src='en', dest='hi')
# print(translation.text)


# from geopy.geocoders import Nominatim

# # Initialize Nominatim API
# geolocator = Nominatim(user_agent="Geopy Library")

# location = geolocator.geocode("nakur")

# print("The latitude of the location is: ", location.latitude)
# print("The longitude of the location is: ", location.longitude)



# from geopy.geocoders import Nominatim

# def get_lat_long(location_name):
#     geolocator = Nominatim(user_agent="geopy_example",timeout=10)
#     location = geolocator.geocode(location_name)

#     if location:
#         latitude, longitude = location.latitude, location.longitude
#         return latitude, longitude
#     else:
#         return None
    
    
# print(get_lat_long("khalilabad,uttar pradesh"))



# from indic_transliteration import sanscript

# def hindi_to_roman(hindi_text):
#     # Transliterate from Devanagari (Hindi) to Roman
#     roman_text = sanscript.transliterate(hindi_text, sanscript.DEVANAGARI, sanscript.ITRANS)
#     return roman_text.lower()

# # Example usage
# hindi_text = "हिन्दी में अनुच्छेद लेखन, किसी विषय को संक्षेप में विस्तार से बताने का एक अहम तरीका है. अनुच्छेद लेखन के ज़रिए, विचारों को स्पष्ट और संगठित तरीके से प्रस्तुत किया जा सकता है. अनुच्छेद लेखन के बारे में ज़्यादा जानकारीः"
# roman_text = hindi_to_roman(hindi_text)
# print(roman_text)



# from langdetect import detect

# def detect_hinglish(text):
#     hindi_words = ["mera", "kis", "hai", "kaise", "tum"]  # Add more transliterated Hindi words
#     if any(word in text.lower() for word in hindi_words):
#         return "Hinglish"
#     else:
#         return detect(text)

# text = "हिन्दी में अनुच्छेद लेखन, किसी विषय को संक्षेप में विस्तार से बताने का एक अहम तरीका है. अनुच्छेद लेखन के ज़रिए, विचारों को स्पष्ट और संगठित तरीके से प्रस्तुत किया जा सकता है. अनुच्छेद लेखन के बारे में ज़्यादा जानकारीः"
# language = detect_hinglish(text)
# print(f"Detected language: {language}")


# from transformers import AutoTokenizer, pipeline
# import transformers
# import torch

# model = "meta-llama/Llama-3.2-3B-Instruct" # meta-llama/Llama-2-7b-hf

# tokenizer = AutoTokenizer.from_pretrained(model, use_auth_token=True)

# # Set pad_token_id explicitly to eos_token_id
# if tokenizer.pad_token_id is None:
#     tokenizer.pad_token_id = tokenizer.eos_token_id

# llama_pipeline = pipeline(
#     "text-generation",  # LLM task
#     model=model,
#     torch_dtype=torch.float16,
#     device_map="auto",
# )


# def get_llama_response(prompt: str) -> None:
#     """
#     Generate a response from the Llama model.

#     Parameters:
#         prompt (str): The user's input/question for the model.

#     Returns:
#         None: Prints the model's response.
#     """
#     sequences = llama_pipeline(
#         prompt,
#         do_sample=True,
#         top_k=10,
#         num_return_sequences=1,
#         eos_token_id=tokenizer.eos_token_id,
#         truncation=True,
#         max_length=256,
#     )
#     print("Chatbot:", sequences[0]['generated_text'])


# prompt = 'Act as astrologer this is my birth detain, year = 1992, month = 1,day = 2, hour = 6,minute = 40, birth_place=Delhi, where my jupyter is placed. based on my kundli give answer in 30 to 40 words only\n'
# get_llama_response(prompt)




# from langchain_ollama import OllamaLLM
# from langchain.prompts import ChatPromptTemplate

# template = """
#     Answer the question below:
    
#     here the conv history: {context}
    
#     Question: {question}
    
#     Answer: 
# """

# model = OllamaLLM(model="llama3.2")
# prompt = ChatPromptTemplate.from_template(template)


# chain = prompt | model

# result = chain.invoke({"context":"", "question":" Act as astrologer this is my birth detain, year = 2001, month = 7,day = 15, hour = 21,minute = 5, birth_place=khalilabad uttar pradesh which year when i get my first job based on my kundli give answer in 30 to 40 words only"})

# print(result)




# from transformers import AutoModelForCausalLM, AutoTokenizer
# from safetensors import safe_open

# # Set paths for model and tokenizer
# # model_path = r"meta-llama\model-00002-of-00002.safetensors"
# tokenizer_path = r"meta-llama\tokenizer.json"

# model_dir = r"meta-llama"  # Path to the directory containing your model and configuration
# model = AutoModelForCausalLM.from_pretrained(model_dir, trust_remote_code=True)
# tokenizer = AutoTokenizer.from_pretrained(model_dir, use_fast=False)

# # Encode input text and generate response
# inputs = tokenizer("Act as an astrologer. This is my birth detail: year = 2001, month = 7, day = 15, hour = 21, minute = 5, birth_place = Khalilabad, Uttar Pradesh. When will I get my first job based on my kundli? Answer in 30 to 40 words only.", return_tensors="pt",padding=True,truncation=True)
# outputs = model.generate(inputs['input_ids'], max_length=256, temperature=0.01,pad_token_id=tokenizer.pad_token_id, eos_token_id=tokenizer.eos_token_id)

# # Decode and print the output
# response = tokenizer.decode(outputs[0], skip_special_tokens=True)
# print(response)



from transformers import LlamaForCausalLM, LlamaTokenizer
from peft import LoraConfig, get_peft_model
import bitsandbytes as bnb  # For quantization support

# Load the pretrained LLaMA model
model_name = "meta-llama"  # Replace with your model path
model = LlamaForCausalLM.from_pretrained(model_name, low_cpu_mem_usage=True)

# Set QLoRA configuration (quantization + adapter layers)
lora_config = LoraConfig(r=8, lora_alpha=32, lora_dropout=0.1)
model = get_peft_model(model, lora_config)

# Apply quantization using bitsandbytes
model = bnb.nn.Int8Params(model)  # Use bitsandbytes to apply int8 quantization

# Save the fine-tuned model
model.save_pretrained("data")
