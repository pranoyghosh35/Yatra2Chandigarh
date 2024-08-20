import pytz
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def determine_season(month):
    if month in ["April", "May", "June"]:
        return "Summer"
    elif month in ["July", "August", "September"]:
        return "Monsoon"
    else:
        return "Winter"

# Add a suitable weather emoji
weather_tags = {
    "sunny": "☀️",
    "clear sky":"🌌",
    "cloudy": "☁️",
    "fog": "🌫️",
    "raining": "🌧️",
    "hail": "🌨️"
}
        
def get_weather_tag(description):
    description = description.lower()
    if "clear" in description:
        return "clear sky", weather_tags["clear sky"]
    elif "sun" in description:
        return "sunny", weather_tags["sunny"]
    elif "cloud" in description:
        return "cloudy", weather_tags["cloudy"]
    elif "fog" in description:
        return "fog", weather_tags["fog"]
    elif "rain" in description:
        return "raining", weather_tags["raining"]
    elif "hail" in description or "snow" in description:
        return "hail", weather_tags["hail"]
    else:
        return "unknown", ""

# Function to get current weather and forecast for 12 hours around the current time
def get_weather_and_forecast(city="Chandigarh", api_key=WEATHER_KEY):
    base_url = "http://api.openweathermap.org/data/2.5/"
    
    # Get current weather
    weather_url = f"{base_url}weather?q={city}&appid={api_key}&units=metric"
    weather_response = requests.get(weather_url)
    current_weather = weather_response.json()

    # Get forecast for the next 5 days, with data every 3 hours
    forecast_url = f"{base_url}forecast?q={city}&appid={api_key}&units=metric"
    forecast_response = requests.get(forecast_url)
    forecast_data = forecast_response.json()

    # Extract relevant times and weather data
    current_time = datetime.utcnow()
    forecast_results = []

    for entry in forecast_data['list']:
        forecast_time = datetime.utcfromtimestamp(entry['dt'])

        # Check if the forecast time is within 6 hours before or after the current time
        if current_time - timedelta(hours=3) <= forecast_time <= current_time + timedelta(hours=3):
            forecast_results.append({
                "time": forecast_time.strftime('%Y-%m-%d %H:%M:%S'),
                "temperature": entry['main']['temp'],
                "weather": entry['weather'][0]['description']
            })

    # Tag the current weather
    weather_description = current_weather['weather'][0]['description']
    weather_tag, weather_icon = get_weather_tag(weather_description)

    return {
        "current_weather": {
            "temperature": current_weather['main']['temp'],
            "weather": weather_description,
            "tag": weather_tag,
            "icon": weather_icon
        },
        "forecast": forecast_results
    }

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
    weather_data = get_weather_and_forecast()  # Example weather condition
    curr_weather_short=dict(weather_data['current_weather']).get('weather')+dict(weather_data['current_weather']).get('icon')

    # Determine the season based on the month
    season = determine_season(month)
    
    # Return all system information as a dictionary
    return {
        "date": date,
        "month": month,
        "weather": curr_weather_short,
        "season": season,
        "current_time": current_time,
        "weather_details": weather_data
    }
