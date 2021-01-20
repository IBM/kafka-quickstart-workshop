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

file1 = open('myfile.txt', 'r') 
Lines = file1.readlines()
for data in Lines:
    # Trigger any available delivery report callbacks from previous produce() calls
    p.poll(0)

    # Asynchronously produce a message, the delivery report callback
    # will be triggered from poll() above, or flush() below, when the message has
    # been successfully delivered or failed permanently.
    
    p.produce('streams-plaintext-input', data.encode('utf-8'), callback=delivery_report)
    time.sleep(1)

# Wait for any outstanding messages to be delivered and delivery report
# callbacks to be triggered.
p.flush()