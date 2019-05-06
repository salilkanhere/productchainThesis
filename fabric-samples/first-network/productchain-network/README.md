# productchain-network

Productchain implemented on HyperLedger Composer


# Instructions

## Startup
- Ensure Hyperledger Composer and the Composer development environment is set up (https://hyperledger.github.io/composer/v0.19/installing/development-tools.html)
- Clone repository into Composer directory
- *cd ProductChain*
- *./startProductChain.sh*

The startProductChain.sh script will remove any existing docker containers, terminate any existing networks running on fabric, stop Fabric (if it is running), then re-start fabric, regenerate the peer admin card, create a new .bna file, install the new network, start the new network, import the network admin card and ping the network.

## Submitting transactions
To start the rest server, uncomment the relevant line in the startProductchain.sh script.

Starting composer playground in the ProductChain directory (by running *composer-playground*) allows you to easily see what kind of transactions are being sent by the rest server, as well as to make transactions via an interface.

## Sensor automation
The two python scripts found in the /Gateway directory allow for the integration of the sensor. 

- *gateway.py* is a script for testing rest server transactions without having to connect a sensor (will be deleted later)
- *server.py* is a script for getting live temperature data sent to the gateway machine and submitting it to the hyperledger composer.
