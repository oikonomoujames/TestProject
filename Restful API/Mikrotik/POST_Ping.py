import requests
import json

url = "https://192.168.0.80/rest/ping"

payload = json.dumps({
  "count": "5",
  "address": "8.8.8.8"
})
headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Basic YWRtaW46YWRtaW4='
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)