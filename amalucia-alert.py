import asyncio
import websockets
import json
from playsound import playsound
import time

async def connect_ais_stream():

    async with websockets.connect("wss://stream.aisstream.io/v0/stream") as websocket:
        subscribe_message = {"APIKey": "<api key here>",
                             "BoundingBoxes": [[[52.06124712782111, 5.098014078839175], [52.07097541416011, 5.086389440933547]]], # "box" aisstream looks in to find ships
#                             "FiltersShipMMSI": ["244021929"],  # Filter per ships comment out if you want to view all ships
                             "FilterMessageTypes": ["PositionReport"]} # Message filters 
        
        subscribe_message_json = json.dumps(subscribe_message)  # Dump json msg from subscribe message
        await websocket.send(subscribe_message_json)    

        async for message_json in websocket:        # filter message
            message = json.loads(message_json)
            message_type = message["MessageType"]

            if message_type == "PositionReport":
                ais_message = message['Message']['PositionReport']
             #   heading = ais_message['TrueHeading']
                course = ais_message['Cog']

            if 0 <= course <= 180: # checks if course of ship is eastward
                print(f"{ais_message['Cog']} Koers rechts {ais_message['UserID']}")
                playsound('slimshady.mp3')
                time.sleep(10)
                playsound('../../Downloads/jobs_done.mp3')

            if 181 <= course <= 370: # checks if course of ship is westward
                print(f"{ais_message['Cog']} Koers links {ais_message['UserID']}")
                playsound('slimshady.mp3')
                time.sleep(10)
                playsound('../../Downloads/jobs_done.mp3')

                time.sleep(360)

asyncio.run(asyncio.run(connect_ais_stream()))
