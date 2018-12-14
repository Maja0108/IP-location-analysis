#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 14 06:37:45 2018

@author: afonya
"""
"""
This code visualise the location of the IP adresses.
"""
import pandas as pd
import seaborn as sns
import folium

ip_location = pd.DataFrame()

for ip_location_chunk in pd.read_csv('ip_location.csv', chunksize = 1000):
    ip_location = ip_location.append(ip_location_chunk)
   
#print(ip_location.describe())    
#print(ip_location.info)
#print(ip_location.dtypes)


#Frequency count of locations
country = ip_location['country']
g = sns.catplot(y='country', kind = 'count', data = ip_location)
g.set(xscale = 'log')
g.savefig('distribution.jpg')

#Visualisation of the loactions in a map
ip_location_noNan =  ip_location.drop(['message'], axis = 1).dropna()

m = folium.Map(location = [20, 0], tiles = "Mapbox Bright", zoom_start = 2)
for i in range(0, len(ip_location_noNan)):
    folium.Marker([ip_location_noNan.iloc[i]['lat'], ip_location_noNan.iloc[i]['lon']]).add_to(m)
    
m.save('ip_location.html')
