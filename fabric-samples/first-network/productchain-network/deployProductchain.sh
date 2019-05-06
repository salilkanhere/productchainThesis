#!bin/bash/

export FABRIC_VERSION=hlfv12
./../stopFabric.sh
#./../teardownFabric.sh
#./../downloadFabric.sh
./../startFabric.sh

composer card delete -c PeerAdmin@productchain-network
composer card delete -c admin@productchain-network

rm -fr ~/.composer

composer card create -p connection.json -u PeerAdmin -c ../certs/Admin@org1.example.com-cert.pem -k ../certs/114aab0e76bf0c78308f89efc4b8c9423e31568da0c340ca187a9b17aa9a4457_sk -r PeerAdmin -r ChannelAdmin

composer card import -f PeerAdmin@productchain-network.card


composer archive create -t dir -n .

composer network install -c PeerAdmin@productchain-network -a productchain-network@0.0.1.bna

composer network start --networkName productchain-network --networkVersion 0.0.1 -A admin -S adminpw -c PeerAdmin@productchain-network


composer card import -f admin@productchain-network.card

composer network ping -c admin@productchain-network
