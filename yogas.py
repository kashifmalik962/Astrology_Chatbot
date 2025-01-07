import ephem

def get_yoga_and_karana(date):
    # Use ephem to calculate planetary positions at a given time
    observer = ephem.Observer()
    observer.date = date
    
    # Get the positions of the Sun and Moon
    sun = ephem.Sun(observer)
    moon = ephem.Moon(observer)
    
    # Calculate the angular distance between Sun and Moon in degrees
    angle_between_sun_moon = abs(sun.hlon - moon.hlon)
    
    # Ensure the angle is within 0 to 180 degrees
    if angle_between_sun_moon > 180:
        angle_between_sun_moon = 360 - angle_between_sun_moon
    
    # 1 Yoga = 13.33° (360° / 27)
    yoga_index = int(angle_between_sun_moon // 13.33)
    
    # 1 Karana = 25.71° (360° / 14)
    karana_index = int(angle_between_sun_moon // 25.71)
    
    # List of Yoga names (27 Yogas)
    yogas = [
        "Vishkumbh", "Priti", "Ayushman", "Sowbhagya", "Shobhana", "Atiganda", "Sukarma",
        "Dhriti", "Shoola", "Gand", "Vridhi", "Dhruva", "Vyagha", "Harshana", "Vajra",
        "Siddhi", "Vyatipata", "Variyana", "Parigha", "Shiva", "Sandhi", "Brahma", "Indra",
        "Vaidhriti", "Vishkumbh", "Priti", "Ayushman", "Sowbhagya"
    ]
    
    # List of Karana names (11 Karanas)
    karanas = ["Bava", "Balava", "Kaulava", "Taitila", "Garija", "Vaidhrti", "Shakuni", 
               "Chatushpada", "Naga", "Kimstughna", "Shakuni"]

    # Yoga and Karana based on the index
    yoga = yogas[yoga_index % len(yogas)]  # Ensure it's within 27
    karana = karanas[karana_index % len(karanas)]  # Ensure it's within 11
    
    return yoga, karana

# Example usage
date = "2025-01-07"
yoga, karana = get_yoga_and_karana(date)
print(f"Yoga: {yoga}")
print(f"Karana: {karana}")
