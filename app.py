from flask import Flask, render_template, request
import requests

app = Flask(__name__)

FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
ZIP_LOOKUP_URL = "https://api.zippopotam.us/us"
SAN_JOSE = {"latitude": 37.3382, "longitude": -121.8863}

WEATHER_DESCRIPTIONS = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snow fall",
    73: "Moderate snow fall",
    75: "Heavy snow fall",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}


def get_current_weather(latitude, longitude, timezone):
    response = requests.get(
        FORECAST_URL,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,weather_code",
            "temperature_unit": "fahrenheit",
            "timezone": timezone,
        },
        timeout=10,
    )
    response.raise_for_status()
    current = response.json()["current"]
    return current["temperature_2m"], WEATHER_DESCRIPTIONS.get(
        current["weather_code"], "Unknown conditions"
    )


@app.get("/")
def index():
    temperature, description = get_current_weather(
        SAN_JOSE["latitude"], SAN_JOSE["longitude"], "America/Los_Angeles"
    )
    return render_template(
        "index.html",
        temperature=temperature,
        description=description,
    )


@app.route("/zip", methods=["GET", "POST"])
def zip_weather():
    zip_code = ""
    error = None
    weather = None
    place_name = None

    if request.method == "POST":
        zip_code = request.form.get("zip_code", "").strip()
        if not (zip_code.isascii() and zip_code.isdigit() and len(zip_code) == 5):
            error = "Enter a valid 5-digit US ZIP code."
        else:
            response = requests.get(f"{ZIP_LOOKUP_URL}/{zip_code}", timeout=10)
            if response.status_code == 404:
                error = f"No US ZIP code {zip_code} was found."
            else:
                response.raise_for_status()
                place = response.json()["places"][0]
                place_name = place["place name"]
                temperature, description = get_current_weather(
                    place["latitude"], place["longitude"], "auto"
                )
                weather = {"temperature": temperature, "description": description}

    return render_template(
        "zip.html",
        zip_code=zip_code,
        error=error,
        place_name=place_name,
        weather=weather,
    )


if __name__ == "__main__":
    app.run()
