# San Jose Weather

A Flask page that displays the current temperature and sky conditions in San
Jose, California, using the Open-Meteo forecast API.

Install dependencies and start the app:

```sh
pip install -r requirements.txt
python app.py
```

Open <http://127.0.0.1:5000/> in a browser. The app fetches fresh weather data
from Open-Meteo each time the page is loaded. Visit
<http://127.0.0.1:5000/zip> to look up current weather by US ZIP code.