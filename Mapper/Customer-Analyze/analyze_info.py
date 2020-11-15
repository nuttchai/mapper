from analyze_time import rangeMode, chooseFunction
from readingFile import readFile
from Upload_file import upload_file 
from Download_data import download_file

import calendar
import asyncio
import csv
import json
import datetime


async def checkRelationship():

    fileLocation = 'CustomerInfo/CustomerInfo.csv'
    customer_info = await readFile(fileLocation)
    customer_info.pop(0)
    customerList = []
    countAtt = 0

    # Gather all user id
    for customer in customer_info: 
        if customer[0] not in customerList: customerList.append(customer[0])

    # Append each user in checker
    
    for customerID in customerList:

        requiredInfo = await returnCustomerInfo(customer_info, customerID)      # Get only used information
        
        if not await sameRouteCheck(requiredInfo): break                        # Check that it is a same route, do others

        if await continuousneseDate(requiredInfo):                              # Check that its date information continue
            
            # print("Calculating Time..")                                       # Calculate Average Time
            totalHour, totalMin, totalTime = 0, 0, 0

            for eachInfo in requiredInfo:                           # Calculate Average TravelTime & Starting Time
                strhour, strmins = eachInfo[4].split(":")
                hour, mins = int(strhour), int(strmins)
                totalHour += hour
                totalMin  += mins
                totalTime += float(eachInfo[6])

            averageTime = totalTime/len(requiredInfo)               # Average Travel Time (mins)
            averageHour = totalHour//len(requiredInfo)
            averageMins = totalMin//len(requiredInfo)
            previousHour = averageHour - 2               

            usedTime = str(averageHour) + ":" +str(averageMins)     # Average Starting Time (Used for predicting next day)
            prevTime = str(previousHour) + ":" +str(averageMins) # 24 Used for test

            lastDay, lastMonth, lastYear = requiredInfo[-1][3].split("/")
            nextDay  = str(int(lastDay) + 1)
            nextDate = nextDay + "/" + lastMonth + "/" + lastYear   # Find next day

            JsonMessage = { "StartPoint"    :   requiredInfo[0][1], 
                            "Destination"   :   requiredInfo[0][2], 
                            "Mode"          :   "2", 
                            "StartDay"      :   nextDate,           # estimate data with 15/11/2020 (test date)
                            "StartTime"     :   usedTime, 
                            "EndDay"        :   "null", 
                            "EndTime"       :   "null" }

            textJson = json.dumps(JsonMessage)
            # print(textJson)

            resultTextJson = await chooseFunction(textJson)
            resultJson = json.loads(resultTextJson)
            # print(resultJson)

            # Citeria that used to decide that should it recommend a new time or not
            ratioRate = 1.5             
            
            if averageTime * 1.5 >= resultJson['minute']: return False
            else: 
                # Predicting a better time
                JsonMessage = { "StartPoint"    :   requiredInfo[0][1], 
                                "Destination"   :   requiredInfo[0][2], 
                                "Mode"          :   "4", 
                                "StartDay"      :   nextDate,           
                                "StartTime"     :   prevTime, 
                                "EndDay"        :   nextDate, 
                                "EndTime"       :   usedTime }
                
                textJson = json.dumps(JsonMessage)
                # print(textJson)

                resultTextJson_Predict = await chooseFunction(textJson)
                resultJson_Predict = json.loads(resultTextJson_Predict)
                # print(resultJson_Predict)

                ############ store data ############

                data = {    "CustomerID"        : customerID,
                            "StartPoint"        : requiredInfo[0][1], 
                            "Destination"       : requiredInfo[0][2], 
                            "StartDate"         : nextDate,
                            "UsualStartTime"    : usedTime,
                            "UsualTime"         : resultJson['minute'],
                            "RecommenedStart"   : resultJson_Predict['startTime'],
                            "RecommenedTime"    : resultJson_Predict['minute'],
                            "TimeSaving"        : abs(resultJson_Predict['minute'] - resultJson['minute'])
                        }
                
                # print(data)
                dataText = json.dumps(data)

                # Clear File and Add New Record
                fileLocation = "AnalyzedData/RecommendInfo.csv"
                
                mode = 'w'
                if countAtt != 0: mode = 'a'

                with open(fileLocation, mode=mode) as csv_file:
                    csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    csv_writer.writerow([dataText])
                
                ############ upload data ############
                countAtt += 1
                

    return fileLocation


async def sameRouteCheck(fileInfo):
    
    startIni, destIni = fileInfo[0][1], fileInfo[0][2]
    for eachInfo in fileInfo:
        if startIni != eachInfo[1] or destIni != eachInfo[2]: return False
    
    return True


async def returnCustomerInfo(fileInfo, cusotmerID):
    
    customerInfo = [] 

    for eachInfo in fileInfo:
        if eachInfo[0] == cusotmerID: customerInfo.append(eachInfo)         # Add require customer information

    return customerInfo


async def continuousneseDate(fileInfo):
    
    # print(fileInfo)
    
    if len(fileInfo) <= 20: return False                    # Need more Information

    firstDate = fileInfo[0][3]                              # take day of the data
    day, month, year = firstDate.split("/")                 # split day, month, year
    fday, fmonth, fyear = int(day), int(month), int(year)   # convert str to int and create initial date
    
    # print(fday, fmonth, fyear)

    for eachInfo in fileInfo:   
        
        curDate = eachInfo[3]
        count = 0
        cday, cmonth, cyear = curDate.split("/")
        iday, imonth, iyear = int(cday), int(cmonth), int(cyear)
        
        if fyear == iyear:
            if fmonth == imonth:
                if iday != fday + 1 and count != 0: return False
                else: fday += 1
            else: 
                if imonth != fmonth + 1 or fday == calendar.monthrange(fyear, fmonth)[1]: return False 
                else:
                    fmonth += 1
                    fday = 0
        else:
            if iyear != fyear + 1: return False
            else:
                fyear += 1
                fmonth = 1
                fday = 0
        
        count += 1

    return True


async def upload_data(fileLocation):
    await upload_file('ClientData/RecommendInfo.csv',fileLocation)
    return True

async def download_data():
    await download_file('CustomerInfomation/CustomerInfoServer.csv','CustomerInfo/CustomerInfoServer.csv')
    return True


async def runMain():
    
    check = datetime.datetime.now().strftime("%d")
    
    while True:

        if check == datetime.datetime.now().strftime("%d"): check = datetime.datetime.now().strftime("%d")
        else: 
            await main()
            check = datetime.datetime.now().strftime("%d")

async def main():
    await download_data()
    fileLoc = await checkRelationship()
    await upload_data(fileLoc)
    
#asyncio.get_event_loop().run_until_complete(runMain())
asyncio.get_event_loop().run_until_complete(main())