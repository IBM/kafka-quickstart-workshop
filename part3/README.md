# Part 3 - Integrating data with Kafka Connect

In this part of the workshop, we will look at Kafka Connect and how to stream data between external systems and Kafka. Make sure that you've completed Part 2, since this part follows on from [Part 2](../part2/README.md).

## Kafka Connect

[Kafka Connect](https://kafka.apache.org/documentation/#connect) is a tool for scalably and reliably streaming data between Apache Kafka and other systems. It makes it simple to quickly define connectors that move large collections of data into and out of Kafka. It provides a framework to build connectors and manage them via a [REST API](https://kafka.apache.org/documentation/#connect_rest).

Kafka Connect can run in 2 modes:
- **Standalone:** This mode is for development and runs in a single process.
- **Distributed:** This mode is suitable for production environments as it allows scaling dynamically and provides fault tolerance.

In this workshop, we will setup Kafka Connect using the distributed mode.

## Importing data into Kafka from a file

To keep things simple, we will use one of the built-in connectors: [`FileStreamSourceConnector`](https://github.com/apache/kafka/blob/trunk/connect/file/src/main/java/org/apache/kafka/connect/file/FileStreamSourceConnector.java). This connector imports data from a file into Kafka. The process to get a connector up and running is very similar for all connectors so it's a great way to get started and learn about Kafka Connect.

## Starting the Kafka Connect runtime

In distributed mode, the first step is to start the Kafka Connect runtime. We need to create a properties file with the correct details to configure Kafka Connect and enable the runtime to connect to our Kafka cluster.

In order to configure Kafka Connect, follow the steps for your Kafka environment:
- For [Event Streams](./event-streams.md)
- For [Local Kafka](./local-kafka.md)

By default, the runtime exposes its REST API on port `8083`. You can change this port by setting `rest.port=<PORT>`. The rest of this workshop assumes that the port is `8083`.

Let's start the Connect runtime using the following command:

```sh
> bin/connect-distributed.sh ./config/connect-distributed.properties
```

We can validate that the Kafka Connect runtime is correctly started by using its REST API. The following command returns the listed of available connectors:

```sh
> curl http://localhost:8083/connector-plugins
```

Ensure it contains at least `org.apache.kafka.connect.file.FileStreamSourceConnector`.

## Configuring the connector

Now that the runtime is running, we are able to start connectors by using the REST API.

In order to start the connector, we need some configurations. Create a file, with the following content:

```json
{
  "name": "file-source",
  "config": {
    "connector.class": "org.apache.kafka.connect.file.FileStreamSourceConnector",
    "tasks.max": "1",
    "file": "/tmp/file-source.txt",
    "topic": "streams-plaintext-input"
  }
}
```

This instructs the runtime to start the `FileStreamSourceConnector` connector and make it read a file called `/tmp/file-source.txt`. It will send each line of this file as a message to the `streams-plaintext-input` topic. Finally, `tasks.max` allows to configure how many tasks Kafka Connect should start, which is just 1 in our scenario.

## Creating the topic

To enable our connector to work, we need to create the `streams-plaintext-input` topic.

```sh
> bin/kafka-topics.sh --bootstrap-server ${BOOTSTRAP_SERVERS} \
  --command-config ${CONFIG_FILE} --create --replication-factor 3 --partitions 1 --topic streams-plaintext-input
```

You should see this output:

```sh
Created topic streams-plaintext-input.
```

## Creating and populating the source file

We create the source file and put some content in it:

```sh
> echo "first line of content" > /tmp/file-source.txt
> echo "another line" >> /tmp/file-source.txt
```

## Starting the connector

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

Now that the connector is running, any line added to `/tmp/file-source.txt` will end up in our topic.

Start a consumer on `streams-plaintext-input`:
```sh
> bin/kafka-console-consumer.sh --bootstrap-server ${BOOTSTRAP_SERVERS} \
  --consumer.config ${CONFIG_FILE} --topic streams-plaintext-input --from-beginning
```

While the consumer is running, we can add more lines to our file and they should be consumed immediately.

```sh
> echo "adding more content" >> /tmp/file-source.txt
```

## Summary

In just a few commands, we have demonstrated how to use the Kafka Connect framework. There is a wide ecosystem of connectors built by the community that enable integrating many systems with Kafka without having to write any code. All connectors are managed the same way with the Kafka Connect REST API, so everything you've learned in this workshop is applicable to real deployments.

## Going further

Kafka comes by default with a few connectors to integrate with:

- Files: The [`FileStreamSourceConnector`](https://github.com/apache/kafka/blob/trunk/connect/file/src/main/java/org/apache/kafka/connect/file/FileStreamSourceConnector.java) and [`FileStreamSinkConnector`](https://github.com/apache/kafka/blob/trunk/connect/file/src/main/java/org/apache/kafka/connect/file/FileStreamSinkConnector.java) respectively enable to import and export data between files and Kafka.

- Kafka: The [`MirrorSourceConnector`](https://github.com/apache/kafka/blob/trunk/connect/mirror/src/main/java/org/apache/kafka/connect/mirror/MirrorSourceConnector.java), [`MirrorCheckpointConnector`](https://github.com/apache/kafka/blob/trunk/connect/mirror/src/main/java/org/apache/kafka/connect/mirror/MirrorCheckpointConnector.java) and [`MirrorHeartbeatConnector`](https://github.com/apache/kafka/blob/trunk/connect/mirror/src/main/java/org/apache/kafka/connect/mirror/MirrorHeartbeatConnector.java) are known as [Mirror Maker 2](https://github.com/apache/kafka/tree/trunk/connect/mirror) and enable mirroring data between Kafka clusters. This can be used to set up disaster recovery environments, for example.

IBM provides the following connectors:

- [MQ Sink](https://github.com/ibm-messaging/kafka-connect-mq-sink)
- [MQ Source](https://github.com/ibm-messaging/kafka-connect-mq-source)
- [Cloud Object Storage Sink](https://github.com/ibm-messaging/kafka-connect-ibmcos-sink)

We also provide a Docker image with a Kubernetes YAML file to easily deploy Kafka Connect in [IBM Kubernetes Service](https://www.ibm.com/cloud/container-service/) in the [Event Streams samples repository](https://github.com/ibm-messaging/event-streams-samples/tree/master/kafka-connect).

## Next Steps

Continue to [Part 4](../part4/README.md).
