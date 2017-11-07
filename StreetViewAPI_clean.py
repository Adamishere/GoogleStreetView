# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 13:29:01 2017
API Key: 
@author: Adam
"""

import requests as r
import pandas as pd
import os
from PIL import Image
from io import BytesIO
from pandas.io.json import json_normalize

os.chdir("")


key = ""
baseurl = "https://maps.googleapis.com/maps/api/streetview?"
metaurl = "https://maps.googleapis.com/maps/api/streetview/metadata?"
heading = ""

#Image Size: max size 640x640
size = "640x640"
#Zoom: default FOV is 90, max 120,
fov = "90"
#Vertical angle
#default pitch is 0, -90 (down) to +90 (Up)
pitch = "0"

location = "Los Angeles, CA, 90071"

request = (baseurl + 
        "location=" + location +
        "&size=" + size +
        "&fov=" + fov +
        "&pitch=" + pitch +
        "&key=" + key)
metarequest = (metaurl + 
        "location=" + location +
        "&size=" + size +
        "&fov=" + fov +
        "&pitch=" + pitch +
        "&key=" + key)

print(request)
print(metarequest)

request_out = r.get(request)
print(request_out)
result = request_out.content

img = Image.open(BytesIO(result))
img.save("test3.jpg")

metarequest_out = r.get(metarequest)
metajson = metarequest_out.json()


metadat = pd.DataFrame(json_normalize(metajson))
metadat["copyright"]
