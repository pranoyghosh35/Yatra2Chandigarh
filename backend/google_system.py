import pytz
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def determine_season(month):
    if month in ["April", "May", "June"]:
        return "Summer"
    elif month in ["July", "August", "September"]:
        return "Monsoon"
    else:
        return "Winter"

def get_system_info():
    # Define the IST timezone
    ist = pytz.timezone('Asia/Kolkata')
    
    # Fetch date and time in UTC and convert to IST
    now = datetime.now(pytz.utc)
    now_ist = now.astimezone(ist)
    
    date = now_ist.strftime("%A %d %B, %Y")
    month = now_ist.strftime("%B")
    current_time = now_ist.strftime("%I:%M %p")

    # Determine weather (placeholder, can be integrated with live API)
    weather = "sunny"  # Example weather condition

    # Determine the season based on the month
    season = determine_season(month)
    
    # Return all system information as a dictionary
    return {
        "date": date,
        "month": month,
        "weather": weather,
        "season": season,
        "current_time": current_time
    }
