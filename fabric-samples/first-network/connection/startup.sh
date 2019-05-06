./certs.sh


rm *pem
rm *_sk
cp ../crypto-config/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp/keystore/*_sk .
cp ../crypto-config/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp/signcerts/A* .

composer card create -p connection.json -u PeerAdmin -c *pem -k *_sk -r PeerAdmin -r ChannelAdmin

composer card delete -c PeerAdmin@byfn-network
composer card delete -c admin@productchain-network

composer card import -f PeerAdmin@byfn-network.card --card PeerAdmin@byfn-network

composer network install --card PeerAdmin@byfn-network --archiveFile ../productchain-network/productchain-network@0.0.1.bna

composer network start --networkName productchain-network --networkVersion 0.0.1 -A admin -S adminpw -c PeerAdmin@byfn-network

composer card import -f admin@productchain-network.card

composer network ping --card admin@productchain-network
