import json
import requests

def get_api_key_from_file(filename):
    """Reads an API key from a file."""
    with open(filename, 'r') as file:
        data = json.load(file)
    return data['api_key']

def fetch_data_from_api(api_key, message):
    """Uses the API key to make a GET request to a mock API."""
    url = "https://api.example.com/data"
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(url, headers=headers, params={"message": message})
    return response.json()
    
def process_data_from_file(filename, message):
    """Reads the API key from a file and fetches data from an API."""
    api_key = get_api_key_from_file(filename)
    return fetch_data_from_api(api_key, message)
