import json
import requests
import time
import urllib


class Gateway():

    headers = {'content-type': 'application/json'}


    ## SUBMIT temperature reading ##
    def tempperature_reading(self):
        json_temp = {
            "$class": "org.example.productchain.TemperatureReading",
            "centigrade": 12,
            "batch": "resource:org.example.productchain.Batch#1"
        }

        resp = requests.post('http://localhost:3000/api/TemperatureReading', json.dumps(json_temp), headers=headers)

        parsed = json.loads(resp.content)
        print(json.dumps(parsed, indent=4, sort_keys=True))


    ## READ ALL history ##
    def read_history(self):
        resp = requests.get('http://localhost:3000/api/system/historian', headers=headers)

        parsed = json.loads(resp.content)
        print(json.dumps(parsed, indent=4, sort_keys=True))



    ## GET all temperature readings for batch 1 ## 
    def get_temp_read(self):
        json_filter = {"where":{"batch": "resource:org.example.productchain.Batch#1"}}

        resp = requests.get('http://localhost:3000/api/TemperatureReading?filter=' + urllib.quote(json.dumps(json_filter)), headers=headers)

        parsed = json.loads(resp.content)
        print(json.dumps(parsed, indent=4, sort_keys=True))




    ## GET batch data by batch ID ## 
    def get_batch_by_id(self, batch_id):
        json_filter = {"where":{"batchId": str(batch_id)}}
 
        resp = requests.get('http://localhost:3000/api/Batch?filter=' + urllib.quote(json.dumps(json_filter)), headers=self.headers)
        parsed = json.loads(resp.content)
        return parsed



    ## GET a list of batches that were the source of this batch ## 
    def get_source_batch(self, batch_id):

        first = self.get_batch_by_id(batch_id)
        queue = [first]
        roots = []
        
        while len(queue) > 0:
            curr = queue.pop(0)

            for a in curr:
                
                if 'constituents' in a:
                    for i in a['constituents']:
                        queue.append(self.get_batch_by_id(i[-1]))

                else:
                    roots.append(curr)

        
        return roots



gw = Gateway()
print(json.dumps(gw.get_source_batch(6), indent=4, sort_keys=True))