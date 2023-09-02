import requests
import cv2
import json

def save_img(uid_list, file_path):
    file = json.load(open(file_path))
    names = []
    for uid in uid_list:
        response = requests.get(file[uid]["thumbnail_url"])
        name = file[uid]["name"]
        names.append(name)
        if response.status_code == 200:
            with open(f'./static/{name}.jpg', 'wb') as f:
                f.write(response.content)
    return names
