import requests
from random import randint, shuffle

def request(url, data):
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(url, json=data, headers=headers)
        #response.raise_for_status()  # Raise an error for HTTP codes 4xx/5xx
        #print("Response status code:", response.status_code)
        #print("Response JSON:", response.json())
        #print("response text:", response.text)
        return response.text
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)


partition = "default"
target = "8080"
ip = "192.168.100.203"

filler = "A" * 200

data_len = 10000

verfication_data = [randint(1, 1000000000) for _ in range(data_len)]

for i in range(data_len):
    url = f"http://{ip}:{target}/api/insert"
    data = {
        "key": str(i),
        "value": filler + str(verfication_data[i]),
        "partition": "default"
    }
    request(url, data)

indices = list(range(data_len))
shuffle(indices)
errors = False

for i in indices:
    url = f"http://{ip}:{target}/api/get"
    data = {
        "key": str(i),
        "partition": "default"
    }
    n = request(url, data)
    if n != filler + str(verfication_data[i]):
        print(f"Data mismatch at index {i}: expected {verfication_data[i]}, got {n}")
        errors = True

if not errors:
    print("Verification successful: all data matches.")