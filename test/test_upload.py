import requests

# url = "http://127.0.0.1:8000/upload/"
# path = "../image/cans2.JPG"
# files = {'file': open(path, 'rb')}
# r = requests.post(url, files=files)
# print(r.url)
# print(r.text)


# url = "http://127.0.0.1:8000/identifyImage/"
# path = "../image/cans2.JPG"
# files = {'image': open(path, 'rb')}
# r = requests.get(url, files=files)
# print(r.text)

import json
import base64
path = "../image/cans2.jpg"
with open(path, "rb") as f:
    data = f.read()
encoded_data = base64.b64encode(data).decode("utf-8")

url = "http://bbox.natapp1.cc/scanImage/invoke/"

r = requests.post(
    url, json={"input": {"image": encoded_data}}
).json()


print(r)
