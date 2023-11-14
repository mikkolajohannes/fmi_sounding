# fmi_sounding
Script for downloading and plotting FMI operational sounding launched in Jokioinen and Sodankylä stations
Written by Johannes Mikkola, University of Helsinki, contact: johannes.mikkola[at]helsinki.fi

getfmi.py
  - run this file for downloading the FMI sounding data to .txt file
  - command line arguments: python getfmi.py stationid time
      * stationid = 101104 for Jokioinen, 101932 for Sodankylä
      * time = YYYY-MM-DDTHH:MM:SSZ in UTC
    Data available since ~2006
    Jokioinen 12am and 12pm, since ~Dec 2016 also 6am and 6pm
    Sodankylä 12am and 12pm

Example:
python getfmi.py 101104 2023-08-14T18:00:00T
python plotfmi.py 1014 2023-08-14T18:00:00T

plotfmi.py
  - use the same command line arguments to plot the sounding on Skew-T
