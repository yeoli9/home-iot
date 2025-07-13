from fastapi import FastAPI, Response
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST
import board
import adafruit_dht
import time

app = FastAPI()

# Prometheus 메트릭 정의
temperature_gauge = Gauge('dht22_temperature_celsius', 'Temperature from DHT22 sensor')
humidity_gauge = Gauge('dht22_humidity_percent', 'Humidity from DHT22 sensor')

# 센서 초기화
dht_device = adafruit_dht.DHT22(board.D4)

@app.get("/")
def root():
    return {"message": "DHT22 Prometheus Exporter"}

@app.get("/metrics")
def metrics():
    try:
        temperature = dht_device.temperature
        humidity = dht_device.humidity
        if temperature is not None:
            temperature_gauge.set(temperature)
        if humidity is not None:
            humidity_gauge.set(humidity)
    except RuntimeError as e:
        print(f"Sensor read error: {e}")
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

