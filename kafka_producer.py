from kafka import KafkaProducer
from shipment_api import generate_shipment_data
import json, time
from datetime import date

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        return super().default(obj)

KAFKA_BROKER = "172.29.198.1:9092"
KAFKA_TOPIC = "shipments_raw"

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda x: json.dumps(x, cls=DateEncoder).encode('utf-8')
)

def stream_shipment_data():
    try:
        while True:
            shipment_data = generate_shipment_data()
            print(f"Producing shipment data: {shipment_data}")
            producer.send(KAFKA_TOPIC, shipment_data)
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Stopping shipment data producer...")
    finally:
        producer.close()
        
if __name__ == "__main__":
    stream_shipment_data()
