# Part 2 - Sending and consuming messages

In this part, we will review the most basics Kafka concepts, and start out by sending and consuming messages. This follows on from [Part 1](../part1/README.md).

## Creating a topic

A **topic** is a category or feed name to which records are published. To create a topic we need 4 things:

    --topic **Name:** A topic is referred by its name. It has to be unique within a cluster. Valid characters are alphanumerics plus a few symbols (`.`, `_` and `-`).
    --partitions **Partition count:** Partitions are the units of scalability. Having multiple partitions allows you to distribute a topic across several brokers. Kafka only guarantees ordering within a partition.
    --replication-factor **Replication factor:** This specifies how many copies of the data are kept in the cluster. This value should not exceed the number of Kafka servers in the cluster. Let's set that to `3` for now.
    - **Configurations:** [Some configurations](https://kafka.apache.org/documentation/#topicconfigs) can be applied per topic. If not specified, the broker defaults are used.
    - bootstrap.servers is a comma-separated list of host and port pairs that are the addresses of the Kafka brokers in a "bootstrap" Kafka cluster that a Kafka client connects to initially to bootstrap itself.
    
Let's create our first topic. In a terminal, run the following command:

```sh
C:\kafka_2.13-2.7.0>bin\windows\kafka-topics.bat --bootstrap-server "localhost:9092,localhost:9192,localhost:9292" --create --replication-factor 3 --partitions 2 --topic my-first-topic
```

You should see this output: `Created topic my-first-topic.`

We can now see our topic if we run the list topics command:
```sh
> bin\windows\kafka-topics.bat --bootstrap-server "localhost:9092,localhost:9192,localhost:9292" --list
```

You should see this output:  `my-first-topic`

## Sending some messages

Kafka comes with a command line **producer** that takes data from a file or from standard input and sends it out as messages to the Kafka cluster. By default, each line will be sent as a separate message.

Run the producer, and then type a few messages into the console to send to the server.

```sh
C:\kafka_2.13-2.7.0>bin\windows\kafka-console-producer.bat --bootstrap-server "localhost:9092,localhost:9192,localhost:9292" --topic my-first-topic
> This is a message
> This is another message
```

## Consuming some messages

Kafka also has a command line **consumer** that prints messages to standard output.

```sh
C:\kafka_2.13-2.7.0>bin\windows\kafka-console-consumer.bat --bootstrap-server "localhost:9092,localhost:9192,localhost:9292" --topic my-first-topic --from-beginning
```

This is printed to the terminal:

```sh
This is a message
This is another message
```

Here, we used the `--from-beginning` flag. Otherwise, by default, the consumer starts consuming at the end of topics and only receives new messages.

If you have both of the above commands running in a different terminal then you should now be able to type messages into the producer terminal and see them appear in the consumer terminal.

All the command line tools have additional options; running the command with no arguments will display detailed usage information for the options.

## Multi broker environment

When creating our topic, we used `3` as the replication factor. In Kafka, the replication factor determines how many copies of the data exist. Having multiple copies improves the availability of our data as even if the Kafka broker that is hosting our topic had a failure, another broker hosting a copy will be able to take over and keep our topic available to applications.

Let's describe our topic, to see the details about its replicas:

```sh
> bin\windows\kafka-topics.bat --bootstrap-server "localhost:9092,localhost:9192,localhost:9292" --describe --topic my-first-topic
```

This is the output:

```sh
Topic: my-first-topic   PartitionCount: 2       ReplicationFactor: 3    Configs: segment.bytes=1073741824
        Topic: my-first-topic   Partition: 0    Leader: 2       Replicas: 2,0,1 Isr: 2,0,1
        Topic: my-first-topic   Partition: 1    Leader: 1       Replicas: 1,2,0 Isr: 1,2,0
```

Here is an explanation of output:

The first line gives a summary of the topic including the topic configurations, which are the defaults since we did not specify any configurations when creating the topic.

The additional lines provide information about each partition:

    - **Leader** is the broker currently responsible for reads and writes for the given partition. Each broker will be the leader for a randomly selected portion of the partitions.
    - **Replicas** is the list of brokers that replicate the log for this partition regardless of whether they are the leader or even if they are currently online.
    - **Isr** is the set of **In-Sync Replicas**. This is the subset of the replicas list that is currently online and fully in-sync with the leader.
<!--
## Consumer groups

A **consumer group** is a collection of consumers that cooperate to consume a set of topics. Kafka guarantees that, within a group, each partition of a topic will only be consumed by a single consumer.

When we run the console consumer above, it consumed both partitions of our topic. If we started another instance, both would see all messages. We can configure the console consumer to use a Consumer Group using the `--group` flag.

Let's restart a consumer with a group:

```sh
> bin\windows\kafka-console-consumer.bat --bootstrap-server "localhost:9092,localhost:9192,localhost:9292" --topic my-first-topic --from-beginning --group my-group
```

Now let's use the `kafka-consumer-groups.bat` tool to check the state of our group:
```sh
> bin\windows\kafka-consumer-groups.bat --bootstrap-server "localhost:9092,localhost:9192,localhost:9292" --describe --group my-group
```

Here's the output:

```sh
GROUP           TOPIC           PARTITION  CURRENT-OFFSET  LOG-END-OFFSET  LAG             CONSUMER-ID                                              HOST            CLIENT-ID
my-group        my-first-topic  0          1               1               0               consumer-my-group-1-a139ff8b-4e7d-40e4-8c81-660b629913d5 /169.254.0.3    consumer-my-group-1
my-group        my-first-topic  1          0               0               0               consumer-my-group-1-a139ff8b-4e7d-40e4-8c81-660b629913d5 /169.254.0.3    consumer-my-group-1
```


We can see that we have a single consumer that is consuming from both partitions of our topic.

Let's now start a second consumer using the same group. In another window, run:

```sh
> bin\windows\kafka-console-consumer.bat --bootstrap-server "localhost:9092,localhost:9192,localhost:9292" --topic my-first-topic --from-beginning --group my-group
```

If we describe our group again, we now see:
```sh
GROUP           TOPIC           PARTITION  CURRENT-OFFSET  LOG-END-OFFSET  LAG             CONSUMER-ID                                              HOST            CLIENT-ID
my-group        my-first-topic  0          1               1               0               consumer-my-group-1-287eb22f-a2e2-4a8d-9c22-b120622bf885 /169.254.0.3    consumer-my-group-1
my-group        my-first-topic  1          0               0               0               consumer-my-group-1-a139ff8b-4e7d-40e4-8c81-660b629913d5 /169.254.0.3    consumer-my-group-1
```

Our consumers have split the partitions between them. If we start a third consumer, it will not consume from any partitions and will act as a hot standby in case one of the other consumers crashes.

### Offsets

In addition, the `kafka-consumer-groups.bat` tool exposes the offsets last consumed by each consumer. This is useful to determine the health and state of consumers. It also shows the consumer lag which is the number of offsets between the current consumer position and the end of the partition. Ideally this value is small, which means consumers are near the end of partitions and processing recent records. If this value keeps increasing, it means consumers are not able to keep up with producers.


## Data Retention

One main characteristic of Kafka is that messages are not deleted once consumed but instead they are persisted. This persistence allows data to be consumed by many consumers and also enables consumers to reprocess data if needed.

As storage is not unlimited, retention limits can be specified to determine when to delete records. Because we did not specify configurations when we created our topic, default values were applied.

Let's describe our topic again to check what these are:

```sh
> bin\windows\kafka-topics.bat --bootstrap-server "localhost:9092,localhost:9192,localhost:9292" --describe --topic my-first-topic
```

The output is:

```sh
Topic: my-first-topic	PartitionCount: 2	ReplicationFactor: 3	Configs: min.insync.replicas=2,segment.bytes=536870912,retention.ms=86400000,retention.bytes=1073741824
	Topic: my-first-topic	Partition: 0	Leader: 1	Replicas: 1,2,3	Isr: 1,2,3
	Topic: my-first-topic	Partition: 1	Leader: 2	Replicas: 2,3,4	Isr: 2,3,4
```

There is:

- [`retention.ms`](https://kafka.apache.org/documentation/#retention.ms): This specifies the guaranteed minimum amount of time data is kept in Kafka.

- [`retention.bytes`](https://kafka.apache.org/documentation/#retention.bytes): This specifies the guaranteed minimum size of data for each partition kept in Kafka per partition

Whichever of these limits is reached first will trigger deletion records. -->

## Next Steps

Continue to [Part 3](../part3/README.md).
