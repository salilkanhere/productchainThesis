rm ../productchain-network/*bna *bna
composer archive create -t dir -n ../productchain-network/
composer network install --card PeerAdmin@byfn-network -a *bna

INPUTT=$(ls *bna)

SSTRING=$(echo $INPUTT | cut -d'@' -f 2)
echo $SSTRING
SUBSTRING=$(echo $SSTRING | cut -d'.' -f 3)

composer network upgrade -c PeerAdmin@byfn-network -n productchain-network -V 0.0.$SUBSTRING
