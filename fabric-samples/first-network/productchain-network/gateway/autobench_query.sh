# Setup
ab -p setup.txt -T application/json -c 1 -n 1 http://localhost:3000/api/Setup

# Create HACCP
ab -p createHACCPInitial.txt -T application/json -c 1 -n 1 http://localhost:3000/api/CreateHACCP

# Create initial batch
ab -p createBatchInitial.txt -T application/json -c 1 -n 1 http://localhost:3000/api/CreateBatch




# TransferBatch, with 1 transfer
ab -p transferBatch_RB.txt -T application/json -c 1 -n 1 http://localhost:3000/api/TransferBatch
ab -n 50 -c 1 http://localhost:3000/api/TransferBatch?filter=%7B%22where%22%3A%7B%22batch%22%3A%20%22resource%3Aorg.example.productchain.Batch%231%22%7D%7D > kafkaQueryResults/transfer1.txt

# TransferBatch with 50
ab -p transferBatch_RB.txt -T application/json -c 1 -n 49 http://localhost:3000/api/TransferBatch
ab -n 50 -c 1 http://localhost:3000/api/TransferBatch?filter=%7B%22where%22%3A%7B%22batch%22%3A%20%22resource%3Aorg.example.productchain.Batch%231%22%7D%7D > kafkaQueryResults/transfer50.txt


# TransferBatch with 100
ab -p transferBatch_RB.txt -T application/json -c 1 -n 50 http://localhost:3000/api/TransferBatch
ab -n 50 -c 1 http://localhost:3000/api/TransferBatch?filter=%7B%22where%22%3A%7B%22batch%22%3A%20%22resource%3Aorg.example.productchain.Batch%231%22%7D%7D > kafkaQueryResults/transfer100.txt


# TransferBatch with 150
ab -p transferBatch_RB.txt -T application/json -c 1 -n 50 http://localhost:3000/api/TransferBatch
ab -n 50 -c 1 http://localhost:3000/api/TransferBatch?filter=%7B%22where%22%3A%7B%22batch%22%3A%20%22resource%3Aorg.example.productchain.Batch%231%22%7D%7D > kafkaQueryResults/transfer150.txt






# CreateBatch, with 1 batch
ab -n 50 -c 1 http://localhost:3000/api/CreateBatch?filter=%7B%22where%22%3A%7B%22batchID%22%3A%20%221%22%7D%7D > kafkaQueryResults/create1.txt

# CreateBatch, with 50 batch
ab -p createBatch.txt -T application/json -c 1 -n 50 http://localhost:3000/api/CreateBatch
ab -n 50 -c 1 http://localhost:3000/api/CreateBatch?filter=%7B%22where%22%3A%7B%22batchID%22%3A%20%221%22%7D%7D > kafkaQueryResults/create50.txt


# CreateBatch, with 100 batch
ab -p createBatch.txt -T application/json -c 1 -n 50 http://localhost:3000/api/CreateBatch
ab -n 50 -c 1 http://localhost:3000/api/CreateBatch?filter=%7B%22where%22%3A%7B%22batchID%22%3A%20%221%22%7D%7D > kafkaQueryResults/create100.txt


# CreateBatch, with 150 batch
ab -p createBatch.txt -T application/json -c 1 -n 50 http://localhost:3000/api/CreateBatch
ab -n 50 -c 1 http://localhost:3000/api/CreateBatch?filter=%7B%22where%22%3A%7B%22batchID%22%3A%20%221%22%7D%7D > kafkaQueryResults/create150.txt
