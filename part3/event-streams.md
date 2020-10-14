# Configuring Kafka Connect for Event Streams

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
key.converter=org.apache.kafka.connect.storage.StringConverter
value.converter=org.apache.kafka.connect.storage.StringConverter

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

## Back to Part 3

Return to [Part 3](../part3/README.md).
