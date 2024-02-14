import asyncio
import websockets
import json
import subprocess
import time

def playsound():
    intro = '../intro.mp3'
    outro = '../outro_out.mp3'
    subprocess.Popen(f"/bin/ffplay -nodisp -loglevel quiet -autoexit -volume 150 {intro}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    time.sleep(10)
    subprocess.Popen(f"/bin/ffplay -nodisp -loglevel quiet -autoexit -volume 150 {outro}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

async def connect_ais_stream():

    async with websockets.connect("wss://stream.aisstream.io/v0/stream") as websocket:
        subscribe_message = {"APIKey": "95ad04e180b70ef1c1e4f3c1455cecab1ec7d2df",
                             "BoundingBoxes": [[[52.06124712782111, 5.098014078839175], [52.07097541416011, 5.086389440933547]]], # "box" aisstream looks in to find ships
                             "FiltersShipMMSI": ["244670667"],  # Filter per ships comment out if you want to view all ships
                             "FilterMessageTypes": ["PositionReport"]} # Message filters 
        
        subscribe_message_json = json.dumps(subscribe_message)  # Dump json msg from subscribe message
        await websocket.send(subscribe_message_json)    

        async for message_json in websocket:        # filter message
            message = json.loads(message_json)
            message_type = message["MessageType"]

            if message_type == "PositionReport":
                ais_message = message['Message']['PositionReport']
              #  course = ais_message['TrueHeading'] # in some cases needed if the ship that you're tracking only shows their true heading 
                course = ais_message['Cog']



            if 0 <= course <= 180: # checks if course of ship is eastward
                print(f"{ais_message['Cog']} Koers rechts {ais_message['UserID']}")
                playsound()

            if 181 <= course <= 370: # checks if course of ship is westward
                print(f"{ais_message['Cog']} Koers links {ais_message['UserID']}")
                playsound()

asyncio.run(asyncio.run(connect_ais_stream()))
