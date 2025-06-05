#Tests the view logic using django testing framework
import responses
from django.test import Client
from django.urls import reverse


def test_get_index_expect_form_only():
    client = Client()
    url = reverse("index_view")
    response = client.get(url)
    body = response.content.decode("utf-8")

    assert response.status_code == 200
    assert "The weather is : " not in body
    assert "Zip Code" in body

@responses.activate
def test_post_index_with_filled_form_expect_weather_string():
    client = Client()

    expected_response = {
        "current": {
            "temp_f": 67,
            "condition": {
                "text": "Partly Cloudy",
            }
        }
    }

    # Adjust the request get
    responses.add(
        responses.GET,
        "https://api.weatherapi.com/v1/current.json",
        json=expected_response,
        status=200,
        content_type='application/json'
    )

    url = reverse("index_view")
    response = client.post(url, { "zip_code": "12345" })
    body = response.content.decode("utf-8")

    assert response.status_code == 200
    assert "The weather is : 67 degrees and Partly Cloudy" in body
    assert "Zip Code" in body

def test_post_index_with_empty_zip_expect_form_error():
    client = Client()

    url = reverse("index_view")
    response = client.post(url, { "zip_code": "" })
    body = response.content.decode("utf-8")

    assert response.status_code == 200
    assert "The weather is" not in body
    assert "Zip Code" in body
    assert "Error: " in body

def test_post_index_with_no_zip_expect_form_error():
    client = Client()

    url = reverse("index_view")
    response = client.post(url, {})
    body = response.content.decode("utf-8")

    assert response.status_code == 200
    assert "The weather is" not in body
    assert "Zip Code" in body
    assert "Error: " in body