from vedicastro import VedicAstro
from geopy.geocoders import Nominatim

utc = 5.5 
ayanamsa = "Lahiri"
house_system = "Placidus"

def get_lat_long(location_name):
    geolocator = Nominatim(user_agent="geopy_example", timeout=10)
    location = geolocator.geocode(location_name)

    if location:
        latitude, longitude = location.latitude, location.longitude
        return latitude, longitude
    else:
        return 28.7041, 77.1025

def get_horoscope_data(year, month, day, hour, minute, birth_place):
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
    return formatted_planets_data

# Example call
print(get_horoscope_data("1992", "1", "2", "6", "40", "Delhi"))
