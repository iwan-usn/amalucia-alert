import asyncio
import websockets
import json
from playsound import playsound
from datetime import datetime, timezone
import time

async def connect_ais_stream():

    async with websockets.connect("wss://stream.aisstream.io/v0/stream") as websocket:
        subscribe_message = {"APIKey": "95ad04e180b70ef1c1e4f3c1455cecab1ec7d2df",
                             "BoundingBoxes": [[[52.06075503467797, 5.103581306188966], [52.078569137579606, 5.077127968094469]]], # "box" aisstream looks in to find ships
           #                  "FiltersShipMMSI": ["244615725", "244670379"],  # Filter per ship(s) comment out if you want to view all ships
                             "FilterMessageTypes": ["PositionReport"]} # Message filters 
        
        subscribe_message_json = json.dumps(subscribe_message)
        await websocket.send(subscribe_message_json)

        async for message_json in websocket:
            message = json.loads(message_json)
            message_type = message["MessageType"]

            if message_type == "PositionReport":
             # the message parameter contains a key of the message type which contains the message itself
                ais_message = message['Message']['PositionReport']
                heading = ais_message['TrueHeading']
                course = ais_message['Cog']

            if 0 <= course <= 180:
                print(f"{ais_message['Cog']} Koers rechts {ais_message['UserID']}")

            if 181 <= course <= 370:
                print(f"{ais_message['Cog']} Koers links {ais_message['UserID']}")
       
#                print(f"[{datetime.now(timezone.utc)}] ShipID: {ais_message['UserID']} Heading: {ais_message['TrueHeading']} Course: {ais_message['Cog']}")            


asyncio.run(asyncio.run(connect_ais_stream()))