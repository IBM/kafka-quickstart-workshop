# Part 3

In this part we will look at Kafka Connect and how to stream data between external systems and Kafka. This follows on from [Part 2](../part2/README.md).

## Kafka Connect

Kafka Connect is a tool for scalably and reliably streaming data between Apache Kafka and other systems. It makes it simple to quickly define connectors that move large collections of data into and out of Kafka. It provides a framework to build connectors and manage them via a REST API.

It can run in 2 modes:
- **Standalone:** This mode is for development and runs in a single process.
- **Distributed:** This mode is suitable for production environment as it allows to scale dynamically and provide fault tolerance.

In this workshop, we will set Connect up using the distributed mode.

## Importing data into Kafka from a file

To keep things simple, we will use one of the built-in connector: `FileStreamSourceConnector`. This connector imports data from a file into Kafka. The process to get a connector up and running is very similar for all connectors so it's a great way to get started and learn about Kafka Connect.

## Starting the Connect runtime

In distributed mode, the first step is to start the Connect runtime. We need to create a properties file with the correct details to configure Connect and enable the runtime to connect to our Event Streams instance.

Create a file with the following contents, replacing the `<BOOTSTRAP_SERVERS>` and `<API_KEY>` tags with your cluster credentials.
```properties
# connectivity settings for the runtime
bootstrap.servers=<BOOTSTRAP_SERVERS>
sasl.jaas.config=org.apache.kafka.common.security.plain.PlainLoginModule required username="token" password="<APIKEY>";
security.protocol=SASL_SSL
sasl.mechanism=PLAIN
ssl.protocol=TLSv1.2
ssl.enabled.protocols=TLSv1.2
ssl.endpoint.identification.algorithm=HTTPS

consumer.sasl.jaas.config=org.apache.kafka.common.security.plain.PlainLoginModule required username="token" password="<APIKEY>";
consumer.security.protocol=SASL_SSL
consumer.sasl.mechanism=PLAIN

producer.sasl.jaas.config=org.apache.kafka.common.security.plain.PlainLoginModule required username="token" password="<APIKEY>";
producer.security.protocol=SASL_SSL
producer.sasl.mechanism=PLAIN

# unique name for the cluster, used in forming the Connect cluster group. Note that this must not conflict with consumer group IDs
group.id=connect_cluster

# The converters specify the format of data in Kafka and how to translate it into Connect data. Every Connect user will
# need to configure these based on the format they want their data in when loaded from or stored into Kafka
key.converter=org.apache.kafka.connect.converters.ByteArrayConverter
value.converter=org.apache.kafka.connect.converters.ByteArrayConverter

# Topic to use for storing offsets
offset.storage.topic=connect_offsets
offset.storage.replication.factor=3

# Topic to use for storing connector and task configurations
config.storage.topic=connect_configs
config.storage.replication.factor=3

# Topic to use for storing statuses
status.storage.topic=connect_status
status.storage.replication.factor=3
```

By default, the runtime will use port `8083`. You can change this port by setting `rest.port=<PORT>`. The rest of this part uses `8083`.

Let's start the runtime. The following command starts the Connect runtime locally:
```sh
./bin/connect-distributed.sh ./config/connect-distributed.properties
```

We can validate the runtime is correctly started by using its REST API. The following command returns the listed of available connectors:
```sh
curl http://localhost:8083/connector-plugins
```

Ensure it contains `org.apache.kafka.connect.file.FileStreamSourceConnector`.

[TODO SMT]

[TODO run in IKS?]

## Starting the connector

Now that the runtime is running, we are now able to start connectors via the REST API.

In order to start the connector, we need some configuration. Create a file, with the following content:
```json
{
  "name": "file-source",
  "config": {
    "connector.class": "org.apache.kafka.connect.file.FileStreamSourceConnector",
    "tasks.max": "1",
    "file": "file-source.txt",
    "topics": "streams-plaintext-input"
  }
}
```

This instructs the runtime to start the `FileStreamSourceConnector` and make it read a file called `file-source.txt`. It should send each line of this file as a message to the `streams-plaintext-input` topic. Finally `tasks.max` allows to configure how many tasks Connect should start.

Let's start our connector:

```sh
> curl -X POST -H "Content-Type: application/json" http://localhost:8083/connectors \
  --data "@<CONNECTOR_CONFIG_FILE>"
```

Where `<CONNECTOR_CONFIG_FILE>` is the path of the JSON file we created above.

We can verify the connector is running:
```sh
> curl http://localhost:8083/connectors/file-source/
```

## Testing the connector

<TODO>

Start consumer on `streams-plaintext-input`

Edit `file-source.txt`

## Simple Message Transform

[ TODO explain SMT ]

## Next Steps

Continue to [part 4](../part4/README.md)
