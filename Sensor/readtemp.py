import os
import glob
import time
import socket
import sys
import json
import requests
import urllib

# Define own shipment
BATCH = str(sys.argv[1])


# initialize sensor
os.system('modprobe w1-gpio')
os.system('sudo modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

# Comms
headers = {'content-type': 'application/json'}

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()

    equals_pos = lines[1].find('t=')
    
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c



try:
    while True:

        data = {
            "$class": "org.example.productchain.TemperatureReading",
            "centigrade": str('{:.2f}'.format(read_temp())),
            "batch": "resource:org.example.productchain.Batch#" + BATCH
        }
        
        resp_rural = requests.post('http://ec2-52-65-227-151.ap-southeast-2.compute.amazonaws.com:3000/api/TemperatureReading', json.dumps(data), headers=headers)
        resp_urban = requests.post('http://ec2-13-238-161-98.ap-southeast-2.compute.amazonaws.com:3000/api/TemperatureReading', json.dumps(data), headers=headers)

        parsed_rural = json.loads(resp_rural.content)
        parsed_urban = json.loads(resp_urban.content)
        print("RURAL:")
        print(json.dumps(parsed_rural, indent=4, sort_keys=True))
        print("URBAN:")
        print(json.dumps(parsed_urban, indent=4, sort_keys=True))

        time.sleep(10)

finally:
    print('FINISHED')
    
