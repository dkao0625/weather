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

Run the test suite with:

```sh
python -m unittest discover
```

The GitHub Actions workflow runs the tests for pull requests and pushes to
`main`. A successful `main` run deploys the app to Cloud Run. Configure these
repository Actions secrets before enabling deployment:

- `GCP_PROJECT_ID`
- `GCP_WORKLOAD_IDENTITY_PROVIDER`
- `GCP_SERVICE_ACCOUNT`

The workload identity provider should trust only the
`dkao0625/weather` GitHub repository, and its service account needs permission
to build and deploy Cloud Run services.