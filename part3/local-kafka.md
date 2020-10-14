# Configuring Kafka Connect for Local Kafka cluster

Create a file with the following contents:

```properties
# connectivity settings for the runtime
bootstrap.servers=localhost:9092,localhost:9192,localhost:9292

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
