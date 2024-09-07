import asyncio
import websockets
import serial
import re

async def sensor_data(websocket, path):
    ser = serial.Serial('COM3', 9600)
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            data = re.findall(r"[-+]?\d*\.\d+|\d+", line)
            if len(data) >= 3:
                message = f"Humidity: {data[0]}%, Temperature: {data[1]}C, Heat Index: {data[2]}C"
                await websocket.send(message)
            else:
                await websocket.send("Incomplete data received")
        await asyncio.sleep(1)  # Check for new data every second

start_server = websockets.serve(sensor_data, 'localhost', 5679)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()