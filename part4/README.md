# Part 4

In this part we will learn about Kafka Streams and how it can be used to process streams of data in real time. This follows on from [Part 3](../part3/README.md).

## Kafka Streams

[Kafka Streams](https://kafka.apache.org/documentation/streams/) is a client library for building applications and microservices, where the input and output data are stored in Kafka clusters. It combines the simplicity of writing and deploying standard Java and Scala applications on the client side with the benefits of Kafka's server-side cluster technology.


## WordCountDemo sample application

One of the built-in sample Streams application is [WordCountDemo](https://github.com/apache/kafka/blob/2.5/streams/examples/src/main/java/org/apache/kafka/streams/examples/wordcount/WordCountDemo.java).

This sample application consumes an input topic, count how many times words appear and write the result back into another topic

Let's use `WordCountDemo` to count word in our topic `streams-plaintext-input`.


## Running WordCountDemo

We start `WordCountDemo` passing our configuration file.

```sh
> bin/kafka-run-class.sh org.apache.kafka.streams.examples.wordcount.WordCountDemo $CONFIG_FILE
```

The Streams application will run until interrupted, for example by pressing `CTRL+C`.

## Check the result

By default, `WordCountDemo` writes its output in the `streams-wordcount-output` topic. We can use a consumer to check the result:
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