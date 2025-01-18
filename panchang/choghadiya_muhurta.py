import requests
from datetime import datetime


API_KEY = "a9a96b0a-fbfb-593b-b0dc-2ca6306964a0"
VEDIC_BASE_API = f"https://api.vedicastroapi.com/v3-json"


def get_current_date_time():
    date = datetime.now().date()
    time = datetime.now().time()

    day, month, year = date.day, date.month, date.year

    hour, minute = time.hour, time.minute
    current_date, current_time = f"{day}/{month}/{year}", f"{hour}:{minute}"

    return current_date, current_time

def get_current_location():
    import geocoder
    # Get the current location using IP
    location = geocoder.ip('me')
    if location.ok:
        return location.latlng  # Returns (latitude, longitude)
    else:
        print("location does not exist...")
        return None

def convert_24_to_12_hour(time_str):
  hour = int(time_str[:2])
  minute = time_str[3:]
  period = "AM"

  if hour >= 12:
    if hour > 12:
      hour -= 12
    period = "PM"

  return f"{hour}:{minute} {period}"

def get_current_muhurat(response):
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
            current_mahurat = get_current_muhurat(response_res)
            return {f"Choghadiya Muhurta => current time is {curr_time_in_12_form} ":current_mahurat}
        else:
            print(f"Failed to fetch horoscope data. Status code: {response_res.status_code}")
            return {}
    except requests.exceptions.RequestException as e:
        print(f"Error while making API call: {e}")
        return {}

print(get_chog_muhurta())