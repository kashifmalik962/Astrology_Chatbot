import requests
from datetime import datetime


API_KEY = "a9a96b0a-fbfb-593b-b0dc-2ca6306964a0"
VEDIC_BASE_API = f"https://api.vedicastroapi.com/v3-json"


def get_gem_details(gem):
    gem = gem
    tz = 5.5
    lang = "en"
    api_rise_entity = "utilities/gem-details"

    try:
        response = requests.get(f"{VEDIC_BASE_API}/{api_rise_entity}?gem={gem}&lang={lang}&api_key={API_KEY}")

        print(response)
        if response.status_code == 200:

            response_json = response.json()
            response_res = response_json.get("response", [])

            print(response_res, "response_res")
            
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

print(get_gem_details("coral"))