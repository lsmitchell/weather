# Weather App

## Overview

A small application to warm up with Python and Django. Calls out to an external weather API (https://api.weatherapi.com) and gets the weather for a specified postal code.

## Setup

The project dependencies are located in the pyproject.toml file.

To run the project, you'll need an API key to call the weatherapi. As of this writing you can get a free API key by signing up at https://www.weatherapi.com/. Once you have an API key, create a `.env` file at the project root and place the following in it:

```WEATHER_API_KEY=<your API key>```

To setup the database (used to save the API responses) run:

```python manage.py makemigrations weatherDisplay```

```python manage.py migrate```

To run the server, run

`python manage.py runserver`

To run the frontend, run

`npm run dev`

Once the server and frontend is started, you can access the main page by going to

```http://localhost:3000/```

## Tests

To run the tests, run

`pytest weatherDisplay/tests/`

The tests use pytest and the django testing framework.