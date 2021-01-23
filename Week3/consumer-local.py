from confluent_kafka import Consumer

c = Consumer({
    'bootstrap.servers': 'localhost:9092,localhost:9192,localhost:9292',
    'group.id': 'mygroup',
    'auto.offset.reset': 'earliest'
})

c.subscribe(['streams-pageviewstats-typed-output'])

while True:
    msg = c.poll(1.0)

    if msg is None:
        continue
    if msg.error():
        print("Consumer error: {}".format(msg.error()))
        continue

    #print(msg.value())
    value = msg.value()
    print(value)
    if value is None:
        value = -1
    else:
        value = msg.value()[-1]
        
    kvalue = msg.key().decode('utf-8')
    print('Received message: {0} , {1}'.format(kvalue, value))
    
c.close()

