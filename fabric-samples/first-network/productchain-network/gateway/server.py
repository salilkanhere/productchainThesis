# socket_echo_server.py
import socket
import sys
import json
import requests
import time

##################################### Raspberry Pi Communication  ###################################
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('192.168.0.24', 10000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)
sock.listen(1)

##################################### REST server communication ###################################
headers = {'content-type': 'application/json'}
json_foo = { "$class": "org.example.productchain.SetupDemo"}
resp = requests.post('http://localhost:3000/api/SetupDemo', json.dumps(json_foo), headers=headers)
print resp.content
print "\n\n\n"


##################################### Run main gateway process ###################################

while True:
    
    print('Waiting for a connection')
    connection, client_address = sock.accept()
    
    
    try:
        print('Connection from', client_address)

        # Receive the data in small chunks and retransmit it
        while True:

            data = connection.recv(48)
            #print("Recieved data: " + str(data))


            if data:
                
                
                try:
                    parsed_data = json.loads(data)

                    if "shipment" in parsed_data and "centigrade" in parsed_data:

                        hyperledger_data = {
                            "$class": "org.example.productchain.TemperatureReading",
                            "centigrade": float(parsed_data["centigrade"]),
                            "shipment": parsed_data["shipment"],
                        }

                        print("********************************************************************")
                        print("Sending temperature " + parsed_data["centigrade"] + " and shipment " + parsed_data["shipment"])
                        resp = requests.post('http://localhost:3000/api/TemperatureReading', json.dumps(hyperledger_data), headers=headers)
                        
                        print("Recieved: " + str(resp.content))
                    else:

                        print("Data not in expected format")
                        
                except:
                    print("********************************************************************")
                    print('Data unable to be sent')
                    print(data)

            else:
                print('No data from', client_address)
                break

    finally:
        # Clean up the connection
        connection.close()
