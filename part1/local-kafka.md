# Local Kafka Setup

## Running a local Kafka cluster

<TODO> steps for starting a kafka cluster locally

1) Starting ZooKeeper

```sh
./bin/zookeeper-server-start.sh ./config/zookeeper.properties
```

2) Starting 3 Kafka brokers

```sh
./bin/kafka-server-start.sh ./config/server.properties
```

```sh
./bin/kafka-server-start.sh ./config/server1.properties
```

```sh
./bin/kafka-server-start.sh ./config/server2.properties
```

## Configuring the command line tools

The next step is to configure the Kafka command line tools to be able to connect to our Kafka cluster. 

1) The configuration file

Create a new file that contains the following:
```properties
bootstrap.servers=localhost:9092,localhost:9192,localhost:9292
replication.factor=3
```

Set an environment variable, `CONFIG_FILE`, pointing to the location of this file. For example:
```sh
export CONFIG_FILE="/tmp/client.properties"
```

2) Bootstrap Servers

Set an environment variable, `BOOTSTRAP_SERVERS`, listing all your brokers.

Set:
```sh
export BOOTSTRAP_SERVERS="localhost:9092,localhost:9192,localhost:9292"
```

## Next Steps

Continue to [part 2](../part2/README.md)
