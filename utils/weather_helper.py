import requests
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file (if it exists)
load_dotenv()

def get_weather_data(location):
    """
    Fetch weather data from OpenWeatherMap API
    """
    try:
        api_key = os.getenv("OPENWEATHER_API_KEY", "default_key")
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        
        params = {
            'q': location,
            'appid': api_key,
            'units': 'metric'  # Celsius
        }
        
        response = requests.get(base_url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            weather_info = {
                'temperature': round(data['main']['temp']),
                'feels_like': round(data['main']['feels_like']),
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'description': data['weather'][0]['description'].title(),
                'wind_speed': round(data['wind']['speed'] * 3.6, 1),  # Convert m/s to km/h
                'visibility': data.get('visibility', 0) / 1000,  # Convert to km
                'cloud_cover': data['clouds']['all'],
                'sunrise': datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M'),
                'sunset': datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M'),
            }
            
            # Check if rainfall data is available
            if 'rain' in data:
                weather_info['rainfall'] = data['rain'].get('1h', 0)  # Last 1 hour
            else:
                weather_info['rainfall'] = 0
                
            return weather_info
            
        else:
            return None
            
    except requests.exceptions.Timeout:
        raise Exception("Weather service timeout. Please try again.")
    except requests.exceptions.ConnectionError:
        raise Exception("Unable to connect to weather service. Check internet connection.")
    except Exception as e:
        raise Exception(f"Error fetching weather data: {str(e)}")

def get_weather_forecast(location, days=5):
    """
    Get weather forecast for specified number of days
    """
    try:
        api_key = os.getenv("OPENWEATHER_API_KEY", "default_key")
        base_url = "http://api.openweathermap.org/data/2.5/forecast"
        
        params = {
            'q': location,
            'appid': api_key,
            'units': 'metric',
            'cnt': days * 8  # 8 forecasts per day (every 3 hours)
        }
        
        response = requests.get(base_url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            forecast = []
            
            for item in data['list']:
                forecast_item = {
                    'datetime': datetime.fromtimestamp(item['dt']),
                    'temperature': round(item['main']['temp']),
                    'humidity': item['main']['humidity'],
                    'description': item['weather'][0]['description'].title(),
                    'wind_speed': round(item['wind']['speed'] * 3.6, 1),
                    'rainfall': item.get('rain', {}).get('3h', 0)
                }
                forecast.append(forecast_item)
            
            return forecast
        else:
            return None
            
    except Exception as e:
        raise Exception(f"Error fetching weather forecast: {str(e)}")

def get_farming_weather_advisory(weather_data):
    """
    Generate farming advisory based on weather conditions
    """
    advisories = []
    
    if weather_data['temperature'] > 35:
        advisories.append("🌡️ High temperature detected. Increase irrigation frequency and provide shade for sensitive crops.")
    
    if weather_data['temperature'] < 10:
        advisories.append("🥶 Low temperature warning. Protect crops from frost damage.")
    
    if weather_data['humidity'] > 85:
        advisories.append("💧 High humidity levels. Monitor for fungal diseases and improve air circulation.")
    
    if weather_data['humidity'] < 30:
        advisories.append("🏜️ Low humidity. Increase irrigation and consider mulching.")
    
    if weather_data['rainfall'] > 50:
        advisories.append("🌧️ Heavy rainfall expected. Ensure proper drainage and harvest ready crops.")
    
    if weather_data['wind_speed'] > 25:
        advisories.append("💨 Strong winds expected. Secure tall crops and protect seedlings.")
    
    if not advisories:
        advisories.append("🌱 Weather conditions are favorable for normal farming activities.")
    
    return advisories
