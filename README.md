# fmi_sounding
Script for downloading and plotting FMI radio soundings launched from Jokioinen and Sodankylä stations
Written by Johannes Mikkola, University of Helsinki, contact: johannes.mikkola[at]helsinki.fi

getfmi.py
  - Download FMI sounding data
  - Command line arguments: python getfmi.py stationid time
      * stationid = 101104 for Jokioinen, 101932 for Sodankylä
      * time = YYYY-MM-DDTHH:MM:SSZ in UTC
    Data available since ~2006
    Jokioinen 12am and 12pm, since ~Dec 2016 also 6am and 6pm
    Sodankylä 12am and 12pm

    Since Dec 2016 the data is provided on 2 seconds resolution, before that on some selection of pressure levels


plotfmi.py
  - Plot FMI sounding data (using the data format produced by getfmi.py)


Example:

python getfmi.py 101104 2023-08-14T18:00:00T

python plotfmi.py 101104 2023-08-14T18:00:00T
