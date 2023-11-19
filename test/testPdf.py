import base64

with open("../image/sample.pdf", "rb") as f:
    data = f.read()

encoded_data = base64.b64encode(data).decode("utf-8")

import requests

try:
    response = requests.post(
        "http://127.0.0.1:8000/pdf/invoke/",
        json={"input": {"file": encoded_data}}
    )
    response.raise_for_status()  # 检查请求是否成功
    print(response.json())
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
    print("Response content:", response.content)
