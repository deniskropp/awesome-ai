import requests

url = "https://api.fish.audio/v1/tts"

payload = {
    "text": "Where is my grave?",
    "format": "wav"
}
headers = {
    "Authorization": "Bearer 55b6b4661e0642a79fcb4aef21f4eb86",
    "Content-Type": "application/json"
}

response = requests.request("POST", url, json=payload, headers=headers)

with open('x.wav', 'w') as f:
    f.write(response.text)
