import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("FIRST_API_KEY")
api_url = os.getenv("FIRST_API_URL")
word = "love"
api_url = f"{api_url}?word={word}"
response = requests.get(api_url, headers={"X-Api-Key": api_key})
if response.status_code == requests.codes.ok:
    print(response.__dict__)
else:
    print("Error:", response.status_code, response.text)
