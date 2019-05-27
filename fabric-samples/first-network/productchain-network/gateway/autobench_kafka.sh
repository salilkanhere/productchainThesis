# Setup
ab -p setup.txt -T application/json -c 1 -n 1 http://localhost:3000/api/Setup

# Create HACCP
ab -p createHACCPInitial.txt -T application/json -c 1 -n 1 http://localhost:3000/api/CreateHACCP

ab -p createHACCP.txt -T application/json -c 1 -n 50 http://localhost:3000/api/CreateHACCP > kafkaResults/createHACCP_results.txt

# Create Batch
ab -p createBatchInitial.txt -T application/json -c 1 -n 1 http://localhost:3000/api/CreateBatch
ab -p createBatchInitial2.txt -T application/json -c 1 -n 1 http://localhost:3000/api/CreateBatch
ab -p createBatchInitial3.txt -T application/json -c 1 -n 1 http://localhost:3000/api/CreateBatch
ab -p createBatchInitial4.txt -T application/json -c 1 -n 1 http://localhost:3000/api/CreateBatch
ab -p createBatchInitial5.txt -T application/json -c 1 -n 1 http://localhost:3000/api/CreateBatch

ab -p createBatch.txt -T application/json -c 1 -n 50 http://localhost:3000/api/CreateBatch > kafkaResults/createBatch_results.txt

# Create Batch Constituents
ab -p createBatch_1con.txt -T application/json -c 1 -n 50 http://localhost:3000/api/CreateBatch > kafkaResults/createBatch_1con_results.txt
ab -p createBatch_2con.txt -T application/json -c 1 -n 50 http://localhost:3000/api/CreateBatch > kafkaResults/createBatch_2con_results.txt
ab -p createBatch_3con.txt -T application/json -c 1 -n 50 http://localhost:3000/api/CreateBatch > kafkaResults/createBatch_3con_results.txt
ab -p createBatch_4con.txt -T application/json -c 1 -n 50 http://localhost:3000/api/CreateBatch > kafkaResults/createBatch_4con_results.txt
ab -p createBatch_5con.txt -T application/json -c 1 -n 50 http://localhost:3000/api/CreateBatch > kafkaResults/createBatch_5con_results.txt

# Temperature 
ab -p temperatureReading.txt -T application/json -c 1 -n 50 http://localhost:3000/api/TemperatureReading > kafkaResults/temperatureReading_results.txt
ab -p temperatureReadingInvalid.txt -T application/json -c 1 -n 50 http://localhost:3000/api/TemperatureReading > kafkaResults/temperatureReadingInvalid_results.txt

# Transfer Batch
ab -p transferBatch_RB.txt -T application/json -c 1 -n 50 http://localhost:3000/api/TransferBatch > kafkaResults/transferBatch_RB_results.txt
ab -p transferBatch_nRB.txt -T application/json -c 1 -n 50 http://localhost:3000/api/TransferBatch > kafkaResults/transferBatch_nRB_results.txt
ab -p transferBatch_RnB.txt -T application/json -c 1 -n 50 http://localhost:3000/api/TransferBatch > kafkaResults/transferBatch_RnB_results.txt
ab -p transferBatch_nRnB.txt -T application/json -c 1 -n 50 http://localhost:3000/api/TransferBatch > kafkaResults/transferBatch_nRnB_results.txt