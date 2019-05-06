rm *txt

awk 'NF {sub(/\r/, ""); printf "%s\\n",$0;}' ../crypto-config/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt > ca-org1.txt

awk 'NF {sub(/\r/, ""); printf "%s\\n",$0;}' ../crypto-config/ordererOrganizations/example.com/orderers/orderer.example.com/tls/ca.crt > orderer.txt

sed -i 's/[\/&]/\\&/g' ca-org1.txt
sed -i 's/[\/&]/\\&/g' orderer.txt

# Copy the template to the file that will be modified to add the private key
cp connection_template.json connection.json

ORDERER_CERT=$(cat orderer.txt)
ORG1_CERT=$(cat ca-org1.txt)

sed -i "s/ORDERER_CERT/${ORDERER_CERT}/g" connection.json
sed -i "s/ORG1_CERT/${ORG1_CERT}/g" connection.json
