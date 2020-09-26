import requests

url = "http://127.0.0.1:8000/get_names"
r = requests.get(url).json()
print(r)
