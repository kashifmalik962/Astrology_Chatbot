import requests
from datetime import datetime


API_KEY = "a9a96b0a-fbfb-593b-b0dc-2ca6306964a0"
VEDIC_BASE_API = f"https://api.vedicastroapi.com/v3-json"


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
    
    
print(get_numerology(2001, 7, 15))