# Part 4

In this part we will learn about Kafka Streams and how it can be used to process streams of data in real time. This follows on from [Part 3](../part3/README.md).

## Kafka Streams

Kafka Streams is a client library for building applications and microservices, where the input and output data are stored in Kafka clusters. It combines the simplicity of writing and deploying standard Java and Scala applications on the client side with the benefits of Kafka's server-side cluster technology.



## WordCountDemo sample application

One of the bbuilt-in sample Streams application is [WordCountDemo](https://github.com/apache/kafka/blob/2.5/streams/examples/src/main/java/org/apache/kafka/streams/examples/wordcount/WordCountDemo.java).

## Prerequisites

- Create output topic
- Configure WordCountDemo
- Build

## Running WordCountDemo

```sh
> bin/kafka-run-class.sh org.apache.kafka.streams.examples.wordcount.WordCountDemo
```

## Check the result

```sh
> bin/kafka-console-consumer.sh --bootstrap-server $BOOTSTRAP_SERVERS \
  --consumer.config $CONFIG_FILE \
  --topic streams-wordcount-output \
  --from-beginning \
  --formatter kafka.tools.DefaultMessageFormatter \
  --property print.key=true \
  --property print.value=true \
  --property key.deserializer=org.apache.kafka.common.serialization.StringDeserializer \
  --property value.deserializer=org.apache.kafka.common.serialization.LongDeserializer
```