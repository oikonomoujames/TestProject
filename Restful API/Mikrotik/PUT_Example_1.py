import requests
import json

url = "https://192.168.0.80/rest/ip/address"

payload = json.dumps({
  "address": "192.168.111.111/32",
  "disabled": "false",
  "interface": "ether4",
  "network": "192.168.111.111"
})
headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Basic YWRtaW46YWRtaW4='
}

response = requests.request("PUT", url, headers=headers, data=payload, verify=False)

print(response.text)