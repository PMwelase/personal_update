import openmeteo_requests
import requests_cache
from retry_requests import retry
import json

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Weather variables are listed here
url = "https://api.open-meteo.com/v1/forecast"
dbn_params = {
	"latitude": -29.858681,
	"longitude": 31.021839,
	"hourly": ["temperature_2m", "apparent_temperature", "precipitation", "weather_code"],
	"forecast_days": 1
}

weather_codes = {
    "codes": {
        "0":"clear sky",
        "1": "mainly clear",
        "2": "partly cloudy",
        "3": "overcast",
        "45": "fog",
        "48": "depositing rime fog",
        "51": "light drizzle",
        "52": "drizzle",
        "55": "dense drizzle",
        "80": "slight rain showers",
        "81": "rain showers",
        "82": "heavy rain",
        "95": "slight thunderstorm",
        "96": "thunderstorm with hail"
    }
}

dbn_responses = openmeteo.weather_api(url, params=dbn_params)
dbn_response = dbn_responses[0]


def hourly_weather(hour):
    hourly = dbn_response.Hourly()
        
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_precipitation = hourly.Variables(2).ValuesAsNumpy()
    hourly_weather_code = hourly.Variables(3).ValuesAsNumpy()
    
    temp = hourly_temperature_2m[hour]
    precipitation =hourly_precipitation[hour]
    weather_code = int(hourly_weather_code[hour])

    weather_description = weather_codes["codes"][str(int(weather_code))]
    
    will_rain = False
    for n in range(8, 16):
        if hourly_precipitation[n] > 0:
            will_rain = True
            break
    
    if precipitation == 0.0:
        precipitation = "no"
    else:
        precipitation = f"{round(precipitation)}%"
        
    return f"Weather at {hour}:00: {round(temp)}°, {weather_description}.", will_rain

if __name__ == '__main__':
    print(hourly_weather(8)[0])
    print(hourly_weather(12)[0])
    print(hourly_weather(16)[0])
    print(hourly_weather(16)[1])