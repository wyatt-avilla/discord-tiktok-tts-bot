import requests
import json

def request_tts_conversion(input_text, chosen_voice): # requests for base64 audio conversion of argument
    ENDPOINT = "https://tiktok-tts.weilnet.workers.dev"

    url = f"{ENDPOINT}/api/generation"
    headers = {'Content-Type': 'application/json'}
    data = {'text': input_text, 'voice': chosen_voice}

    response = (requests.post(url, headers=headers, data=json.dumps(data))).json()

    if response["success"] == True:
        return ("data:audio/mpeg;base64," + response["data"])
    else: 
        return "./error-responses/conversion-error.mp3"