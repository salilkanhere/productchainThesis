#!/bin/bash

# Script that will shut down any existing network running on Hyperledger composer
# and initialize the Productchain network and its REST server



echo "#################################### Removing docker images  ################################### "
docker kill $(docker ps -q)
docker rm $(docker ps -aq)
docker rmi $(docker images dev-* -q)

echo "################################## Stopping Hyperledger Fabric ################################# "
./../stopFabric.sh


echo "#################################### Running Teardown Fabric ################################### "
./../teardownFabric.sh

echo "################################# Restarting Hyperledger Fabric ################################"
./../startFabric.sh


echo "################################# Creating peer admin card  ################################"
./../createPeerAdminCard.sh


echo "###################################### Generating .bna file ####################################"
composer archive create -t dir -n .


echo "################### Installing Productchain network onto Hyperledger Fabric #################### "
composer network install --card PeerAdmin@hlfv1 --archiveFile productchain-network@0.0.1.bna


echo "################################ Starting Productchain network ################################# "
composer network start --networkName productchain-network --networkVersion 0.0.1 --networkAdmin admin --networkAdminEnrollSecret adminpw --card PeerAdmin@hlfv1 --file networkadmin.card


echo "######################################### Importing Card ###################################### "
composer card import --file networkadmin.card


echo "########################################  Pinging network #####################################"
composer network ping --card admin@productchain-network


#echo "#####################################  Starting REST Server ################################### "
#composer-rest-server -c admin@productchain-network -n never -u true -w true


#composer network upgrade -c PeerAdmin@hlfv1 -n productchain -V 0.0.1
