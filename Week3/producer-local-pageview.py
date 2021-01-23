from confluent_kafka import Producer
import time

p = Producer({'bootstrap.servers': 'localhost:9092,localhost:9192,localhost:9292'})

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))


key = 'user'
r1 = {"_t": "pv", key:"2", "page":"22", "timestamp":1435278177777}
r2 = {"_t": "up", "region":"CA","timestamp":1435278177777} 

import json

# Trigger any available delivery report callbacks from previous produce() calls
p.poll(0)

p.produce('streams-pageview-input', key=r1[key], value=json.dumps(r1))

time.sleep(2)

p.produce('streams-userprofile-input', key=r1[key], value=json.dumps(r2))
time.sleep(2)

# Wait for any outstanding messages to be delivered and delivery report
# callbacks to be triggered.
p.flush()