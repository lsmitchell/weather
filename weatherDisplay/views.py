import json
import os

import requests
import re
from django.shortcuts import render
from weatherDisplay.forms import ZipForm
from dotenv import load_dotenv

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Weather
from .serializers import WeatherSerializer

# Create your views here.
base_url = "https://api.weatherapi.com/v1/current.json?q="


## Example of using Django views in an MVC style
def view(request):
    ## Load the API key (and other settings) from the .env file (needs to be created locally, see README)
    load_dotenv()
    weather_str = ""
    errors = ""

    ## Capture the form submission
    if request.method == "POST":
        form = ZipForm(request.POST)
        if form.is_valid():
            weather_str = get_weather_string(form.cleaned_data["zip_code"])
        else:
            errors = "Error: " + form.errors.as_text()
    # Else just display the form
    else:
        form = ZipForm()

    return render(request, 'index.html',
                  {'form': form, 'weather': weather_str, 'errors': errors})


def get_weather_string(input_zip):
    json_response = call_weather_api(input_zip)
    weather_msg = "Unknown"

    if 'error' in json_response:
        weather_msg = "Error"

    if 'current' in json_response:
        temp_f = json_response['current']['temp_f']
        condition = json_response['current']['condition']['text']
        weather_msg = f"{temp_f} degrees and {condition}"

    return "The weather is : " + weather_msg


## Example of using Django rest endpoints (called by a frontend rendering technology)

@api_view(['GET', 'POST'])
def get_weather(request):
    """
    Gets the weather (temperature and condition) given a zip code.

    :param request: query param or body should include zip_code, 5 digits numeric
    :return: a json response with the temp_f, condition, and err fields. If successful,
    the temp_f and condition are returned, else the err field is populated with the error
    """
    zip_code = None

    ## Check the input values we need are provided
    if request.method == 'GET':
        if not request.query_params.get('zip_code'):
            return Response('Zip code must be provided.',
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            zip_code = request.query_params.get('zip_code')

    elif request.method == 'POST':
        if not request.data.get('zip_code'):
            return Response('Zip code must be provided.',
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            zip_code = request.data.get('zip_code')

    return get_weather_data_response(zip_code)


def is_valid_zip_code(zip_code):
    """
    Checks if the zip code is 5 digits and numeric-only.

    :param zip_code: the zip code to check
    :return: true if zip code is 5 digits numeric, false otherwise
    """
    zip_string = str(zip_code)
    pattern = r'\d{5}'
    return re.match(pattern, zip_string) is not None


def get_weather_data_response(zip_code):
    """
    Gets the weather data API response for a given zip code.

    :param zip_code: the zip code to check the weather for
    :return: a response with the weather data, or error if it was a bad request
    """

    ## Validate
    if not is_valid_zip_code(zip_code):
        return Response('Zip code must be numeric 5 digits.',
                        status=status.HTTP_400_BAD_REQUEST)

    weather_obj = Weather(err="Non-initialized")

    ## Call the weather api
    json_response = call_weather_api(str(zip_code))

    ## Handle success or failure
    if 'error' in json_response:
        # print("Got error: ", json_response)
        weather_obj.err = json_response.get('error').get('message')
    elif 'current' in json_response:
        temp_f = json_response['current']['temp_f']
        condition = json_response['current']['condition']['text']
        # print("Got success response")
        weather_obj = Weather(temp_f=temp_f, condition=condition)

    ## Saves the response object in the database
    weather_obj.save()
    ## Serialize the response object for the response
    serializer = WeatherSerializer(weather_obj)
    return Response(serializer.data)


def call_weather_api(input_zip):
    """
    Calls the weather api for the given zip to get the temperature and condition.

    :param input_zip: the zip to check the weather for
    :return: the api response as json; if the api key is not set or the input zip is null, returns a json error object (with the same style as the api response error)
    """
    load_dotenv()
    api_key = os.getenv('WEATHER_API_KEY')

    if not api_key:
        return json.loads('{"error": "Weather API key is not set."}')

    if input_zip is None:
        return json.loads('{"error": "Input zip must be non-empty."}')

    full_url = base_url + input_zip + "&key=" + api_key
    response = requests.get(full_url)
    return response.json()
