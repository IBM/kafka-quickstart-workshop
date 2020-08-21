# Getting started with Kafka

Learn how Apache Kafka works and how you can use it to build applications that react to events as they happen. This workshop demonstrates how Kafka can be used as a streaming platform. It covers the basics of Apache Kafka and takes a look at all the components of the Kafka platform, explaining key concepts as we go along.


## Workshop objectives

In this workshop, we will build a small event streaming pipeline using the built-in tools and samples of Apache Kafka.

![Workshop pipeline](./pipeline.png)

Data flow:
- Our input data comes from a file, `/tmp/file-source.txt`.
- As new lines are added to this file, Kafka Connect streams them into a topic, `streams-plaintext-input`, in Kafka.
- A Kafka Streams application processes records from ``streams-plaintext-input`` in real time and writes the computed output into a new topic, `streams-wordcount-output`.


## [Part 1 - Setup and Prerequisites](./part1/README.md)

The first part gives an overview of the Kafka platform. It covers the main use cases for Kafka. It also contains the prerequisites for the workshop.

## [Part 2 - Basic Kafka Concepts](./part2/README.md)

The second part covers the most basic principles of Apache Kafka such as topics, partitions and the Producer and Consumer clients.

## [Part 3 - Integrating data with Kafka Connect](./part3/README.md)

The third part explains how existing systems can be connected to Kafka using Kafka Connect. Using built-in connectors, we will see how data can be imported into Kafka.

## [Part 4 - Processing data with Kafka Streams](./part4/README.md)

The fourth part introduces Kafka Streams and explains its data processing capabilities. It explores the `WordCountDemo` sample application by running it and detailing its processing logic.
