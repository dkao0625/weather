import unittest
from unittest.mock import patch

import app


class WeatherAppTests(unittest.TestCase):
    def setUp(self):
        app.app.config["TESTING"] = True
        self.client = app.app.test_client()

    @patch("app.get_current_weather", return_value=(72.5, "Clear sky"))
    def test_home_displays_current_weather(self, get_current_weather):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"72.5", response.data)
        self.assertIn(b"Clear sky", response.data)
        get_current_weather.assert_called_once()

    @patch("app.requests.get")
    def test_invalid_zip_does_not_make_external_request(self, get):
        response = self.client.post("/zip", data={"zip_code": "12a"})

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Enter a valid 5-digit US ZIP code.", response.data)
        get.assert_not_called()

    @patch("app.get_current_weather", return_value=(68.0, "Partly cloudy"))
    @patch("app.requests.get")
    def test_valid_zip_displays_weather(self, get, get_current_weather):
        get.return_value.status_code = 200
        get.return_value.json.return_value = {
            "places": [
                {
                    "place name": "San Jose",
                    "latitude": "37.3382",
                    "longitude": "-121.8863",
                }
            ]
        }

        response = self.client.post("/zip", data={"zip_code": "95112"})

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"San Jose", response.data)
        self.assertIn(b"68.0", response.data)
        self.assertIn(b"Partly cloudy", response.data)
        get_current_weather.assert_called_once_with("37.3382", "-121.8863", "auto")

    @patch("app.requests.get")
    def test_unknown_zip_shows_not_found(self, get):
        get.return_value.status_code = 404

        response = self.client.post("/zip", data={"zip_code": "00000"})

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"No US ZIP code 00000 was found.", response.data)
