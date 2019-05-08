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
async function temperacontracttureReading(temperatureReading) {  // eslint-disable-line no-unused-vars

    const batch = temperatureReading.batch;

    console.log('Adding temperature ' + temperatureReading.centigrade + ' to batch ' + batch.$identifier);

    // Check if the HACCP has been violated
    var violation = null;
    if (temperatureReading.centigrade < batch.haccp.minTemperature) {
        violation = "LOW_TEMP";
    } else if (temperatureReading.centigrade > batch.haccp.maxTemperature) {
        violation = "HIGH_TEMP";
    }

    // If violation has been detected, add it to the violations list
    if (violation != null) {
        if (batch.haccpViolations) {
            batch.haccpViolations.push(violation);
        } else {
            batch.haccpViolations = [violation];
        }
    }

    // Add temperature reading to the full list of temperatures
    if (batch.temperatureReadings) {
        batch.temperatureReadings.push(temperatureReading);
    } else {
        batch.temperatureReadings = [temperatureReading];
    }

    // add the temp reading to the shipment
    const batchRegistry = await getAssetRegistry('org.example.productchain.Batch');
    await batchRegistry.update(batch);

}

/**
 * A batch is being created
 * @param {org.example.productchain.CreateBatch} createBatch - the TemperatureReading transaction
 * @transaction
 */
async function createBatch(createBatch) {
    
    const factory = getFactory();
    const NS = 'org.example.productchain';
    const batch = factory.newResource(NS, 'Batch', createBatch.batchID);
    batch.creator = createBatch.creator;
    batch.currentOwner = createBatch.currentOwner;
    batch.type = createBatch.type;

    // Add contract to batch
    batch.haccp = factory.newRelationship(NS, createBatch.haccp.getType(), createBatch.haccp.getIdentifier());

    // In the case that this is a produce transaction
    if (createBatch.constituents) {
        batch.constituents = [];
        createBatch.constituents.forEach(constituent => {
            batch.constituents.push(factory.newRelationship(NS, constituent.getType(), constituent.getIdentifier()));
        }); 
    };

    // add the batch
    const batchRegistry = await getAssetRegistry(NS + '.Batch');
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
    const haccp = factory.newResource(NS, 'HACCP', createHACCP.haccpId);
    haccp.minTemperature = createHACCP.minTemperature;
    haccp.maxTemperature = createHACCP.maxTemperature;

    // add the haccp
    const haccpRegistry = await getAssetRegistry(NS + '.HACCP');
    await haccpRegistry.addAll([haccp]);
}


/**
 * A transfer of batch ownership
 * @param {org.example.productchain.TransferBatch} transferBatch - the TemperatureReading transaction
 * @transaction
 */
async function transferBatch(transferBatch) {
    
    const factory = getFactory();
    const NS = 'org.example.productchain';

    transferBatch.batch.currentOwner = transferBatch.newOwner;

    // add the growers
    const batchRegistry = await getAssetRegistry(NS + '.Batch');
    await batchRegistry.update(transferBatch.batch);

}



