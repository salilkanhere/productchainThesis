rm -rf /tmp/zookeeper
rm -rf /tmp/kafka-logs

cd "kafka_2.12-2.2.0"

echo "Starting zookeeper"
xterm -hold -e "bin/zookeeper-server-start.sh config/zookeeper.properties" &

sleep 3

echo "Starting 4 nodes"
xterm -hold -e "bin/kafka-server-start.sh config/server.properties" &
xterm -hold -e "bin/kafka-server-start.sh config/server-1.properties" &
xterm -hold -e "bin/kafka-server-start.sh config/server-2.properties" &
xterm -hold -e "bin/kafka-server-start.sh config/server-3.properties" &

sleep 5

bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 3 --partitions 1 --topic orderer
