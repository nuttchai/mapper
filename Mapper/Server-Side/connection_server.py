#!/usr/bin/env python
from analyze_data import chooseFunction
from sent_message import messageToUser
from store_data import storeData
from get_data import download_data
from Upload_file import upload_file
import asyncio
import websockets
import json

async def echo(websocket, path):

    async for message in websocket:

        if json.loads(message)['Mode'] == "99" :

            #### communicate with client ####
            resultMessage = await (json.loads(message)["CustomerID"])
            await websocket.send(resultMessage)    
        
        else:

            #### communicate with client ####
            # print(message)
            await download_data()
            resultJson = await chooseFunction(message)
            # print(resultJson)
            await websocket.send(resultJson)

            #### store client data ####
            clientMesg = json.loads(message)
            await storeData(resultJson, json.loads(message)["CustomerID"], clientMesg["StartPoint"], clientMesg["Destination"])
            
            #### upload file ####
            await upload_file('CustomerInformation/CustomerInfoServer.csv','CustomerInformation/CustomerInfoServer.csv')

asyncio.get_event_loop().run_until_complete(
    websockets.serve(echo, '0.0.0.0', 80))
asyncio.get_event_loop().run_forever()
