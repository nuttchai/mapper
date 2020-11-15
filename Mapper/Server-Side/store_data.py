from readingFile import readFile
import asyncio
import csv
import json

async def storeData(resultJson, CustomerID, StartPoint, Destination):

    fileLocation = "CustomerInformation/CustomerInfoServer.csv"
     
    information = []
    information.append(CustomerID)
    information.append(StartPoint)
    information.append(Destination)
    information.append(resultJson["startDate"])
    information.append(resultJson["startTime"])
    information.append(str(resultJson["distance"]))
    information.append(str(resultJson["minute"]))
    information.append(str(resultJson["percentRain"]))
    information.append(str(resultJson["minuteRain"]))
    # print(information)

    previousInfoRaw = await readFile(fileLocation)
    previousInfo = []
    for info in previousInfoRaw:
        if info[0] != "": previousInfo.append(info)

    # print(previousInfo)
    with open(fileLocation, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        for info in previousInfo:
            csv_writer.writerow(info)
        csv_writer.writerow(information)

""" 

result = {     
                "startDate" : "21/12/2020",
                "startTime" : "10:30",
                "distance" : 5, 
                    "minute" : 15, 
            "percentRain" : 5.00, 
                "minuteRain" : 16   }
    

asyncio.run(storeData(result, "123", "R1", "R2"))

"""