
import asyncio
import math
import json
from readingFile import readFile
from datetime import date, datetime

## Test Function 

#   StartPoint    # Selected Range: R1 to R5 or null
#   Destination   # Selected Range: R1 to R5 
#   Mode          # Available Mode: 1 (default mode), 2 (select starting time),                                   3 (select arriving time), 4 (select the range)
#   StartDay      # Available For Mode 2 & 4 (Selecting Starting Day) 
#   StartTime     # Available For Mode 2 & 4 (Selecting Starting Time) 
#   EndDay        # Available For Mode 3 & 4 (Selecting Ending Time) 
#   EndTime       # Available For Mode 3 & 4 (Selecting Ending Time) 



async def chooseFunction(jsonText):
    
    msg = json.loads(jsonText)
    modeMsg = msg["Mode"]

    if modeMsg == "2": startDate, startTime, totalDistance, totalMinute, chanceOfRaining, totalMinute_rain = await startTimeMode(msg)
    elif modeMsg == "3": startDate, startTime, totalDistance, totalMinute, chanceOfRaining, totalMinute_rain = await endTimeMode(msg)
    elif modeMsg == "4": startDate, startTime, totalDistance, totalMinute, chanceOfRaining, totalMinute_rain = await rangeMode(msg)
    else: startDate, startTime, totalDistance, totalMinute, chanceOfRaining, totalMinute_rain = await defaultMode(msg)
    
    result = {    "startDate" : startDate,
                  "startTime" : startTime,
                   "distance" : totalDistance, 
                     "minute" : totalMinute, 
                "percentRain" : chanceOfRaining, 
                 "minuteRain" : totalMinute_rain   }
    
    """
    # DISPLAY RESULT
    print("Start Date:", result["startDate"]) # DATE
    print("Start Time:", result["startTime"]) # TIME
    print("Total Distance:", result["distance"], "km") # DISTANCE
    print("Total Minutes:", result["minute"], "minutes") # TIME
    print("Chance of Raining:", result["percentRain"], "%") # CHANCE OF RAINING
    if float(result["percentRain"]) > 0:
        print("Total Minutes with Rain:", result["minuteRain"], "minutes") # CHANCE OF RAINING
    """

    resultJson = json.dumps(result)

    return resultJson
    

async def defaultMode(msg):

    today = date.today()
    time = datetime.now()

    # current day, time (hour) && require destination && optional starting location (default = current location)
    currentDate = today.strftime("%d/%m/%Y") # current day
    currentHour = time.strftime("%H") # current time - hour
    currentMin  = time.strftime("%M") # current time - minute

    startDate, startTime = currentDate, time.strftime("%H:%M")
    
    if msg["StartPoint"] == "null": msg["StartPoint"] = "R1"
    startingPoint = msg["StartPoint"] # starting point
    destination = msg["Destination"] # destination

    ############### calculating time ###############

    # Get Road Distance
    fileLocation = 'Data/Road/RoadInformation.csv'
    roadFile = await readFile(fileLocation)
    roadFile.pop(0)
    
    # Find Each Road Lenght
    usedRoad, check = [], False

    for roadInfo in roadFile:
        if destination == roadInfo[0]: 
            usedRoad.append(roadInfo[1])
            check = True
        if check: break
        else: usedRoad.append(roadInfo[1])

    # Give a Correct Starting Point
    startingIndex = int(startingPoint[1:])
    usedRoad = usedRoad[startingIndex-1:]
    ## print("distance: ", usedRoad) # Each Data Represent a Distance of Each Used Road

    # Locate the date index
    fileLocation = 'Data/TrafficCondition/AverageSpeed/AverageSpeed.csv' # Don't forget to change file back !!!!!!!!!!!!
    avgFile = await readFile(fileLocation)
    
    count, roadBlock, numberOfday = 0, 5, 3

    for info in avgFile:
        index = 1 + roadBlock * count
        if avgFile[index][0] == currentDate: break
        elif count >= numberOfday: 
            print("Invaild Date")
            return "err", "err", "err", "err", "err", "err"
        else: count += 1

    usedAvg, check = [], False

    # Find the Avg Speed of that hour
    for infoIndex in range(index, index + roadBlock):
        if destination == avgFile[infoIndex][1]: 
            usedAvg.append(avgFile[infoIndex][int(currentHour) + 2])
            check = True
        if check: break
        else: usedAvg.append(avgFile[infoIndex][int(currentHour) + 2])

    # Give a Correct Starting Point
    usedAvg = usedAvg[startingIndex-1:]
    ## print("avg: ", usedAvg) # Each Data Represent an Average Speed of Each Used Road in that Hour 

    # Calculate Time => Distance (km) / Average Speed (km/hr) => Time * 60 (minutes)
    totalMinute = 0

    for indexData in range(len(usedAvg)):
        time_min =  (float(usedRoad[indexData]) / float(usedAvg[indexData])) * 60 # Time travel for Each Road Block
        ## print("Time for each block: ", time_min)
        totalMinute += time_min
    
    # print(totalMinute) 
    totalMinute = math.ceil(totalMinute) # Round to be full minute
    
    ############### calculating distance ###############
    totalDistance = 0
    for str_dis in usedRoad:
        totalDistance += float(str_dis)
    totalDistance = "{:.2f}".format(totalDistance)

    ############### calculating chance of raining ###############
    city = 'Bangkok'
    fileLocation = 'Data/Weather/'+ city +'.csv'
    weatherFile = await readFile(fileLocation)
    selectedInfo = ''

    for weatherInfo in weatherFile:
        if currentDate == weatherInfo[0]:
            selectedInfo = weatherInfo
            break
    # print(selectedInfo)
    
    chanceOfRaining = float(selectedInfo[int(currentHour) + 1]) * 100
    
    ############### calculating time with raining ###############

    ratioIncrease = 1.04 # Edit later (Rain: x2, Heavy Rain: x5)
    totalMinute_rain = math.ceil(totalMinute * ratioIncrease)
    
    return startDate, startTime, totalDistance, totalMinute, chanceOfRaining, totalMinute_rain


async def startTimeMode(msg):
    
    startDate, startTime, totalDistance, totalMinute, chanceOfRaining, totalMinute_rain = 0, 0, 0, 0, 0, 0
    # require start time (hour), day, destination && optional starting location (defualt = current location)
    # { "StartPoint":"R1", "Destination":"R5", "Mode":"1", "StartDay":"null", "StartTime":"null","EndDay":"null", "EndTime":"null" }

    startingTime = msg["StartTime"]
    destination = msg["Destination"] # Destination
    givenDate = msg["StartDay"] # Start Day
    
    startDate, startTime, = givenDate, startingTime

    # Starting Location
    if msg["StartPoint"] == "null": msg["StartPoint"] = "R1"
    startingPoint = msg["StartPoint"] 

    # Split starting hour and minute
    startingHour, startingMinute = startingTime.split(":") 
    
    # Get Road Distance
    fileLocation = 'Data/Road/RoadInformation.csv'
    roadFile = await readFile(fileLocation)
    roadFile.pop(0)
    
    # Find Each Road Lenght
    usedRoad, check = [], False

    for roadInfo in roadFile:
        if destination == roadInfo[0]: 
            usedRoad.append(roadInfo[1])
            check = True
        if check: break
        else: usedRoad.append(roadInfo[1])
    
    # Give a Correct Starting Point
    startingIndex = int(startingPoint[1:])
    usedRoad = usedRoad[startingIndex-1:]
    ## print("distance: ", usedRoad) # Each Data Represent a Distance of Each Used Road

    # Locate the date index
    fileLocation = 'Data/TrafficCondition/AverageSpeed/AverageSpeed.csv' # Don't forget to change file back !!!!!!!!!!!!
    avgFile = await readFile(fileLocation)
    
    count, roadBlock, numberOfday = 0, 5, 3
    
    for info in avgFile:
        index = 1 + roadBlock * count
        if avgFile[index][0] == givenDate: break
        elif count >= numberOfday: 
            print("Invaild Date")
            return "err", "err", "err", "err", "err", "err"
        else: count += 1
    usedAvg, check = [], False

    # Find the Avg Speed of that hour
    for infoIndex in range(index, index + roadBlock):
        if destination == avgFile[infoIndex][1]: 
            usedAvg.append(avgFile[infoIndex][int(startingHour) + 2])
            check = True
        if check: break
        else: usedAvg.append(avgFile[infoIndex][int(startingHour) + 2])

    # Give a Correct Starting Point
    usedAvg = usedAvg[startingIndex-1:]
    ## print("avg: ", usedAvg) # Each Data Represent an Average Speed of Each Used Road in that Hour 

    # Calculate Time => Distance (km) / Average Speed (km/hr) => Time * 60 (minutes)
    totalMinute = 0

    for indexData in range(len(usedAvg)):
        time_min =  (float(usedRoad[indexData]) / float(usedAvg[indexData])) * 60 # Time travel for Each Road Block
        ## print("Time for each block: ", time_min)
        totalMinute += time_min
    
    # print(totalMinute) 
    totalMinute = math.ceil(totalMinute) # Round to be full minute
    
    ############### calculating distance ###############
    totalDistance = 0
    for str_dis in usedRoad:
        totalDistance += float(str_dis)
    totalDistance = "{:.2f}".format(totalDistance)

    ############### calculating chance of raining ###############
    city = 'Bangkok'
    fileLocation = 'Data/Weather/'+ city +'.csv'
    weatherFile = await readFile(fileLocation)
    selectedInfo = ''

    for weatherInfo in weatherFile:
        if givenDate == weatherInfo[0]:
            selectedInfo = weatherInfo
            break

    chanceOfRaining = float(selectedInfo[int(startingHour) + 1]) * 100
    
    ############### calculating time with raining ###############

    ratioIncrease = 1.04 # Edit later (Rain: x2, Heavy Rain: x5)
    totalMinute_rain = math.ceil(totalMinute * ratioIncrease)

    return startDate, startTime, totalDistance, totalMinute, chanceOfRaining, totalMinute_rain


async def endTimeMode(msg):

    startDate, startTime, totalDistance, totalMinute, chanceOfRaining, totalMinute_rain = 0, 0, 0, 0, 0, 0
    # require end time (hour), day, destination && optional starting location (defualt = current location)

    givenDate = msg["EndDay"] # Arrive Day
    arrivingTime = msg["EndTime"] # Arrive Time
    destination = msg["Destination"] # Destination
    if msg["StartPoint"] == "null": msg["StartPoint"] = "R1"
    startingPoint = msg["StartPoint"] 

    # { "StartPoint":"R1", "Destination":"R4", "Mode":"1", "StartDay":"null", "StartTime":"null", "EndDay":"17/11/2020", "EndTime":"16:00" }

    arrivingHour, arrivingMinute = arrivingTime.split(":")
    
    setOfRoad = {"R1":1, "R2":2, "R3":3, "R4":4, "R5":5}
    lisOfRoad = ["R1", "R2", "R3", "R4", "R5"]
    usedRoad  = lisOfRoad[setOfRoad[startingPoint]-1:setOfRoad[destination]]

    # Get Road Distance
    fileLocation = 'Data/Road/RoadInformation.csv'
    roadFile = await readFile(fileLocation)
    roadFile.pop(0)
    usedRoadInfo = []

    for road in roadFile:
        if road[0] in usedRoad:
            usedRoadInfo.append(road)            # Append Road Information that we need

    reverseRoadInfo = usedRoadInfo[::-1]         # Reverse the list
    

    # Locate the date index
    fileLocation = 'Data/TrafficCondition/AverageSpeed/AverageSpeed.csv' # Don't forget to change file back !!!!!!!!!!!!
    avgFile = await readFile(fileLocation)

    count, roadBlock, numberOfday = 0, 5, 3
    
    for info in avgFile:
        index = 1 + roadBlock * count
        if avgFile[index][0] == givenDate: break
        elif count >= numberOfday: 
            print("Invaild Date")
            return "err", "err", "err", "err", "err", "err"
        else: count += 1
    usedAvg, check = [], False

    selectAvg = avgFile[index : index + roadBlock]
    selectAvgInfo = []

    for eachInfo in selectAvg:
        if eachInfo[1] in usedRoad:
            selectAvgInfo.append(eachInfo)  

    reversedAvgInfo = selectAvgInfo[::-1]
    reversedRoad    = usedRoad[::-1]
    roadDistance = []

    for roadInfo in reverseRoadInfo:
        roadDistance.append(roadInfo[1])

    #print(roadDistance)
    #print(reversedRoad)
    #print(reversedAvgInfo)

    arriveHourInitial = int(arrivingHour)             # Set the inital hour value
    arriveMinuteInitial  = int(arrivingMinute)       # Set the inital minute value
    arriveDayInitial, arriveMthInitial, arriveYrsInitial = givenDate.split("/")
    arriveDayInitial, arriveMthInitial, arriveYrsInitial = int(arriveDayInitial), int(arriveMthInitial), int(arriveYrsInitial)
    totalTime = 0

    for index in range(len(roadDistance)):
        velocity = reversedAvgInfo[index][int(arriveHourInitial) + 2]
        distance = roadDistance[index]        
        time     = (float(distance)/float(velocity)) * 60
        totalTime += time

        if arriveMinuteInitial - time < 0:
            if arriveHourInitial - 1 < 0: 
                arriveHourInitial = 23
                arriveDayInitial -= 1
            else: arriveHourInitial -= 1

            remainder = abs(arriveMinuteInitial - time)
            arriveMinuteInitial = 60 - remainder
        else: arriveMinuteInitial -= time

    totalTime = math.ceil(totalTime)
    timeLeave = str(arriveHourInitial) + ":" + str(math.floor(arriveMinuteInitial))
    
    for dis in roadDistance:
        totalDistance += float(dis)

    startDate = str(arriveDayInitial) + "/" + str(arriveMthInitial) + "/" + str(arriveYrsInitial)
    startTime = timeLeave
    totalMinute = totalTime


    ############### calculating chance of raining ###############
    city = 'Bangkok'
    fileLocation = 'Data/Weather/'+ city +'.csv'
    weatherFile = await readFile(fileLocation)
    selectedInfo = ''

    for weatherInfo in weatherFile:
        if givenDate == weatherInfo[0]:
            selectedInfo = weatherInfo
            break

    chanceOfRaining = float(selectedInfo[int(arriveHourInitial) + 1]) * 100
    
    ############### calculating time with raining ###############

    ratioIncrease = 1.04 # Edit later (Rain: x2, Heavy Rain: x5)
    totalMinute_rain = math.ceil(totalMinute * ratioIncrease)

    return startDate, startTime, totalDistance, totalMinute, chanceOfRaining, totalMinute_rain











async def rangeMode(msg):

    bestDate, bestTime, totalDistance, totalMinute, chanceOfRaining, totalMinute_rain = 0, 0, 0, 0, 0, 0
    # require start time & end time (hour), day, destination && optional starting location (defualt = current location)
    # { "StartPoint":"R1", "Destination":"R5", "Mode":"3", "StartDay":"null", "StartTime":"null","EndDay":"null", "EndTime":"null" }

    allResults = []

    # Starting Location
    if msg["StartPoint"] == "null": msg["StartPoint"] = "R1"
    startingPoint = msg["StartPoint"] 
    # Destination   
    destination = msg["Destination"] 

    startingTime = msg["StartTime"]
    startingDay = msg["StartDay"]
    endingTime = msg["EndTime"]
    endingDay = msg["EndDay"]

    # Split starting & ending hour and minute
    startingHour, startingMinute = startingTime.split(":") 
    endingHour, endingMinute     = endingTime.split(":") 
    
    # Split starting & ending day, month, and year
    startingDay, startingMth, startingYrs = startingDay.split("/") 
    endingDay, endingMth, endingYrs = endingDay.split("/") 

    # find the range of checking
    if int(endingDay) != int(startingDay): 
        rangeCheck = (24 - int(startingHour)) + abs(int(endingDay) - int(startingDay) - 1) * 24 + int(endingHour)
    else: rangeCheck = abs(int(endingHour) - int(startingHour))

    countHour = int(startingHour)
    countDay  = int(startingDay)
    storeResult = []
    for attempt in range(rangeCheck+1):

        if countHour == 24: 
            countHour = 0
            countDay += 1

        # Create JSON
        startDayJSON  = str(countDay) + "/" + startingMth +  "/" + startingYrs
        startTimeJSON = str(countHour) + ":" + startingMinute
        jsonText = '{ "StartPoint":"' + startingPoint + '", "Destination":"' + destination + '", "Mode":"1", "StartDay":"' + startDayJSON + '", "StartTime":"' + startTimeJSON + '", "EndDay":"null", "EndTime":"null" }'
        # print(jsonText)
        msg = json.loads(jsonText)
        
        # Put into startTimeMode function
        startDate, startTime, totalDistance, totalMinute, chanceOfRaining, totalMinute_rain = await startTimeMode(msg)

        storeResult.append([startDate, startTime, totalDistance, totalMinute, chanceOfRaining, totalMinute_rain])
        
        countHour += 1
    
    # compare each result 
    minimumTime, positionMinimum, count = 10**10000, -1, 0
    
    for eachInfo in storeResult:

        if int(eachInfo[3]) < minimumTime:
            minimumTime = int(eachInfo[3])
            positionMinimum = count

        count += 1

    result = storeResult[positionMinimum]

    # check that there are more result that give a same minute
    allResults = []

    for eachInfo in storeResult:
        if eachInfo[3] == minimumTime:
            allResults.append(eachInfo)


    # print("Set Minimum Time: ", allResults)
    # print(result)

    bestDate, bestTime, totalDistance, totalMinute, chanceOfRaining, totalMinute_rain = result[0], result[1], result[2], result[3], result[4], result[5]

    return bestDate, bestTime, totalDistance, totalMinute, chanceOfRaining, totalMinute_rain

