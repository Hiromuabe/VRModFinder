import requests
import cv2
import json

file = json.load(open("data.json"))
uid = "2607a4881a8546119f74edf1d46b195f"
url = file[uid]["thumbnail_url"]
response = requests.get(url)

if response.status_code == 200:
    with open('./static/image.jpg', 'wb') as f:
        f.write(response.content)