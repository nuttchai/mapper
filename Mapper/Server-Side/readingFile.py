import csv
import asyncio

async def readFile(name):
    with open(name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        return list(csv_reader)
        