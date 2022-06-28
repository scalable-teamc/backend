import requests

# BASE = "http://127.0.0.1:80" # "http://127.0.0.1:5000" for erase_upload_run.sh
BASE = "http://127.0.0.1:5000"

json_data = {
                "userID": "abcdefghijkpqrstxyz",
                "content": "Today is JJJ"
            }

# response = requests.post(BASE + "/post", json_data) 
# print(response.json())

# ^^^ DOESNT WORK WITH Flask 2.1 for some reason. Use this for POST
# curl -X POST http://127.0.0.1:5000/post -H 'Content-Type: application/json' -d '{ "userID": "abcdefghijkpqrstxyz", "content": "Today is JJJ" }'

response = requests.post(BASE + "/recent")
for i in response.json().get("lst"):
    print(i)



# Can run from local machine with
# python3 tester.py