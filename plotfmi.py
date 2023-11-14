# coding=utf-8
#Python script for plotting FMI open data radiosounding as Skew-T
#Johannes Mikkola, last modified 11/2023
#All you (should) need is MetPy-package
#https://unidata.github.io/MetPy/latest/api/generated/metpy.plots.SkewT.html

import numpy as np
import sys,os
import matplotlib.pyplot as plt
from metpy.plots import SkewT
from metpy.units import units
from metpy.calc import wind_components
from metpy.calc import dewpoint_from_relative_humidity

try:
    station=sys.argv[1]     # Jokioinen - 101104, Sodankylä - 101932
    time=sys.argv[2]        # YYYY-MM-DDTHH:MM:SSZ

    if station=="101104":
        infile = "Jokioinen_Ilmala_"+time.replace("-","_").replace(":","_")+".txt"
    elif station=="101932":
        infile = "Sodankyla_Tahtela_"+time.replace("-","_").replace(":","_")+".txt"

    print(infile)
    data = np.loadtxt(infile)
except:
    print("Check command line input and the data file.")
    exit()


#apply MetPy units
hgt = data[:,0]*units.m
pres = data[:,1]*units.hPa
wspd = data[:,2]*units.mps
wdir = data[:,3]*units.degrees
uu, vv = wind_components(wspd,wdir)
uu, vv = 1.94*uu*units.knots, vv*1.94*units.knots
temp = data[:,4]*units.degC

#after 16 Dec 2014 dew point temperature and data every 2 seconds
if data[:,5].min() < 0:
    dew_point = data[:,5]*units.degC
    wind_averaging = True
#before 16 Dec 2014 relative humidty and data every somewhat levels
else:
    dew_point = dewpoint_from_relative_humidity(temperature=temp,rh=0.01*data[:,5])
    wind_averaging = False

#plotting
fig = plt.figure(figsize=(9,9))
skew = SkewT(fig, rotation=45) #rotation=0 would plot emagram
skew.plot(pres, temp, 'k',label="T",zorder=3)
skew.plot(pres, dew_point, 'b',label="Td",zorder=2)

#plot limits
pbot, ptop = 1020, 100 #hPa
tmin, tmax = -40, 40 #C
#average winds over the plotting "density"
uu_mean = uu.copy()
vv_mean = vv.copy()

if wind_averaging:
    every_ith = 25 #Average and plot wind on every_ith levels
    for ii in range(every_ith,uu.shape[0]-every_ith):
        uu_mean[ii] = np.nanmean(uu[ii-every_ith:ii+every_ith])
        vv_mean[ii] = np.nanmean(vv[ii-every_ith:ii+every_ith])
    skew.plot_barbs(pres[pres>ptop*units("hPa")][::2*every_ith],
                    uu_mean[pres>ptop*units("hPa")][::2*every_ith],
                    vv_mean[pres>ptop*units("hPa")][::2*every_ith])
else:
    skew.plot_barbs(pres[pres>ptop*units("hPa")],
                    uu[pres>ptop*units("hPa")],
                    vv[pres>ptop*units("hPa")])


skew.plot_dry_adiabats(np.arange(-30,100,10.0)*units.degC,alpha=0.4,label="$\\Gamma _d$")
skew.plot_moist_adiabats(np.arange(-30,100,10.0)*units.degC,alpha=0.4,label="$\\Gamma _m$")
skew.plot_mixing_lines(color="gray",alpha=0.8)

plt.ylabel("Pressure (hPa)")
plt.xlabel("Temperature ($^\\circ$C)")
title = infile.replace(".txt","").replace("_"," ")
plt.title(title)

yticks = np.arange(ptop,1021)[::50]
yticklabels = yticks.copy().astype(str)
yticklabels[yticks%100!=0] = ""

xticks = np.arange(-80,51)[::5]
xticklabels = xticks.copy().astype(str)
xticklabels[xticks%10!=0] = ""

skew.ax.set_yticks(yticks)
skew.ax.set_yticklabels(yticklabels)
skew.ax.set_xticks(xticks)
skew.ax.set_xticklabels(xticklabels)

#Bolded lines and fix upper left corner in the grid
for T in np.arange(-140,51)[::10]:
    skew.ax.plot([T,T],[1020,100],'k',alpha=.5,zorder=1)

for p in np.arange(100,1001)[::100]:
    skew.ax.plot([-140,51],[p,p],'k',alpha=.5,zorder=1)

for T in np.arange(-140,-79)[::5]:
    skew.ax.plot([T,T],[1020,100],'gray',alpha=.5,linewidth=0.5,zorder=1)

plt.ylim(pbot,ptop)
plt.xlim(tmin,tmax)

figname = infile.replace(".txt",".pdf")
plt.savefig(figname,bbox_inches = 'tight',dpi=300)
figname = infile.replace(".txt",".png")
plt.savefig(figname,bbox_inches = 'tight',dpi=300)
