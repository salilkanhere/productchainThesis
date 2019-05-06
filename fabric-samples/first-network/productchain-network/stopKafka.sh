cd "kafka_2.12-2.2.0"

xterm -e "bin/zookeeper-server-stop.sh config/zookeeper.properties"

xterm -e "bin/kafka-server-stop.sh config/server.properties"
xterm -e "bin/kafka-server-stop.sh config/server-1.properties"
xterm -e "bin/kafka-server-stop.sh config/server-2.properties"
xterm -e "bin/kafka-server-stop.sh config/server-3.properties"

rm -rf /tmp/zookeeper
rm -rf /tmp/kafka-logs


