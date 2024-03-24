from datetime import datetime
import json
from config.db import KAFKA_PRODUCER, KAFKA_CONSUMER, KAFKA_TOPIC

"""
This module provides functionality for publishing and consuming events with Kafka. It leverages the Kafka producer
and consumer configurations defined in `config.db`. It defines two main functions: `publish_event` for sending
events to a Kafka topic, and `consume_events` for retrieving events from a Kafka topic. The `publish_event` function
takes an operation type and data payload, constructs a message with a timestamp, and sends it to the configured Kafka
topic. The `consume_events` function reads messages from the Kafka topic up to a specified maximum or until there are
no more messages to consume, returning the collected messages.
"""

# Publish events
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

# Consume events
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