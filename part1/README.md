# Part 1

## Kafka overview

Apache Kafka is a distributed streaming platform. It provides publish-subscribe APIs and can store and process streams of records at large scale.

Kafka is made of the following components:
- Cluster: One of more Kafka servers 
- Producer: Client to send records into Kafka
- Consumer: Client to read records from Kafka
- Admin: Client to manage Kafka clusters
- Connect: Runtime for Sink and Source Connectors to stream data between external systems and Kafka
- Streams: Client to process streams of records in real time

![Kafka Platform](./kafka-platform.png)

## Workshop objectives

In this workshop we will build a small event streaming pipeline using the tools and samples built-in Apache Kafka.

![Workshop pipeline](./pipeline.png)

Our input data comes from a file. Kafka Connect streams it into a topic in Kafka. Finally Kafka Streams processes the data and writes the output into a new topic.

## Prerequisites

In this workshop, we will use the Kafka command line tools.

[Download](http://kafka.apache.org/downloads) the latest binary package from the [Apache Kafka website](http://kafka.apache.org/) and uncompress it. For example, for Kafka 2.5.0:

```sh
tar -xzf kafka_2.13-2.5.0.tgz
cd kafka_2.13-2.5.0
```

For the server side, we will use IBM Event Streams. This workshop requires creating several topics so it will incur a fee.

This workshop assumes you are running a Unix based platform like macOS or Linux. If you are on Windows, use the scripts that are in the `bin/windows` directory.

### Configuring the command line tools

The first step is to configure the Kafka command line tools to be able to connect to our Kafka cluster. 

To retrieve your Event Streams credentials, navigate to the instance in IBM Cloud. Click on the Service Credentials tab and select New Credentials. Then click on View Credentials. This panel contains all the information required to connect to your Event Streams instance.

1) The configuration file

Create a new file that contains the following:
```
sasl.jaas.config=org.apache.kafka.common.security.plain.PlainLoginModule required username="token" password="<APIKEY>";
security.protocol=SASL_SSL
sasl.mechanism=PLAIN
ssl.protocol=TLSv1.2
ssl.enabled.protocols=TLSv1.2
ssl.endpoint.identification.algorithm=HTTPS
```
Replace `<APIKEY>` by the value of the `apikey` field in your Service Credentials.

Set an environment variable, `CONFIG_FILE`, pointing to the location of this file. For example:
```sh
export CONFIG_FILE="/tmp/client.properties"
```

2) Bootstrap Servers

In your credentials, take note of the `kafka_brokers_sasl` field, these are the bootstrap servers that are used to connect to the cluster. All commands will require the these values to be passed in the CSV format. 

Set an environment variable, `BOOTSTRAP_SERVERS`, listing all your brokers. For example, for:
```json
"kafka_brokers_sasl": [
  "broker-2-<...>.eventstreams.cloud.ibm.com:9093",
  "broker-0-<...>.eventstreams.cloud.ibm.com:9093",
  "broker-1-<...>.eventstreams.cloud.ibm.com:9093"
],
```

Set:
```sh
export BOOTSTRAP_SERVERS="broker-2-<...>.eventstreams.cloud.ibm.com:9093,broker-0-<...>.eventstreams.cloud.ibm.com:9093,broker-1-<...>.eventstreams.cloud.ibm.com:9093"
```
