import json
import requests
import time
import urllib

RURAL = 'localhost:3000'
URBAN = 'localhost:3000'

class Setup():

    headers = {'content-type': 'application/json'}

    def init(self):
        server_rural = {
            "$class": "org.example.productchain.Setup",
            "region": "RURAL"
        }

        server_urban = {
            "$class": "org.example.productchain.Setup",
            "region": "URBAN"
        }
        
        resp_rural = requests.post('http://'+ RURAL + '/api/Setup', json.dumps(server_rural), headers=self.headers)
        resp_urban = requests.post('http://'+ URBAN + '/api/Setup', json.dumps(server_urban), headers=self.headers)

        parsed_rural = json.loads(resp_rural.content)
        parsed_urban = json.loads(resp_urban.content)

        print(json.dumps(parsed_rural, indent=4, sort_keys=True))
        print(json.dumps(parsed_urban, indent=4, sort_keys=True))

        return json.dumps(parsed_rural, indent=4, sort_keys=True)


class CreateBatch():

    headers = {'content-type': 'application/json'}

    def create(self, batch_id, owner, product_type, region, constituents):

        json_constituents = []
        constituents = constituents.split(' ')
        for curr in constituents:
            json_constituents.append("org.example.productchain.Batch#" + str(curr))

        json_data = {
            "$class": "org.example.productchain.CreateBatch",
            "batchID": str(batch_id),
            "currentOwner": str(owner),
            "type": str(product_type),
            "constituents": json_constituents
        }

        if str(region) == 'Rural':
            response = requests.post('http://'+ RURAL + '/api/CreateBatch', json.dumps(json_data), headers=self.headers)
            
        else:
            resp_urban = requests.post('http://'+ URBAN + '/api/CreateBatch', json.dumps(json_data), headers=self.headers)
            response = json.loads(resp_urban.content)

        result = json.loads(response.content)
        if response.status_code != 200:
            result = "ERROR: " + result["error"]["message"]

        print(json.dumps(result, indent=4, sort_keys=True))
        return result





class TransferBatch():

    headers = {'content-type': 'application/json'}

    def transfer(self, batch_id, owner, product_type, region):

        json_data = {
            "$class": "org.example.productchain.TransferBatch",
            "newOwner": str(owner),
            "type": str(product_type),
            "region": str(region).upper(),
            "batch": "resource:org.example.productchain.Batch#" + str(batch_id)
        }

        resp_rural = requests.post('http://'+ RURAL + '/api/TransferBatch', json.dumps(json_data), headers=self.headers)
        resp_urban = requests.post('http://'+ URBAN + '/api/TransferBatch', json.dumps(json_data), headers=self.headers)

        
        parsed_rural = json.loads(resp_rural.content)
        parsed_urban = json.loads(resp_urban.content)

        if resp_rural.status_code != 200 and resp_urban.status_code != 200:
            result = "ERROR FROM BOTH SERVERS: " + parsed_rural["error"]["message"] 
            result += parsed_urban["error"]["message"]
        elif resp_rural.status_code != 200:
            result = parsed_urban
        else:
            result = parsed_rural

        print(json.dumps(parsed_rural, indent=4, sort_keys=True))
        print(json.dumps(parsed_urban, indent=4, sort_keys=True))

        return result




class QueryBatch():
    
    headers = {'content-type': 'application/json'}

    def query(self, batch_id):

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



    def get_transfers(self, batch_id):
        json_filter = {"where":{"batch": "resource:org.example.productchain.Batch#" + str(batch_id)}}
 
        resp_rural = requests.get('http://'+ RURAL + '/api/TransferBatch?filter=' + urllib.quote(json.dumps(json_filter)), headers=self.headers)
        resp_urban = requests.get('http://'+ URBAN + '/api/TransferBatch?filter=' + urllib.quote(json.dumps(json_filter)), headers=self.headers)
        
        parsed_rural = json.loads(resp_rural.content)
        parsed_urban = json.loads(resp_urban.content)


        if resp_rural.status_code == 200 and resp_urban.status_code == 200:
            result = parsed_rural.extend(parsed_urban)
        elif resp_rural.status_code == 200:
            result = parsed_rural
        elif resp_urban.status_code == 200:
            result = parsed_urban
        else:
            result = []

        print(json.dumps(parsed_rural, indent=4, sort_keys=True))
        print(json.dumps(parsed_urban, indent=4, sort_keys=True))
        
        return result



    def get_create(self, batch_id):
        json_filter = {"where":{"batchID": str(batch_id)}}
 
        resp_rural = requests.get('http://'+ RURAL + '/api/CreateBatch?filter=' + urllib.quote(json.dumps(json_filter)), headers=self.headers)
        resp_urban = requests.get('http://'+ URBAN + '/api/CreateBatch?filter=' + urllib.quote(json.dumps(json_filter)), headers=self.headers)
        
        parsed_rural = json.loads(resp_rural.content)
        parsed_urban = json.loads(resp_urban.content)


        if resp_rural.status_code == 200 and resp_urban.status_code == 200:
            result = parsed_rural.extend(parsed_urban)
        elif resp_rural.status_code == 200:
            result = parsed_rural
        elif resp_urban.status_code == 200:
            result = parsed_urban
        else:
            result = []

        print(json.dumps(parsed_rural, indent=4, sort_keys=True))
        print(json.dumps(parsed_urban, indent=4, sort_keys=True))

        return result


    def extract_time(self, json):
        try:
            numberjson = filter(lambda x: x.isdigit(), json['timestamp'])
            return int(numberjson)
        except KeyError:
            return 0
