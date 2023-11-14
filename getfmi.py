# coding=utf-8

#parsing FMI sounding data to .txt file
#Johannes Mikkola, 06/2018, last modified 11/2023

import os,sys,string,requests
import xml.etree.ElementTree as ET
import numpy as np

#command line arguments:
#(scriptname) station id, time
#e.g.
#python getfmi.py 101104 2018-08-12T12:00:00Z

station=sys.argv[1]     # Jokioinen - 101104, Sodankylä - 101932
time=sys.argv[2]        # YYYY-MM-DDTHH:MM:SSZ
	                    # Jokioinen 12am, 12pm, since Dec 2016 also 6am and 6pm
                        # Sodankyla 12am and 12pm

url = 'https://opendata.fmi.fi/wfs?request=getFeature&storedquery_id=fmi::observations::weather::sounding::multipointcoverage&fmisid=' + station + '&starttime=' + time + '&endtime=' + time + '&'
print(url)

#url->XML->tree->root
req = requests.get(url)
xmlstring = req.content
tree=ET.ElementTree(ET.fromstring(xmlstring))
root = tree.getroot()

#reading location and time data to "positions" from XML
try:
    for elem in root.iter(tag='{http://www.opengis.net/gmlcov/1.0}positions'):
        positions = elem.text

    #'positions' is string type variable
    #--> split positions into a list by " "
    #then remove empty chars and "\n"
    # from pos_split --> data into positions_data
    pos_split = positions.split(' ')
    positions_data = []
    for i in range(0,len(pos_split)):
        if not (pos_split[i] == "" or pos_split[i] == "\n"):
            positions_data.append(pos_split[i])

except:
    print("----------------------------------")
    print("No data -- check the date and time")
    print("----------------------------------")
    exit()

#index for height: 2,6,10 etc in positions_data
height = []
pos = range(2,len(positions_data))
for i in pos[::4]:
    height.append(positions_data[i])

#reading wind speed, wind direction, air temperature and dew point data to 'values'
for elem in root.iter(tag='{http://www.opengis.net/gml/3.2}doubleOrNilReasonTupleList'):
    values = elem.text

#split 'values' into a list by " "
#then remove empty chars and "\n"
val_split = values.split(' ')
values_data = []
for i in range(0,len(val_split)):
    if not(val_split[i] == "" or val_split[i]=="\n"):
        values_data.append(val_split[i])

#data in values_data: w_speed, w_dir, t_air, t_dew
p = []
w_speed = []
w_dir = []
t_air = []
t_dew = []
indeces = range(0,len(values_data))
for i in indeces[::5]:
    p.append(values_data[i])
    w_speed.append(values_data[i+1])
    w_dir.append(values_data[i+2])
    t_air.append(values_data[i+3])
    t_dew.append(values_data[i+4])

#read location and time from XML
for elem in root.iter(tag='{http://www.opengis.net/gml/3.2}timePosition'):
    time = elem.text

for elem in root.iter(tag='{http://www.opengis.net/gml/3.2}name'):
    location = elem.text

locationstr=location.replace(u'ä','a').replace(u'ö','o').replace(" ","_")

#create text file
outfilename = locationstr + "_" + str(time) + ".txt"
outfilename = outfilename.replace(":","_").replace("-","_")
outfile = open(outfilename,"w")

#writing data to text file
indeces = range(0,len(p))

#height pressure w_speed w_dir T_air T_dew
#before 2015: pressure w_speed w_dir T_air RH
for i in indeces[::1]:
    str2 = str(height[i]) + " " + str(p[i]) + " " + str(w_speed[i]) + " " + str(w_dir[i] + " " + str(t_air[i]) + " " + str(t_dew[i]) + '\n')
    outfile.write(str2)

outfile.close()
