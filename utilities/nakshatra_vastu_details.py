import requests
from datetime import datetime


API_KEY = "a9a96b0a-fbfb-593b-b0dc-2ca6306964a0"
VEDIC_BASE_API = f"https://api.vedicastroapi.com/v3-json"


def get_nakshatra_vastu_details(nakshatra_no):
    nakshatra_no = nakshatra_no
    tz = 5.5
    lang = "en"
    api_rise_entity = "utilities/nakshatra-vastu-details"

    try:
        response = requests.get(f"{VEDIC_BASE_API}/{api_rise_entity}?nakshatra={nakshatra_no}&lang={lang}&api_key={API_KEY}")

        print(response)
        if response.status_code == 200:

            response_json = response.json()
            response_res = response_json.get("response", [])

            print(response_res, "response_res")
            
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

print(get_nakshatra_vastu_details("1"))