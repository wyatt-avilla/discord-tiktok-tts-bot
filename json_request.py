import requests
import json

def request_tts_conversion(input_text, chosen_voice):                                       # input_text and chosen_voice are passed from the /tts command in bot.py

    if len(input_text) > 300:                                                               # ensures appropriate length for HTTP request
        return "./error-responses/length-error.mp3"

    ENDPOINT = "https://tiktok-tts.weilnet.workers.dev"

    url = f"{ENDPOINT}/api/generation"
    headers = {'Content-Type': 'application/json'}
    data = {'text': input_text, 'voice': chosen_voice}

    response = (requests.post(url, headers=headers, data=json.dumps(data))).json()          # HTTP request returns JSON with audio encoded in base64

    if response["success"] == True:                                                         # if the request is successful, return encoded audio
        return ("data:audio/mpeg;base64," + response["data"])
    else: 
        return "./error-responses/conversion-error.mp3"                                     # if the request fails, return path to an audio file containing error message