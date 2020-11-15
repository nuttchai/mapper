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

# AK = 'N02JFWTL4SEDYUQSWNLF'
# SK = '9x5ZJ1HoXkI4L9NuOBTdsxQ2eFDh3txBohqGonT8'
# server = 'https://obs.ap-southeast-2.myhuaweicloud.com'
# bucketName = 'obs-mapper'
# objectKey = 'ClientData/testUpload.txt'

async def upload_file(objectKey,FilePath):
    # AK = 'N02JFWTL4SEDYUQSWNLF'
    # SK = '9x5ZJ1HoXkI4L9NuOBTdsxQ2eFDh3txBohqGonT8'
    # server = 'https://obs.ap-southeast-2.myhuaweicloud.com'
    # bucketName = 'obs-mapper'
    AK = 'IJKOCBW6LYDVI6Y1WW0Q'
    SK = '7SCcFD6ROXwCAN1B5ios2tapwhvsStZMG1qxrOxy'
    server = 'https://obs.ap-southeast-2.myhuaweicloud.com'
    bucketName = 'obs-mapper-cie'
    # Constructs a obs client instance with your account for accessing OBS
    obsClient = ObsClient(access_key_id=AK, secret_access_key=SK, server=server)
    
    # Upload an object to your bucket
    print('Uploading a new object to OBS from a file\n')
    obsClient.putFile(bucketName, objectKey, FilePath)

# asyncio.run(upload_file())