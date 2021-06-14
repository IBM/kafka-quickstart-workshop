# Setting up Apache Kafka on a local machine

Follow these steps if you want to set up a 3-broker Kafka cluster on a single machine. This environment is not suitable for production, but it provides all the features necessary to complete this workshop.

## Starting ZooKeeper

The first step is to get ZooKeeper running. This is necessary in order to start Kafka:

We can start ZooKeeper with the default configuration file, by running this command:

```sh
./bin/zookeeper-server-start.sh ./config/zookeeper.properties
```

### Note for Window users:
If you're working on Windows with `bash`, you should do the following in order to start ZooKeeper:

1. Edit `config/zookeeper.properties` at line 16 by indicating the absolute path (Windows format) for the *dataDir*. For instance:

```properties
dataDir=C:\\Users\\<username>\\AppData\\Local\\Temp\\zookeeper
```

2. Then, run the following command:
```sh
./bin/windows/zookeeper-server-start.bat ./config/zookeeper.properties
```

We have now started a ZooKeeper ensemble consisting of a single server. Again, this is not suitable for production but it is enough to start a Kafka cluster.

## Configuring a local Kafka cluster

Kafka provides a default Kafka configuration file, `config/server.properties`. We will reuse this file and make a few changes.

1. Make 3 copies of `config/server.properties`:

    - `config/server0.properties`
    - `config/server1.properties`
    - `config/server2.properties`

2. In all 3 files:
    - Replace lines 74 to 76 with:

    ```properties
    offsets.topic.replication.factor=3
    transaction.state.log.replication.factor=3
    transaction.state.log.min.isr=3
    ```

    - Replace line 21 with `broker.id=<BROKER_ID>`
    - Replace line 31 with `listeners=PLAINTEXT://:9<BROKER_ID>92`
    - Replace line 60 with `log.dirs=/tmp/kafka<BROKER_ID>-logs` where `<BROKER_ID>` is the number in the file name, for example `2` for `config/server2.properties`.

    For example, in `config/server2.properties`:

    - `broker.id=2`
    - `listeners=PLAINTEXT://:9292`
    - `log.dirs=/tmp/kafka2-logs`  

## Starting the Kafka cluster

Now that we have all the required configurations, let's start our brokers:

```sh
./bin/kafka-server-start.sh ./config/server0.properties
```

Then in a different terminal window, run:

```sh
./bin/kafka-server-start.sh ./config/server1.properties
```

Finally in a different terminal window, run:
```sh
./bin/kafka-server-start.sh ./config/server2.properties
```

Congratulations, you've now started your Kafka cluster!

## Configuring the command line tools

The next step is to configure the Kafka command line tools to be able to connect to our Kafka cluster.

1. The configuration file

Create a new file that contains the following:

```properties
bootstrap.servers=localhost:9092,localhost:9192,localhost:9292
replication.factor=3
```

Set an environment variable, `CONFIG_FILE`, pointing to the location of this file. For example:

```sh
export CONFIG_FILE="/tmp/client.properties"
```

2. Bootstrap Servers

Set an environment variable, `BOOTSTRAP_SERVERS`, listing all your brokers.

Set the environment variable like this:

```sh
export BOOTSTRAP_SERVERS="localhost:9092,localhost:9192,localhost:9292"
```

## Back to Part 1

Return to [Part 1](../part1/README.md)
