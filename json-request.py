import requests
import json

def request_tts_conversion(input_text): # requests for base64 audio conversion of argument
    voice = "en_us_001"                 # girl voice
    ENDPOINT = "https://tiktok-tts.weilnet.workers.dev"

    url = f"{ENDPOINT}/api/generation"
    headers = {'Content-Type': 'application/json'}
    data = {'text': input_text, 'voice': voice}

    response = (requests.post(url, headers=headers, data=json.dumps(data))).json()

    return ("data:audio/mpeg;base64," + response["data"])