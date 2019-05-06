import json
import requests
import time
import urllib

headers = {'content-type': 'application/json'}


json_temp = {
  "$class": "org.example.productchain.TemperatureReading",
  "centigrade": 0,
  "batch": "resource:org.example.productchain.Batch#001"
}



json_foo = {}


#resp = requests.post('http://localhost:3000/api/system/historian', json.dumps(json_foo), headers=headers)

#how to read history
#resp = requests.get('http://localhost:3000/api/system/historian', headers=headers)

#how to get transaction history
json_filter = {"where":{"batchID": "1"}}

resp = requests.get('http://localhost:3000/api/CreateBatch?filter=' + urllib.quote(json.dumps(json_filter)), headers=headers)


parsed = json.loads(resp.content)
print(json.dumps(parsed, indent=4, sort_keys=True))
