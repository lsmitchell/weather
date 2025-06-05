import os

import requests
from django.shortcuts import render
from weatherDisplay.forms import ZipForm
from dotenv import load_dotenv

# Create your views here.
base_url = "https://api.weatherapi.com/v1/current.json?q="

def view(request):
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

    return render(request, 'index.html', {'form': form, 'weather': weather_str, 'errors': errors})

def get_weather_string(input_zip):
    full_url = base_url + input_zip + "&key=" + os.getenv("WEATHER_API_KEY")
    response = requests.get(full_url)
    json_response = response.json()
    weather_msg = "Unknown"

    if 'error' in json_response:
        weather_msg = "Error"

    if 'current' in json_response:
        temp_f = json_response['current']['temp_f']
        condition = json_response['current']['condition']['text']
        weather_msg = f"{temp_f} degrees and {condition}"

    return "The weather is : " + weather_msg


