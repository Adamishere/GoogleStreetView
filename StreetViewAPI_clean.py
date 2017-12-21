##########################
# Expected File Structure#
##########################
# Main
#   main.py
#   L_ Coords
#       1001.xlsx
#       ...
#       1302.xlsx
#       L_ Processed Lists
#   L_ Images
#       Street View 1001_0.jpg
#       ...
#
#
#
#
#
#Street View API Key: 
#Geocoding API Key: 
#@author: Adamishere
#
import re as re
import requests as r
import pandas as pd
import os
from PIL import Image
from io import BytesIO
#from pandas.io.json import json_normalize

#Set Workspace
os.chdir("")

#Google API Keys
geo_key = ""
sv_key = ""

################################################################
#Read Folder for DA's, create list of DA's
files = os.listdir("./Coords/")

#Define Regex pattern
regex = re.compile("\d+")

#store files with number in a list
selectfiles = list(filter(regex.match,files))

#check
print(selectfiles)

#########################################################
for z in selectfiles:

    #return DA id
    z2 = re.search(r"\d+",z)[0]

    coords = pd.read_excel(("./Coords/"+z))
    len(coords)

    #Parse (##.###,-##.###) into lat and long
    coords["lat"] = 0
    coords["lng"] = 0
    for x in range(0,len(coords)):
        coords.loc[x,("lat")] = re.findall(r"\-?\d+.\d+",coords["latlong"][x])[0]
        coords.loc[x,("lng")] = re.findall(r"\-?\d+.\d+",coords["latlong"][x])[1]

    #Intialize Dataframe:
    columns = ["da", "lat","lng", "address","maplink","status","image","streetlink","MURB Eligible (1/0)", "Building Name","Revised Address", "Coder Comments"]
    df = pd.DataFrame(index=range(0,len(coords)), columns=columns)

    #Google Geocode settings:
    geo_request = "https://maps.googleapis.com/maps/api/geocode/json?address="

    #Google Streetview settings:
    baseurl = "https://maps.googleapis.com/maps/api/streetview?"
    metaurl = "https://maps.googleapis.com/maps/api/streetview/metadata?"
    heading = ""

    #Image Size: max size 640x640
    size = "640x640"
    #Zoom: default FOV is 90, max 120,
    fov = "90"
    #Vertical angle
    #default pitch is 0, -90 (down) to +90 (Up)
    pitch = "10"

    #############################
    #Loop through coords dataset#
    #############################
    for i in range(0,len(coords)):

        da = coords["da"][i]
        lat = coords["lat"][i]
        lng = coords["lng"][i]

        #Reverse geo coding to get address from Lat and Long
        r_loc = str(lat)+","+str(lng)
        request = geo_request + r_loc + "&key=" + geo_key
        request_out = r.get(request)

        #Live Status Check
        print(request_out)

        result = request_out.json()
        df["status"][i]         = request_out
        df["da"][i]        = da
        df["lat"][i]       = lat
        df["lng"][i]       = lng
        df["address"][i]   = result["results"][0]["formatted_address"]
        df["maplink"][i]      = "https://www.google.com/maps/place/"+r_loc
        df["streetlink"][i]      = "http://maps.google.com/maps?q=&layer=c&cbll="+r_loc

        #Extract Street View Image:
        request = (baseurl +
                "location=" + r_loc +
                "&size=" + size +
                "&fov=" + fov +
                "&pitch=" + pitch +
                "&key=" + sv_key)

        #print(request)
        #print(metarequest)

        request_out = r.get(request)
        print(request_out)
        result = request_out.content

        img = Image.open(BytesIO(result))

        #save image name in dataframe
        #File name:
        filename = "Images/Street View "+str(da)+"_"+str(i)+".jpg"
        df["image"][i]          = filename
        img.save(filename)
    #Save DA log data
    df.to_excel("Google Geocoding Log ("+z2+").xlsx")

    #Move Coord List to Processed folder to make program safe for reruns.
    os.rename("./Coords/"+z, "./Coords/Processed Lists/"+z)



True==True

#
#    metarequest = (metaurl +
#            "location=" + r_loc +
#            "&size=" + size +
#            "&fov=" + fov +
#            "&pitch=" + pitch +
#            "&key=" + sv_key)
#
#metarequest_out = r.get(metarequest)
#metajson = metarequest_out.json()
#
#
#metadat = pd.DataFrame(json_normalize(metajson))
#metadat["copyright"]
