import time
from pymongo import MongoClient
from kafka import KafkaProducer, KafkaConsumer

# Connecting to Database
# conn = MongoClient("mongodb://localhost:27017")
db_host = os.getenv("DB_HOST", "localhost")
db_port = os.getenv("DB_PORT", 27017)

print(f"mongodb://{db_host}:{db_port}")

client = MongoClient(f"mongodb://{db_host}:{db_port}")
db = client['calendar_db']
events = db['event']

KAFKA_TOPIC = 'events'
KAFKA_SERVER = 'kafka:9092'

def create_kafka_producer(retries=6, delay=5):
    for _ in range(retries):
        try:
            producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER, acks='all')
            return producer
        except Exception as e:
            print(f"Kafka Producer connection failed. Retrying in {delay} seconds.")
            time.sleep(delay)
    raise Exception("Failed to connect to Kafka after several attempts.")

# Use the function to create your Kafka producer
KAFKA_PRODUCER = create_kafka_producer()

KAFKA_CONSUMER = KafkaConsumer(KAFKA_TOPIC, bootstrap_servers=KAFKA_SERVER, auto_offset_reset='earliest')