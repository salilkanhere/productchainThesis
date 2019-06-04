import json
import requests
import time
import urllib
import timeit

# Two region servers
RURAL = 'ec2-52-65-227-151.ap-southeast-2.compute.amazonaws.com:3000'
URBAN = 'ec2-13-238-161-98.ap-southeast-2.compute.amazonaws.com:3000'

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

        print("Starting req")
        
        resp_rural = requests.post('http://'+ RURAL + '/api/Setup', json.dumps(server_rural), headers=self.headers)
        resp_urban = requests.post('http://'+ URBAN + '/api/Setup', json.dumps(server_urban), headers=self.headers)

        print("Ended req")

        return (resp_rural.status_code == 200 and resp_urban.status_code == 200)


class CreateHACCP():

    headers = {'content-type': 'application/json'}

    def create(self, product_type, min_temperature, max_temperature):


        json_data = {
            "$class": "org.example.productchain.CreateHACCP",
            "type": str(product_type).upper(),
            "minTemperature": int(min_temperature),
            "maxTemperature": int(max_temperature)
        }

        resp_rural = requests.post('http://'+ RURAL + '/api/CreateHACCP', json.dumps(json_data), headers=self.headers)
        resp_urban = requests.post('http://'+ URBAN + '/api/CreateHACCP', json.dumps(json_data), headers=self.headers)

        return (resp_rural.status_code == 200 and resp_urban.status_code == 200)


class CreateBatch():

    headers = {'content-type': 'application/json'}

    def create(self, batch_id, owner, product_type, region, constituents):

        json_constituents = []
        
        if len(constituents) > 0:
            constituents = constituents.split(' ')
            print("Constituents " + str(constituents))

            for curr in constituents:
                json_constituents.append("org.example.productchain.Batch#" + str(curr))

        json_data = {
            "$class": "org.example.productchain.CreateBatch",
            "batchID": str(batch_id),
            "currentOwner": str(owner),
            "type": str(product_type).upper(),
            "constituents": json_constituents
        }

        if str(region) == 'Rural':
            response = requests.post('http://'+ RURAL + '/api/CreateBatch', json.dumps(json_data), headers=self.headers)
        elif str(region) == 'Urban':
            response = requests.post('http://'+ URBAN + '/api/CreateBatch', json.dumps(json_data), headers=self.headers)

        return (response.status_code == 200)





class TransferBatch():

    headers = {'content-type': 'application/json'}

    def transfer(self, batch_id, owner, product_type, region):

        json_data = {
            "$class": "org.example.productchain.TransferBatch",
            "newOwner": str(owner),
            "type": str(product_type).upper(),
            "region": str(region).upper(),
            "batch": "resource:org.example.productchain.Batch#" + str(batch_id)
        }

        resp_rural = requests.post('http://'+ RURAL + '/api/TransferBatch', json.dumps(json_data), headers=self.headers)
        resp_urban = requests.post('http://'+ URBAN + '/api/TransferBatch', json.dumps(json_data), headers=self.headers)

        return (resp_rural.status_code == 200 or resp_urban.status_code == 200)


class QueryTemp():

    headers = {'content-type': 'application/json'}

    def wrapper(self, func, *args, **kwargs):
        def wrapped():
            return func(*args, **kwargs)
        return wrapped

    def test(self, batch_id):

        wrapper = self.wrapper(self.query, batch_id)

        print("~~~~~~~~~~~ TIMING RESULTS ~~~~~~~~~~~")
        print(timeit.timeit(wrapper, number=5))
        print("~~~~~~~~~ END TIMING RESULTS ~~~~~~~~~")
        
        return 0

    def query(self, batch_id):

        haccp = self.get_batch_HACCP(batch_id)

        if not haccp:
            return 0

        json_filter = {"where":{"batch": "resource:org.example.productchain.Batch#" + str(batch_id)}}

        resp_rural = requests.get('http://'+ RURAL + '/api/TemperatureReading?filter=' + urllib.quote(json.dumps(json_filter)), headers=self.headers)
        resp_urban = requests.get('http://'+ URBAN + '/api/TemperatureReading?filter=' + urllib.quote(json.dumps(json_filter)), headers=self.headers)
        
        parsed_rural = json.loads(resp_rural.content)
        parsed_urban = json.loads(resp_urban.content)

        
        temperatures = ''
        if resp_rural.status_code == 200 and resp_urban.status_code == 200:
            parsed_rural.extend(parsed_urban)
            temperatures = parsed_rural
        else:
            return 0

        return self.parse_temperatures(temperatures, haccp)


    def get_batch_HACCP(self, batch_id):

        #getting batch
        json_filter = {"where":{"batchId": str(batch_id)}}

        resp_rural = requests.get('http://'+ RURAL + '/api/Batch?filter=' + urllib.quote(json.dumps(json_filter)), headers=self.headers)
        resp_urban = requests.get('http://'+ URBAN + '/api/Batch?filter=' + urllib.quote(json.dumps(json_filter)), headers=self.headers)
        
        parsed_rural = json.loads(resp_rural.content)
        parsed_urban = json.loads(resp_urban.content)

        product_type = ''
        if resp_rural.status_code == 200 and len(parsed_rural) > 0:
            product_type = parsed_rural[0]["type"]
        elif resp_urban.status_code == 200 and len(parsed_urban) > 0:
            product_type = parsed_urban[0]["type"]
        else:
            return 0

        #getting HACCP
        json_filter = {"where":{"type": product_type}}

        resp_rural = requests.get('http://'+ RURAL + '/api/HACCP?filter=' + urllib.quote(json.dumps(json_filter)), headers=self.headers)
        resp_urban = requests.get('http://'+ URBAN + '/api/HACCP?filter=' + urllib.quote(json.dumps(json_filter)), headers=self.headers)
        
        parsed_rural = json.loads(resp_rural.content)
        parsed_urban = json.loads(resp_urban.content)

        haccp = ''
        if resp_rural.status_code == 200 and len(parsed_rural) > 0:
            haccp = parsed_rural[0]
        elif resp_urban.status_code == 200 and len(parsed_urban) > 0:
            haccp = parsed_urban[0]
        else:
            return 0

        return haccp

    def parse_temperatures(self, temperatures, haccp):
        
        response = {}
        response["all_temp"] = []
        response["violating_temp"] = []

        temperatures.sort(key=self.extract_time, reverse=True)

        for curr in temperatures:
            temp = {
                "date" : curr["timestamp"][:10],
                "time" : curr["timestamp"][12:19],
                "temp" : str(curr["centigrade"])
            }
            if curr["centigrade"] < haccp["minTemperature"] or curr["centigrade"] > haccp["maxTemperature"]:
                response["violating_temp"].append(temp)

            response["all_temp"].append(temp)

        return response


    def extract_time(self, json):
        try:
            numberjson = filter(lambda x: x.isdigit(), json['timestamp'])
            return int(numberjson)
        except KeyError:
            return 0



class QueryBatch():
    
    headers = {'content-type': 'application/json'}

    def wrapper(self, func, *args, **kwargs):
        def wrapped():
            return func(*args, **kwargs)
        return wrapped

    def test(self, batch_id):

        wrapper = self.wrapper(self.query, batch_id)

        print("~~~~~~~~~~~ TIMING RESULTS ~~~~~~~~~~~")
        print(timeit.timeit(wrapper, number=5))
        print("~~~~~~~~~ END TIMING RESULTS ~~~~~~~~~")
        
        return 0

    def query(self, batch_id):

        create = self.get_create(batch_id)
        transfers = self.get_transfers(batch_id)

        story = list(create)
        story.extend(transfers)
        queue = list(create)
        
        while len(queue) > 0:
            curr = queue.pop(0)

            if 'constituents' in curr:
                for i in curr['constituents']:


                    transfers = self.get_transfers(i.split('#')[1])
                    create = self.get_create(i.split('#')[1])

                    story.extend(transfers)
                    story.extend(create)

                    queue.extend(create)



        return self.format_story(story)



    def get_transfers(self, batch_id):
        json_filter = {"where":{"batch": "resource:org.example.productchain.Batch#" + str(batch_id)}}
 
        resp_rural = requests.get('http://'+ RURAL + '/api/TransferBatch?filter=' + urllib.quote(json.dumps(json_filter)), headers=self.headers)
        resp_urban = requests.get('http://'+ URBAN + '/api/TransferBatch?filter=' + urllib.quote(json.dumps(json_filter)), headers=self.headers)
        
        parsed_rural = json.loads(resp_rural.content)
        parsed_urban = json.loads(resp_urban.content)

        result = ''
        if resp_rural.status_code == 200 and resp_urban.status_code == 200:
            for a in parsed_rural:
                a["region"] = "Rural"
            
            for a in parsed_urban:
                a["region"] = "Urban"
            
            parsed_rural.extend(parsed_urban)
            result = parsed_rural
        elif resp_rural.status_code == 200:
            for a in parsed_rural:
                a["region"] = "Rural"

            result = parsed_rural
        elif resp_urban.status_code == 200:
            for a in parsed_urban:
                a["region"] = "Urban"
            
            result = parsed_urban
        else:
            result = []
        
        return result



    def get_create(self, batch_id):
        json_filter = {"where":{"batchID": str(batch_id)}}
 
        resp_rural = requests.get('http://'+ RURAL + '/api/CreateBatch?filter=' + urllib.quote(json.dumps(json_filter)), headers=self.headers)
        resp_urban = requests.get('http://'+ URBAN + '/api/CreateBatch?filter=' + urllib.quote(json.dumps(json_filter)), headers=self.headers)
        
        parsed_rural = json.loads(resp_rural.content)
        parsed_urban = json.loads(resp_urban.content)


        result = ''
        if resp_rural.status_code == 200 and resp_urban.status_code == 200:
            for a in parsed_rural:
                a["region"] = "Rural"
            
            for a in parsed_urban:
                a["region"] = "Urban"
            
            parsed_rural.extend(parsed_urban)
            result = parsed_rural

        elif resp_rural.status_code == 200:
            for a in parsed_rural:
                a["region"] = "Rural"

            result = parsed_rural
        elif resp_urban.status_code == 200:
            for a in parsed_urban:
                a["region"] = "Urban"
            
            result = parsed_urban
        else:
            result = []

        return result


    def extract_time(self, json):
        try:
            numberjson = filter(lambda x: x.isdigit(), json['timestamp'])
            return int(numberjson)
        except KeyError:
            return 0


    def format_story(self, story):

        story.sort(key=self.extract_time, reverse=True)
        final = []

        for curr in story:

            transaction_type = curr["$class"].split('.')[3]
            transaction_id = curr["transactionId"]
            date = curr["timestamp"][:10]
            time = curr["timestamp"][12:19]
            region = curr["region"]
            batch = ""
            constituents = []
            owner = ""

            if transaction_type == "TransferBatch":
                batch = curr["batch"].split('#')[1]
                constituents = 0
                owner = curr["newOwner"]
            elif transaction_type == "CreateBatch":
                batch = curr["batchID"]
                for val in curr["constituents"]:
                    constituents.append(val.split('#')[1])
                owner = curr["currentOwner"]



            obj = {
                "transaction_type" : transaction_type,
                "date" : date,
                "time" : time,
                "batch" : batch,
                "owner" : owner,
                "constituents" : constituents,
                "transaction_id": transaction_id,
                "region": region
            }

            final.append(obj)

        return final
