import requests

# BASE = "http://127.0.0.1:80" # "http://127.0.0.1:5000" for erase_upload_run.sh
BASE = "http://127.0.0.1:5000"

json_data = {
                "userID": "abcdefghijkpqrstxyz",
                "content": "Today is Friday",
            }

# response = requests.post(BASE + "/post", json_data) 
response = requests.get(BASE + "/get")

print(response)
print(response.json())

# Can run from local machine with
# python3 destination.py