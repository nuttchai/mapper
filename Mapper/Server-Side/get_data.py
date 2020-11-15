#!/usr/bin/python
# -*- coding:utf-8 -*-
# Copyright 2019 Huawei Technologies Co.,Ltd.
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use
# this file except in compliance with the License.  You may obtain a copy of the
# License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations under the License.

"""
 This sample demonstrates how to download an object
 from OBS in different ways using the OBS SDK for Python.
"""

from __future__ import print_function
import os
from obs import ObsClient

import asyncio


async def download_data():

    AK = 'IJKOCBW6LYDVI6Y1WW0Q'
    SK = '7SCcFD6ROXwCAN1B5ios2tapwhvsStZMG1qxrOxy'
    server = 'https://obs.ap-southeast-2.myhuaweicloud.com'
    bucketName = 'obs-mapper-cie'

    objectKey = 'Data/Weather/Bangkok.csv'
    localFile = 'Data/Weather/Bangkok.csv'

    objectKey2 = 'Data/TrafficCondition/AverageSpeed/AverageSpeed.csv'
    localFile2 = 'Data/TrafficCondition/AverageSpeed/AverageSpeed.csv'

    objectKey3 = 'Data/Road/RoadInformation.csv'
    localFile3 = 'Data/Road/RoadInformation.csv'

    obsClient = ObsClient(access_key_id=AK, secret_access_key=SK, server=server)


    # print('Downloading an object as a socket stream\n')
    # print('Downloading an object to :' + localFile + '\n')
    resp = obsClient.getObject(bucketName, objectKey, downloadPath=localFile)
    resp2 = obsClient.getObject(bucketName, objectKey2, downloadPath=localFile2)
    resp3 = obsClient.getObject(bucketName, objectKey3, downloadPath=localFile3)

# asyncio.run(download_data())