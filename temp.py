from datetime import datetime

def extract_date_time_variables():
    # Parse the date string into datetime object
    date_obj = datetime.now()
    
    # Extract year, month, day, hour, minute
    year = date_obj.year
    month = date_obj.month
    day = date_obj.day
    hour = date_obj.hour
    minute = date_obj.minute
    
    return year, month, day, hour, minute

# Extract the variables from the string
year, month, day, hour, minute = extract_date_time_variables()

# Print the extracted values
print("Year:", year)
print("Month:", month)
print("Day:", day)
print("Hour:", hour)
print("Minute:", minute)
