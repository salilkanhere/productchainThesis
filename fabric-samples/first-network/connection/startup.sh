rm -rf ~/.composer/
rm *bna

./certs.sh


rm *pem
rm *_sk
cp ../crypto-config/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp/keystore/*_sk .
cp ../crypto-config/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp/signcerts/A* .

composer archive create -t dir -n ../productchain-network/

composer card create -p connection.json -u PeerAdmin -c *pem -k *_sk -r PeerAdmin -r ChannelAdmin

composer card import -f PeerAdmin@byfn-network.card --card PeerAdmin@byfn-network

INPUTT=$(ls *bna)

SSTRING=$(echo $INPUTT | cut -d'@' -f 2 | cut -d'.' -f 3)


composer network install --card PeerAdmin@byfn-network --archiveFile productchain-network@0.0.$SSTRING.bna

composer network start --networkName productchain-network --networkVersion 0.0.$SSTRING -A admin -S adminpw -c PeerAdmin@byfn-network

composer card import -f admin@productchain-network.card

composer network ping --card admin@productchain-network
