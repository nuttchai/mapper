#!/usr/bin/env python

import asyncio
import websockets
import json

async def send_request(uri):

    async with websockets.connect(uri) as websocket:
        jjsonText = '{ "StartPoint":"R2", "Destination":"R5", "Mode":"3", "StartDay":"15/11/2020", "StartTime":"7:00", "EndDay":"17/11/2020", "EndTime":"7:00", "CustomerID":"CUS001" }'
        await websocket.send(jsonText)
        resp = await websocket.recv()
        print(resp)

asyncio.get_event_loop().run_until_complete(
    send_request('ws://159.138.253.71:80'))

