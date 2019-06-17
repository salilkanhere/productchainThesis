# Top Level Application

The top level application was written in Python using Flask. Flask is a micro-framework for Python that has a simple but extensible core for developing web applications. The purpose of the top level application is to pass communications between Productchain clients and all the shards of the network. It acts as an abstraction layer from the blockchain network.

The application is fairly simple and features 5 different forms - one for each of the types of transactions or queries that would be commonly made by a client. Some of the forms require the client to specify the region in the form, however, in the future this could be automated to detect region based on the clients IP address. The functionality is as follows:


- *Create Batch*: allows the user to create a batch in a specified region
- *Create HACCP*: allows the user to define a HACCP contract (currently only 'meat' or 'milk'). This is not region specific and creates the HACCP in every shard of the network.
- *Transfer Batch*: allows a user to transfer an existing batch between different owners (such as in the case of a batch purchase). This specifies a region. There are two things that can happen depending on the specified region on the form and the region in which the batch in question currently resides. The first is if the specified region is the same as the current region, a standard transfer of owner occurs. The second occurs if the specified region is different from the current one - in this case, the current regional server deletes the asset instance and the specified regional server creates a new asset with the same value. Thus an asset is transferred across regions, and as a result, across servers.
- *Query Product Story*: compiles a chronological list from most recent to least recent of all the create and transfer transactions in a specific batches history. Batches are queried for by ID.
- *Query Temperature*: returns a complete list of all temperature readings submitted in reference to that batch. The list also highlights the HACCP violations at the top for quick reference - if there are any.

## Code Structure

The main pages and behaviours are defined in *main.py*
The specific form stuctures are defined in *forms.py*
The behaviour of each form is defined in *utils.py*
The HTML elements are defined in *templates/*