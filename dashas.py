import ephem

def get_planet_positions(date):
    # Use ephem to calculate planetary positions at a given time
    observer = ephem.Observer()
    observer.date = date
    
    # Get the current position of planets (e.g., Sun, Moon, etc.)
    sun = ephem.Sun(observer)
    moon = ephem.Moon(observer)
    venus = ephem.Venus(observer)
    jupiter = ephem.Jupiter(observer)
    
    # Return the longitudes of the planets in degrees
    return sun, moon, venus, jupiter

# Example: get planet positions for today
planet_positions = get_planet_positions("2025-01-07")

# Convert the positions from hours to degrees and print
for planet in planet_positions:
    # Convert from hours (ephem.hlon) to degrees
    longitude_in_degrees = planet.hlon * 15  # 1 hour = 15 degrees
    if planet.name == "Moon":
        moon_longitude = round(longitude_in_degrees,2)
        print(moon_longitude)
