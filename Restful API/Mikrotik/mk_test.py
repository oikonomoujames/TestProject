import requests
import json
from requests.auth import HTTPBasicAuth

response = requests.get("https://192.168.0.80/rest/system/resource",
                        auth=HTTPBasicAuth('admin', 'admin'),
                        verify=False)
print(response)
print(response.text)
a = json.loads(response.text)

print(a.get("architecture-name"))

command = json.dumps(
            {".id": "*2",
            "actual-interface": "ether3",
            "address": "10.0.0.1/24",
            "disabled": "false",
            "dynamic": "true",
            "interface": "ether3",
            "invalid": "false",
            "network": "10.0.0.0"})

response = requests.put(url="https://192.168.0.80/rest/ip/address/",
                        auth=HTTPBasicAuth('admin', 'admin'),
                        verify=False,
                        headers="content-type: application/json",
                        data=command,
                        )

print(response.text)
