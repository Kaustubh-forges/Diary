from datetime import date, datetime  # Import classes for working with dates and times

# Get the current date and time, then format it as a string: "YYYY-MM-DD HH:MM:SS"
obj = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Split the string into two parts: date and time
split_obj = obj.split()  # split_obj[0] is date, split_obj[1] is time

# Get the current datetime again as a datetime object
now = datetime.now()

# Get the current day of the week as a string, e.g., "Wednesday"
day = now.strftime("%A")
