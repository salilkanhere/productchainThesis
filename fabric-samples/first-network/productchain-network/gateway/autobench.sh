# Setup
ab -p setup.txt -T application/json -c 1 -n 1 http://localhost:3000/api/Setup

# Create HACCP
ab -p createHACCPInitial.txt -T application/json -c 1 -n 1 http://localhost:3000/api/CreateHACCP

ab -p createHACCP.txt -T application/json -c 1 -n 100 http://localhost:3000/api/CreateHACCP

# Create Batch
ab -p createBatchInitial.txt -T application/json -c 1 -n 1 http://localhost:3000/api/CreateBatch
ab -p createBatchInitial2.txt -T application/json -c 1 -n 1 http://localhost:3000/api/CreateBatch
ab -p createBatchInitial3.txt -T application/json -c 1 -n 1 http://localhost:3000/api/CreateBatch
ab -p createBatchInitial4.txt -T application/json -c 1 -n 1 http://localhost:3000/api/CreateBatch
ab -p createBatchInitial5.txt -T application/json -c 1 -n 1 http://localhost:3000/api/CreateBatch

ab -p createBatch.txt -T application/json -c 1 -n 100 http://localhost:3000/api/CreateBatch

# Create Batch Constituents

# Temperature 

# Transfer Batch
ab -p transferBatch.txt -T application/json -c 1 -n 10 http://localhost:3000/api/TransferBatch