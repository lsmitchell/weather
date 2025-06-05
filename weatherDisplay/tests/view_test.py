# Tests the view logic using pytest basic testing
from django.http import HttpRequest

from weatherDisplay.views import view


def test_view_when_request_get_expect_no_weather_string():
    request = HttpRequest()
    request.method = "GET"

    http_response = view(request)
    body = http_response.text
    assert "The weather is : " not in body
    assert "Zip Code" in body
