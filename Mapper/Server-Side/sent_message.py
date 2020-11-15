
from readingFile import readFile
from analyze_data import chooseFunction
from Download_data import download_file
import datetime
import asyncio
import json
import csv

async def messageToUser(CusomterID):
    
    #await download_data('ClientData/RecommendInfo.csv','AnalyzedData/RecommendInfo.csv') # download customer information (action)
    fileLocation = "AnalyzedData/RecommendInfo.csv"
    listFileInfo = await readFile(fileLocation)
    saveInfo = []

    tomorrowDate = (datetime.date.today() + datetime.timedelta(days=1))
    year, month, day = str(tomorrowDate).split("-")
    tomorrowDate = day + "/" + month + "/" + year

    for eachInfo in listFileInfo:
        cusJson = json.loads(eachInfo[0])
        if cusJson["CustomerID"] == CusomterID: 
            if cusJson["StartDate"] == tomorrowDate: saveInfo.append(cusJson)

    if saveInfo == []: return "Tommorrow is fine"
    
    for warning in saveInfo:

        message = "Your destination from " + warning["StartPoint"] + " to " + warning["Destination"] + " in tommorrow around " + warning["UsualStartTime"] + " which takes " + str(warning["UsualTime"]) + " mins! We recommend you to start at " + warning["RecommenedStart"] + " which takes only " + str(warning["RecommenedTime"]) + " mins."
        print()
        print(message)
        print()

        return message # use only first 


async def download_data(objectKey,localFile):
    await download_file(objectKey,localFile)
    return True

asyncio.run(messageToUser("CUS001"))