import json
import requests
import time
import urllib


class Gateway():

    headers = {'content-type': 'application/json'}


    ## SUBMIT temperature reading ##
    def temperature_reading(self):
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


    ## GET batch data by batch ID ## 
    def get_transfers(self, batch_id):
        json_filter = {"where":{"batch": "resource:org.example.productchain.Batch#" + str(batch_id)}}
 
        resp = requests.get('http://localhost:3000/api/TransferBatch?filter=' + urllib.quote(json.dumps(json_filter)), headers=self.headers)
        parsed = json.loads(resp.content)
        return parsed


    ## GET batch data by batch ID ## 
    def get_create(self, batch_id):
        json_filter = {"where":{"batchID": str(batch_id)}}
 
        resp = requests.get('http://localhost:3000/api/CreateBatch?filter=' + urllib.quote(json.dumps(json_filter)), headers=self.headers)
        parsed = json.loads(resp.content)
        return parsed



    def get_product_story(self, batch_id):

        story = []
        transfers = self.get_transfers(batch_id)
        create = self.get_create(batch_id)

        story.extend(transfers)
        story.extend(create)
        queue = [create]

        while len(queue) > 0:
            curr = queue.pop(0)

            for a in curr:
            
                if 'constituents' in a:
                    for i in a['constituents']:

                        transfers = self.get_transfers(i[-1])
                        create = self.get_create(i[-1])

                        story.extend(transfers)
                        story.extend(create)

                        queue.append(create)


        story.sort(key=self.extract_time, reverse=True)
        return story


    def extract_time(self, json):
        try:
            numberjson = filter(lambda x: x.isdigit(), json['timestamp'])
            return int(numberjson)
        except KeyError:
            return 0


gw = Gateway()
print(json.dumps(gw.get_product_story(5), indent=4, sort_keys=True))