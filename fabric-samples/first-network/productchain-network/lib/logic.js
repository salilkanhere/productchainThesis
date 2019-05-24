/*
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

'use strict';


/* global getParticipantRegistry getAssetRegistry getFactory */

/**transaction TemperatureReading extends BatchTransaction {

 * A temperature reading has been received for a shipment
 * @param {org.example.productchain.TemperatureReading} temperatureReading - the TemperatureReading transaction
 * @transaction
 */
async function temperaureReading(temperatureReading) {  // eslint-disable-line no-unused-vars

    const factory = getFactory();
    const NS = 'org.example.productchain';
    const batch = temperatureReading.batch;

    console.log("About to calculate if batch exists");
    var batchExists = await getAssetRegistry(NS + '.Batch')
    .then(function (batchAssetRegistry) {
      return batchAssetRegistry.exists(batch.getIdentifier());
    })
    .then(function (exists) {
      return exists;
    })
    .catch(function (error) {
      // Add optional error handling here.
      console.log('ERROR: ' + error);
    });

    if (!batchExists) {
        throw new Error ('Batch ' + batch.getIdentifier() + ' does not exist');
    }

    // Check if the HACCP has been violated
    var violation = null;
    if (temperatureReading.centigrade < batch.haccp.minTemperature) {
        violation = "LOW_TEMP";
    } else if (temperatureReading.centigrade > batch.haccp.maxTemperature) {
        violation = "HIGH_TEMP";
    }

    // If violation has been detected, emit TemperatureViolation event
    if (violation != null) {
        const temperatureViolationEvent = factory.newEvent(NS, 'TemperatureViolation');
        temperatureViolationEvent.batch = factory.newRelationship(NS, batch.getType(), batch.getIdentifier());
        temperatureViolationEvent.temperatureReading = temperatureReading;
        temperatureViolationEvent.violation = violation;
        emit(temperatureViolationEvent);
    }

}

/**
 * A batch is being created
 * @param {org.example.productchain.CreateBatch} createBatch - the TemperatureReading transaction
 * @transaction
 */
async function createBatch(createBatch) {
    
    const factory = getFactory();
    const NS = 'org.example.productchain';
    const batchRegistry = await getAssetRegistry(NS + '.Batch');

    if (createBatch.batchID == '' || createBatch.batchID == '_') {
        createBatch.batchID = Math.floor((Math.random() * 10000) + 1).toString(10);
    }

    const batch = factory.newResource(NS, 'Batch', createBatch.batchID);
    batch.currentOwner = createBatch.currentOwner;
    batch.type = createBatch.type;

    // Add contract to batch

    var HACCPExists = await getAssetRegistry(NS + '.HACCP')
    .then(function (hccpAssetRegistry) {
      return hccpAssetRegistry.exists(batch.type);
    })
    .then(function (exists) {
      return exists;
    })
    .catch(function (error) {
      // Add optional error handling here.
      console.log('ERROR: ' + error);
    });


    if (HACCPExists) {
        batch.haccp = factory.newRelationship(NS, 'HACCP', batch.type.toString());  
    } else {
        throw new Error ('No compatible HACCP of type ' + batch.type.toString());
    }

    // In the case that this is a produce transaction
    if (createBatch.constituents) {
        batch.constituents = [];
        
        for (constituent of createBatch.constituents) {

            var constituentExists = await getAssetRegistry(NS + '.Batch')
            .then(function (batchAssetRegistry) {
              return batchAssetRegistry.exists(constituent.getIdentifier());
            })
            .then(function (exists) {
              return exists;
            })
            .catch(function (error) {
              // Add optional error handling here.
              console.log('ERROR: ' + error);
            });

            if (constituentExists) {
                batch.constituents.push(factory.newRelationship(NS, constituent.getType(), constituent.getIdentifier()));
            } else {
                throw new Error ('Batch ' + constituent.getIdentifier() + ' does not exist - ensure all constituents are in this region');
            }
            
        }; 
    };

    // add the batch
    await batchRegistry.addAll([batch]);

}


/**
 * A batch is being created
 * @param {org.example.productchain.CreateHACCP} createHACCP - create an asset called HACCP
 * @transaction
 */
async function createHACCP(createHACCP) {
    const factory = getFactory();
    const NS = 'org.example.productchain';

    var id = createHACCP.type;
    if (id == 'TEST') {
        id = id + '_' + Math.floor((Math.random() * 10000) + 1).toString(10);
    }

    var HACCPExists = await getAssetRegistry(NS + '.HACCP')
    .then(function (hccpAssetRegistry) {
        return hccpAssetRegistry.exists(id);
    })
    .then(function (exists) {
        return exists;
    })
    .catch(function (error) {
        // Add optional error handling here.
        console.log('ERROR: ' + error);
    });


    if (HACCPExists) {

        var existingHACCP = await getAssetRegistry(NS + '.HACCP')
        .then(function (hccpAssetRegistry) {
            return hccpAssetRegistry.get(id);
        })
        .then(function (exists) {
            return exists;
        })
        .catch(function (error) {
            // Add optional error handling here.
            console.log('ERROR: ' + error);
        });

        var HACCPExists = await getAssetRegistry(NS + '.HACCP')
        .then(function (hccpAssetRegistry) {
            existingHACCP.maxTemperature = createHACCP.maxTemperature;
            existingHACCP.minTemperature = createHACCP.minTemperature;
            return hccpAssetRegistry.update(existingHACCP);
        })
        .then(function (exists) {
            return exists;
        })
        .catch(function (error) {
            // Add optional error handling here.
            console.log('ERROR: ' + error);
        });

    } else {

        // Since one HACCP exists for each type of product, we can make the unique identifier just the type
        const haccp = factory.newResource(NS, 'HACCP', id);
        haccp.minTemperature = createHACCP.minTemperature;
        haccp.maxTemperature = createHACCP.maxTemperature;
        haccp.type = createHACCP.type;

        // add the haccp
        const haccpRegistry = await getAssetRegistry(NS + '.HACCP');
        await haccpRegistry.addAll([haccp]);

    }
}


/**
 * A transfer of batch ownership
 * @param {org.example.productchain.TransferBatch} transferBatch - the TemperatureReading transaction
 * @transaction
 */
async function transferBatch(transferBatch) {

    const factory = getFactory();
    const NS = 'org.example.productchain';
    const batchRegistry = await getAssetRegistry(NS + '.Batch');
    const haccpRegistry = await getAssetRegistry(NS + '.HACCP');
    const batch = transferBatch.batch;
    console.log(batch);

    // REGION
    console.log("About to calculate current region");
    var currRegion = await getAssetRegistry(NS + '.CurrentRegion')
    .then(function (regionAssetRegistry) {
      return regionAssetRegistry.get('CURR');
    })
    .then(function (region) {
      return region;
    })
    .catch(function (error) {
      // Add optional error handling here.
      console.log('ERROR: ' + error);
    });

    //BATCH
    console.log("About to calculate if batch exists");
    var batchExists = await getAssetRegistry(NS + '.Batch')
    .then(function (batchAssetRegistry) {
      return batchAssetRegistry.exists(batch.getIdentifier());
    })
    .then(function (exists) {
      return exists;
    })
    .catch(function (error) {
      // Add optional error handling here.
      console.log('ERROR: ' + error);
    });



    // REGION LOGISTICS
    // Transfer batch can be done across regions
    // If the transfer is in the same region
    //      1. exists = update it
    //      2. doesnt exist = create new batch
    // otherwise, only delete if its a different region, but it exists in this one
    if (currRegion.region == transferBatch.region) {

        if (batchExists) {
            batch.currentOwner = transferBatch.newOwner;
            await batchRegistry.update(batch);
        
        } else {
            console.log("Creating batch");
            const newBatch = factory.newResource(NS, 'Batch', batch.getIdentifier());
            newBatch.currentOwner = transferBatch.newOwner;
            newBatch.type = transferBatch.type;
        
            // Add contract to batch
            if (haccpRegistry.exists(transferBatch.type.toString())) {
                newBatch.haccp = factory.newRelationship(NS, 'HACCP', transferBatch.type.toString());  
            } else {
                throw new Error ('No compatible HACCP of type ' + transferBatch.type.toString());
            }

            await batchRegistry.addAll([newBatch]);
            
        }
    } else {
        if (batchExists) {
            await batchRegistry.remove(batch.getIdentifier());
        } else {
            throw new Error ('Transfer transaction not does not apply to this region');
        }
    }
}


/**
 * A transfer of batch ownership
 * @param {org.example.productchain.Setup} setup
 * @transaction
 */
async function setup(setup) {
    const factory = getFactory();
    const NS = 'org.example.productchain';
    const currentRegion = factory.newResource(NS, 'CurrentRegion', 'CURR');
    currentRegion.region = setup.region;
    const regionRegistry = await getAssetRegistry(NS + '.CurrentRegion');
    await regionRegistry.addAll([currentRegion]);
}