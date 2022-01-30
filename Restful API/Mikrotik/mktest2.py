import requests
import json

url = "https://192.168.0.80/rest/ip/address/*2"

payload = json.dumps({
  ".id": "*2",
  "address": "10.0.0.1/24",
  "comment": "test",
  "disabled": "false",
  "interface": "ether3",
  "network": "10.0.0.0"
})
headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Basic YWRtaW46YWRtaW4='
}

response = requests.request("PATCH", url, headers=headers, data=payload, verify=False)

print(response.text)