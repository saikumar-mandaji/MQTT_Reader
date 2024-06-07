import asyncio
import logging
from gmqtt import Client as MQTTClient
import  json



logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.FileHandler("log/mqtt_client.log"), logging.StreamHandler()],
)
logger = logging.getLogger("MQTTClient")


BROKER_HOST = "mosquitto"
BROKER_PORT = 1883
TOPIC = "/events"

MAX_RETRIES = 5
RETRY_DELAY = 60

STOP = asyncio.Event()


def on_message(client, topic, payload, qos, properties):
    print(f"Received message on topic '{topic}': {payload}")
    logger.info(f"Received message on topic '{topic}': {payload}")
    try:
        sensor_data = payload.decode()
        print(sensor_data)
    except Exception as e:
        logger.info(e)


def on_connect(client, flags, rc, properties):
    print("Connected to MQTT broker")
    logger.info("Connected to MQTT broker")
    client.subscribe(TOPIC, qos=1)


async def main():
    client = MQTTClient("mqtt-client")
    client.set_config(
        {"reconnect_retries": MAX_RETRIES, "reconnect_delay": RETRY_DELAY}
    )
    client.on_message = on_message
    client.on_connect = on_connect

    await client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)

    await asyncio.Future()  # Run forever


if __name__ == "__main__":
    asyncio.run(main())
