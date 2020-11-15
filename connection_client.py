#!/usr/bin/env python

import asyncio
import websockets
import json

async def send_request(uri):

    async with websockets.connect(uri) as websocket:

        ################################################################################





        #   StartPoint    # Selected Range: R1 to R5
        #   Destination   # Selected Range: R1 to R5 
        #   Mode          # Available Mode: 1 (default mode), 2 (select starting time),                                     3 (select arriving time), 4 (select the range)


        # Message From Client

        jsonText = '{ "StartPoint":"R1", "Destination":"R5", "Mode":"4", "StartDay":"14/11/2020", "StartTime":"8:00", "EndDay":"17/11/2020", "EndTime":"19:00", "CustomerID" : "CUS001" }'








        ################################################################################



        await websocket.send(jsonText)
        resp = await websocket.recv()
        convertResp = json.loads(resp)
        print("")
        print("Starting Date:", convertResp["startDate"])
        print("Starting Time:", convertResp["startTime"])
        print("Starting Distance:", convertResp["distance"], "kilometers")
        print("Total Minutes:", convertResp["minute"], "minutes")
        print("Percent of Raining:", convertResp["minuteRain"], "%")
        if float(convertResp["percentRain"]) > 0:
            print("Total Minutes with Rain:", convertResp["minuteRain"], "minutes") 
        print("")

asyncio.get_event_loop().run_until_complete(
    send_request('ws://159.138.253.71:80'))

