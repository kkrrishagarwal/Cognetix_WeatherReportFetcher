import os
import requests

# Get a free key from https://openweathermap.org/api and either paste it below
# or export it as an environment variable:  export OPENWEATHER_API_KEY=your_key
API_KEY = os.environ.get("OPENWEATHER_API_KEY", "YOUR_OPENWEATHERMAP_API_KEY")
PLACEHOLDER_KEY = "YOUR_OPENWEATHERMAP_API_KEY"

# Offline sample data used in DEMO MODE (when no real API key is configured).
# Shaped exactly like the OpenWeatherMap /data/2.5/weather JSON response.
MOCK_DATA = {
    "delhi":     {"name": "Delhi",     "sys": {"country": "IN"}, "main": {"temp": 24.6, "humidity": 48}, "weather": [{"description": "haze"}]},
    "mumbai":    {"name": "Mumbai",    "sys": {"country": "IN"}, "main": {"temp": 31.2, "humidity": 66}, "weather": [{"description": "partly cloudy"}]},
    "bengaluru": {"name": "Bengaluru", "sys": {"country": "IN"}, "main": {"temp": 22.8, "humidity": 71}, "weather": [{"description": "light rain"}]},
    "kolkata":   {"name": "Kolkata",   "sys": {"country": "IN"}, "main": {"temp": 27.9, "humidity": 74}, "weather": [{"description": "mist"}]},
    "chennai":   {"name": "Chennai",   "sys": {"country": "IN"}, "main": {"temp": 29.4, "humidity": 79}, "weather": [{"description": "scattered clouds"}]},
    "jaipur":    {"name": "Jaipur",    "sys": {"country": "IN"}, "main": {"temp": 23.1, "humidity": 35}, "weather": [{"description": "clear sky"}]},
}


def is_demo_mode():
    return not API_KEY or API_KEY == PLACEHOLDER_KEY


def print_report(data, demo=False):
    city_name = data["name"]
    country = data["sys"]["country"]
    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    condition = data["weather"][0]["description"].capitalize()

    print("\n" + "=" * 40)
    print(f" WEATHER REPORT ---- {city_name} ({country})")
    if demo:
        print(" (demo data - no API key configured)")
    print("=" * 40)
    print(f" Temperature : {temp}°C")
    print(f" Humidity    : {humidity}%")
    print(f" Condition   : {condition}")
    print("=" * 40)


def fetch_weather(city):
    if is_demo_mode():
        data = MOCK_DATA.get(city.strip().lower())
        if data:
            print_report(data, demo=True)
        else:
            print(f"❌ Demo mode: no sample data for '{city}'. "
                  f"Available: {', '.join(d['name'] for d in MOCK_DATA.values())}")
        return

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            print_report(response.json())
        elif response.status_code == 401:
            print("❌ Error: Invalid API key. Check your OpenWeatherMap key.")
        elif response.status_code == 404:
            print("❌ Error: City not found. Please check spelling.")
        else:
            print(f"❌ API Error: Status code {response.status_code}")
    except requests.RequestException as e:
        print(f"❌ Network Error: {e}")


def main():
    print("==========================================")
    print("      WEATHER REPORT FETCHER (API)        ")
    print("==========================================")
    if is_demo_mode():
        print("ℹ️  No API key found - running in DEMO MODE with sample data.")
    while True:
        try:
            city = input("\nEnter city name (or 'exit' to quit): ").strip()
        except EOFError:
            break
        if not city or city.lower() == "exit":
            break
        fetch_weather(city)
    print("\nThank you for using Weather Report Fetcher. Goodbye!")


if __name__ == "__main__":
    main()
