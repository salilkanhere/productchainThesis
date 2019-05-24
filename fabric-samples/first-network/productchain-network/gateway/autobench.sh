# Setup
ab -p setup.txt -T application/json -c 1 -n 1 http://localhost:3000/api/Setup

# Create HACCP
ab -p createHACCPInitial.txt -T application/json -c 1 -n 1 http://localhost:3000/api/CreateHACCP

ab -p createHACCP.txt -T application/json -c 1 -n 100 http://localhost:3000/api/CreateHACCP > results/createHACCP_results.txt

# Create Batch
ab -p createBatchInitial.txt -T application/json -c 1 -n 1 http://localhost:3000/api/CreateBatch
ab -p createBatchInitial2.txt -T application/json -c 1 -n 1 http://localhost:3000/api/CreateBatch
ab -p createBatchInitial3.txt -T application/json -c 1 -n 1 http://localhost:3000/api/CreateBatch
ab -p createBatchInitial4.txt -T application/json -c 1 -n 1 http://localhost:3000/api/CreateBatch
ab -p createBatchInitial5.txt -T application/json -c 1 -n 1 http://localhost:3000/api/CreateBatch

ab -p createBatch.txt -T application/json -c 1 -n 100 http://localhost:3000/api/CreateBatch > results/createBatch_results.txt

# Create Batch Constituents
ab -p createBatch_1con.txt -T application/json -c 1 -n 10 http://localhost:3000/api/CreateBatch > results/createBatch_1con_results.txt
ab -p createBatch_2con.txt -T application/json -c 1 -n 10 http://localhost:3000/api/CreateBatch > results/createBatch_2con_results.txt
ab -p createBatch_3con.txt -T application/json -c 1 -n 10 http://localhost:3000/api/CreateBatch > results/createBatch_3con_results.txt
ab -p createBatch_4con.txt -T application/json -c 1 -n 10 http://localhost:3000/api/CreateBatch > results/createBatch_4con_results.txt
ab -p createBatch_5con.txt -T application/json -c 1 -n 10 http://localhost:3000/api/CreateBatch > results/createBatch_5con_results.txt

# Temperature 
ab -p temperatureReading.txt -T application/json -c 1 -n 20 http://localhost:3000/api/TemperatureReading > results/temperatureReading_results.txt
ab -p temperatureReadingInvalid.txt -T application/json -c 1 -n 20 http://localhost:3000/api/TemperatureReading > results/temperatureReadingInvalid_results.txt

# Transfer Batch
ab -p transferBatch_RB.txt -T application/json -c 1 -n 10 http://localhost:3000/api/TransferBatch > results/transferBatch_RB_results.txt
ab -p transferBatch_nRB.txt -T application/json -c 1 -n 10 http://localhost:3000/api/TransferBatch > results/transferBatch_nRB_results.txt
ab -p transferBatch_RnB.txt -T application/json -c 1 -n 10 http://localhost:3000/api/TransferBatch > results/transferBatch_RnB_results.txt
ab -p transferBatch_nRnB.txt -T application/json -c 1 -n 10 http://localhost:3000/api/TransferBatch > results/transferBatch_nRnB_results.txt