import requests
import time

BASE = "http://127.0.0.1:5000/"

response = requests.post(BASE, {"cmd": "list"})
print(response.json())

time.sleep(5)
response = requests.post(BASE, {"cmd": "select 0"})
print(response.json())

time.sleep(5)
response = requests.post(BASE, {"cmd": "dir"})
print(response.json())

time.sleep(5)
response = requests.post(BASE, {"cmd": "cd .."})
print(response.json())

time.sleep(5)
response = requests.post(BASE, {"cmd": "cd Reverse Shell"})
print(response.json())

time.sleep(5)
response = requests.post(BASE, {"cmd": "echo a"})
print(response.json())
