# Setting up Event Streams

For the server side, we will use [IBM Event Streams for IBM Cloud](https://www.ibm.com/cloud/event-streams).

This workshop requires creating several topics so you will incur a fee.

## Provisioning an Event Streams instance

1. Log in to the [IBM Cloud console](https://cloud.ibm.com/login).

2. Select the [Event Streams service](https://cloud.ibm.com/catalog/event-streams) in the Catalog.

3. Select the Standard or Enterprise plan on the service instance page.

4. Enter a name for your service. You can use the default value.

5. Click **Create**. The Event Streams Getting started page opens.

## Configuring the command line tools

Next, you need to configure the Kafka command line tools to be able to connect to our Kafka cluster.

To retrieve your Event Streams credentials, navigate to the instance in [IBM Cloud](https://cloud.ibm.com/resources). Click on the **Service Credentials** tab and select **New Credentials**. Then click on **View Credentials**. This panel contains all the information required to connect to your Event Streams instance.

1. The configuration file

Create a new file that contains the following:

```properties
bootstrap.servers=<BOOTSTRAP_SERVERS>
sasl.jaas.config=org.apache.kafka.common.security.plain.PlainLoginModule required username="token" password="<APIKEY>";
security.protocol=SASL_SSL
sasl.mechanism=PLAIN
ssl.protocol=TLSv1.2
ssl.enabled.protocols=TLSv1.2
ssl.endpoint.identification.algorithm=HTTPS
replication.factor=3
```

Replace `<APIKEY>` by the value of the `apikey` field in your Service Credentials.
Replace `BOOTSTRAP_SERVERS` by the values of the `kafka_brokers_sasl` field in your Service Credentials, separated by commas.

Set an environment variable, `CONFIG_FILE`, pointing to the location of this file. For example:

```sh
export CONFIG_FILE="/tmp/client.properties"
```

2. Bootstrap Servers

In your credentials, take note of the `kafka_brokers_sasl` field. These are the bootstrap servers that are used to connect to the cluster. Most commands will require these values to be passed in the CSV format.

Set an environment variable, `BOOTSTRAP_SERVERS`, listing all your brokers. For example, for:

```json
"kafka_brokers_sasl": [
  "broker-2-<...>.eventstreams.cloud.ibm.com:9093",
  "broker-0-<...>.eventstreams.cloud.ibm.com:9093",
  "broker-1-<...>.eventstreams.cloud.ibm.com:9093"
],
```

Set the environment variable like this:

```sh
export BOOTSTRAP_SERVERS="broker-2-<...>.eventstreams.cloud.ibm.com:9093,broker-0-<...>.eventstreams.cloud.ibm.com:9093,broker-1-<...>.eventstreams.cloud.ibm.com:9093"
```

## Back to Part 1

Return to [Part 1](../part1/README.md)
