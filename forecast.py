#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 10:09:33 2017

@author: lolo
"""

#Import tools for the database
import csv
import sqlite3

import random
from random import uniform

import datetime
import inspect
import os

#scientific python add-ons
import numpy as np
import pandas as pd
import pvlib




#plotting stuff

import matplotlib.pyplot as plt
import matplotlib as mpl
 #seaborn to makes plots look better
try : 
    import seaborn as sns
    sns.set(rc={"figure.figsize": (12, 6)})
    sns.set_color_codes()
except ImportError:
    print('install seaborn')

#import pvlib library
from pvlib import solarposition, irradiance, atmosphere, pvsystem
from pvlib.forecast import GFS, NAM, NDFD, RAP, HRRR


######################Reading the text file and transform it into a csv file########################

column_names = ["Station", "Date", "irradiation", "temperature","wind_speed"]
meteo = pd.read_csv("//home//lolo//AnacondaProjects//Projet//expose.txt", sep=";", index_col=1, header = 0,  names = column_names, parse_dates=True, infer_datetime_format=True)
ir = meteo['irradiation']
temp = meteo.iloc[:,2]
ws = meteo.iloc[:,3]



df = pd.DataFrame(meteo, columns =["Station", "irradiation", "temperature","wind_speed"] )


df.to_csv('//home//lolo//AnacondaProjects//Projet//Data.csv')

###########################create the database###################################################

conn = sqlite3.connect('Forecast.db')
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS Meteo(Date, station, irradation, temperature, wind_speed)")
c.execute("DELETE FROM Meteo")
'Data.csv'.encode('utf-8')
with open('Data.csv') as f:
            reader = csv.reader(f)
            for field in reader:
                c.execute("INSERT INTO Meteo VALUES (?,?,?,?,?);", field)

c.execute("DELETE FROM Meteo WHERE rowid = 1")

#####################picking the data needed##################################################

c.execute('SELECT temperature FROM Meteo')
temp = c.fetchall()
measured_temp =[]
for i in range(len(temp)):
    measured_temp.append(temp[i][0])

    
c.execute('SELECT wind_speed FROM Meteo')
wspeed = c.fetchall()
measured_wspeed =[]
for i in range(len(wspeed)):
    measured_wspeed.append(wspeed[i][0])

         

c.execute('SELECT irradation FROM Meteo')
irrad = c.fetchall()
measured_irrad =[]
for i in range(len(irrad)):
    measured_irrad.append(irrad[i][0])





                


########################################################################################################

#########################################Forecast#######################################################


pvtemps = pvsystem.sapm_celltemp(meteo['irradiation'], meteo['wind_speed'], meteo['temperature'])

sandia_modules = pvsystem.retrieve_sam('SandiaMod')
test = pvlib.pvsystem.PVSystem(surface_tilt=30, surface_azimuth=180, albedo=None, surface_type=None, module='Polycrystalline silicon', module_parameters=None, modules_per_string=1, strings_per_inverter=1, inverter=None, inverter_parameters=None, racking_model='open_rack_cell_glassback', name='Neuchâtel')
sandia_module = sandia_modules.Canadian_Solar_CS5P_220M___2009_


sapm_out = pvsystem.sapm(meteo['irradiation']/1000, pvtemps['temp_cell'], sandia_module)



sapm_out[['p_mp']].plot()
plt.ylabel('DC Power (W)')
plt.savefig('expose')

conn.commit()
c.close
conn.close()



























