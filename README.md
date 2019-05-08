# THESIS

ProductChain network implemented with the following underlying Hyperledger Fabric configuration:

- 1 Organization
- 2 Peers (Future work: make number of peers easily variable for speed testing purposes)
- 1 certificate authority
- Orderer: kafka or solo

More information on the configuration can be found within the connection file:
/fabric-samples/first-network/connection/connections.json


## Instructions

In order to startup the network, follow the following steps:

1. Start up the underlying Fabric configuration:
*cd fabric-samples/first-network*
*./byfn.sh generate*
*./byfn.sh -m up -s couchdb -a {-o kafka}*

2. Start up the Composer Network (Insert certificates into connection.json file, create and import cards, compile the busness archive file, install and start the network, ping network to confirm success of the startup sequence)
*cd connection*
*./startup.sh*
