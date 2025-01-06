import swisseph as swe
import datetime

# Set the date for which you want to calculate the positions
date = datetime.datetime(2001, 7, 15)  # Example date
jd = swe.julday(date.year, date.month, date.day)  # Julian day for the given date

# Define the planets you are interested in (Sun, Moon, Mars, etc.)
planet_ids = [swe.SUN, swe.MOON, swe.MARS, swe.MERCURY, swe.JUPITER, swe.VENUS, swe.SATURN]

# Function to get the position of planets
def get_planetary_positions(jd):
    positions = {}
    for planet in planet_ids:
        result, *planet_data = swe.calc(jd, planet)  # Get planetary data
        lon = planet_data[0]  # Longitude of the planet
        positions[planet] = lon
    return positions

# Function to check if planets are in conjunction (same longitude)
def is_in_yoga(planet_positions):
    yogas = []
    
    print(f"Planetary Positions on {date.strftime('%Y-%m-%d')}:")
    for planet, pos in planet_positions.items():
        print(f"Planet {planet} Longitude: {pos}")

    # Check for conjunctions (all planets at the same longitude or close)
    tolerance = 10  # Degree tolerance for conjunction (can adjust as needed)
    planet_lonitudes = list(planet_positions.values())

    # If all planets are within a certain degree tolerance of each other
    if all(abs(lon - planet_lonitudes[0]) <= tolerance for lon in planet_lonitudes):
        yogas.append("Conjunction Yoga")

    # Add more yogas based on other combinations (like trines, squares, etc.)

    return yogas

# Get planetary positions
planet_positions = get_planetary_positions(jd)

# Check for yogas
yogas = is_in_yoga(planet_positions)

if yogas:
    print(f"Yogas on {date.strftime('%Y-%m-%d')}: {yogas}")
else:
    print(f"No yogas found on {date.strftime('%Y-%m-%d')}.")
