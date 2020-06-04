import requests


def getData(value):
    """Look up quote for symbol."""

    # Contact API
    try:
        api_key = '4942d893e111cf68b4f2e9acbf544dfc'
        response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={value}&appid={api_key}")
    except requests.RequestException as err:
        return None

    # Parse response
    try:
        quote = response.json()
        return quote
    except (KeyError, TypeError, ValueError):
        return None