# THESIS

Supply chains grow ever more complex as businesses globalize. The effect of a mistake or malpractice at any point within the chain can have disastrous impacts on public health and safety. It is for these reasons that the existence of clear, immutable and correct data on a products path from source to destination is becoming increasingly important. This paper proposes a way to make this data a reality. Through a marriage of blockchain and IoT, there emerges a way by which data can be collected that reflects the state of products as they progress through the supply chain and then stored on a platform that ensures that the data is secure and immutable. Hyperledger Fabric and Hyperledger Composer frameworks are utilized by this project for the blockchain implementation, and a Raspberry Pi 3 with a digital temperature sensor attachment works as a prototype for an IoT sensor device.

Core paper referenced in design: *"ProductChain: Scalable Blockchain Framework to Support Provenance in Supply Chains"*
Found here: https://www.researchgate.net/publication/329292174_ProductChain_Scalable_Blockchain_Framework_to_Support_Provenance_in_Supply_Chains


## Structure

![Productchain architecture](architecture.png?raw=true "Architecture")

The blockchain network element of Productchain is built using Hyperledger Fabric and Composer (Composer is a tooleset and framework that works with Fabric to make development easier). The network structure is sharded for 

Fabric: https://hyperledger-fabric.readthedocs.io/en/latest/
Composer: https://hyperledger.github.io/composer/latest/introduction/introduction.html


![Productchain shards](shards.png?raw=true "Shards")

The top level application is built using Flask (a Python microframework) and abstracts the details of the network from the clients/users.


![The Application](toplevelapp.png?raw=true "App")


## Hyperledger Fabric Structure

ProductChain network implemented with the following underlying Hyperledger Fabric configuration:

- 1 Organization
- 2 Peers (Future work: make number of peers easily variable for benchmarking/testing purposes)
- 1 certificate authority
- Orderer: kafka or solo

More information on the configuration can be found within the connection file:
*/fabric-samples/first-network/connection/connections.json*


## Hyperledger Composer Structure

Composer creates the business network definition using 3 main files:

- *Model (.cto)*:  defines data structures for assets, transactions and participants
- *Script (.js)*:  defines the behaviour of transactions
- *Access Control Rules (.acl)*:  defines what participants can access what assetsand transactions

Code defined here:
*/fabric-samples/first-network/productchain-network*

## Instructions

In order to startup the network, follow the following steps:

1. Start up the underlying Fabric configuration:

      *cd fabric-samples/first-network*
  
      *./byfn.sh generate*
  
      *./byfn.sh -m up -s couchdb -a {-o kafka}*

2. Start up the Composer Network (Insert certificates into connection.json file, create and import cards, compile the busness archive file, install and start the network, ping network to confirm success of the startup sequence)

      *cd connection*
  
      *./startup.sh*


All these steps are automated in the scripts. The Fabric configuration followed the following tutorial:
https://hyperledger.github.io/composer/latest/tutorials/deploy-to-fabric-multi-org

Both scripts (byfn.sh and startup.sh) can be read to understand the network setup in greater detail.