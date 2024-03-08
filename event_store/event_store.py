from datetime import datetime
import json
from config.db import KAFKA_PRODUCER, KAFKA_CONSUMER, KAFKA_TOPIC

def publish_event(operation, data):
    message = {
        'operation': operation,
        'timestamp': datetime.utcnow().isoformat(),
        'data': data
    }

    #Encode
    message_bytes = json.dumps(message).encode('utf-8')

    # Send the message to Kafka
    KAFKA_PRODUCER.send(KAFKA_TOPIC, value=message_bytes)
    KAFKA_PRODUCER.flush()

def consume_events(max_messages=5):
    messages = []
    try:
        for message in KAFKA_CONSUMER:
            messages.append(message.value)
            if len(messages) >= max_messages:
                break
    finally:
        return messages

# def consume_events(max_messages=5):
#     messages = []
#     try:
#         for _ in range(max_messages):
#             # Consume a single message at a time with a timeout
#             msg = next(KAFKA_CONSUMER, None)
#             if msg is None:
#                 # No more messages, break out of the loop
#                 break
#             messages.append(msg.value)
#     except StopIteration:
#         # No more messages available to consume
#         pass
#     return messages