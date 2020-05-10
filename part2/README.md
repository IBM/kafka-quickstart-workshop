# Part 2

In this part we will look at the most basics Kafka concepts.

## Creating a topic

A topic is a category or feed name to which records are published. To create a topic we need 3 things:

- Name: A topic is referred by its name. It has to be unique within a cluster and must use alphanumerics plus a few symbols (`.`, `_` and `-`).

- Partition count: Partitions are the units of scalability. Having multiple partitions allows distributing a topic across several brokers. However, Kafka only guarantees ordering within a partition.

- Replication factor: This specifies how many copies of the data are kept in the cluster. Let's set that to `3` for now.


Let's create our first topic:

```sh
> bin/kafka-topics.sh --bootstrap-server $BOOTSTRAP_SERVERS --command-config $CONFIG_FILE --create --replication-factor 3 --partitions 1 --topic my-first-topic
Created topic my-first-topic.
```

We can now see that topic if we run the list topic command:
```sh
> bin/kafka-topics.sh --bootstrap-server $BOOTSTRAP_SERVERS --command-config $CONFIG_FILE --list
my-first-topic
```

## Sending some messages

Kafka comes with a command line Producer that will take data from a file or from standard input and send it out as messages to the Kafka cluster. By default, each line will be sent as a separate message.

Run the producer and then type a few messages into the console to send to the server.

```sh
> bin/kafka-console-producer.sh --bootstrap-server $BOOTSTRAP_SERVERS --producer.config $CONFIG_FILE --topic my-first-topic
This is a message
This is another message
```

## Consuming some messages

Kafka also has a command line Consumer that will print messages to standard output.

```sh
> bin/kafka-console-consumer.sh --bootstrap-server $BOOTSTRAP_SERVERS --consumer.config $CONFIG_FILE --topic my-first-topic --from-beginning
This is a message
This is another message
```

Here we used the `--from-beginning` flag. Otherwise, by default, the Consumer starts consuming at the end of topics and only receives new messages.

If you have each of the above commands running in a different terminal then you should now be able to type messages into the producer terminal and see them appear in the consumer terminal.

All of the command line tools have additional options; running the command with no arguments will display usage information documenting them in more detail.

## Multi broker environment

When creating our topic, we used `3` as the replication factor. Event Streams requires all topics to have 3 replicas. In Kafka, the replication factor determines how many copies of the data exist. Having multiple copies improves the availability of our data as even if the Kafka broker hosting our topic had a failure, another broker hosting a copy will be able to take over and keep our topic accessible.

Let's describe our topic, to see the details about its replicas:

```sh
> bin/kafka-topics.sh --bootstrap-server <BOOTSTRAP_SERVERS> --command-config <CONFIG_FILE> --topic my-first-topic --describe
Topic:my-first-topic   PartitionCount:1    ReplicationFactor:3 Configs:
    Topic: my-first-topic  Partition: 0    Leader: 1   Replicas: 1,2,0 Isr: 1,2,0
```

Here is an explanation of output:

The first line gives a summary of the topic. Additional line gives information about each partition. Since we have only one partition for this topic there is only one line. We also did not specify any configuration hence there's nothing after `Configs`.

- `Leader` is the broker responsible for reads and writes for the given partition. Each broker will be the leader for a randomly selected portion of the partitions.
- `Replicas` is the list of brokers that replicate the log for this partition regardless of whether they are the leader or even if they are currently online.
- `Isr` is the set of "In-Sync Replicas". This is the subset of the replicas list that is currently online and caught-up to the leader.

## Consumer groups

## Delivery Semantics
