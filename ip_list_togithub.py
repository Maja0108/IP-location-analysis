#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 13 13:29:31 2018

@author: afonya
"""
"""
This small code collects the location information of several IP adresses, and 
analyse the frequency of the IP addresses in a given file.  
"""
import pandas as pd
import seaborn as sns
import requests
import time

# First I create a new dictionary for the frequency calculations, then I load
# the dataset in chunks, the original file contains more than 8 hundred thousand lines.

IP_dict = {}

for ip_list_chunk in pd.read_csv('ip_list.txt', delim_whitespace = True, 
                                 header = None, chunksize = 1000):
    ip_list_chunk.columns = ['Month', 'Day', 'Hour', 'Host', 'Proxy', 'IP_port',
                             'Datestamp', 'Localnodes', 'Container', 'ize1', 
                             'ize2', 'ize3', 'ize4', 'ize5' ]
    #IP adresses and ports are in one column in the original dataset, so I make
    #2 new columns.
    ip_list_chunk['IP'] = ip_list_chunk['IP_port'].str.slice(0,-6)
    ip_list_chunk['port'] = ip_list_chunk['IP_port'].str.slice(-6)
    
    for ip in ip_list_chunk['IP']:
        if ip in IP_dict:
            IP_dict[ip] += 1
        else:
            IP_dict[ip] = 1
    #print(ip_list_chunk.head())
    
       
# Frequency and outliers in IP dataset, for easier work I converted the dictionary to DataFrame
values_dict = list(IP_dict.values())
ax = sns.boxplot(x = values_dict)

IP_df = pd.DataFrame(list(IP_dict.items()), columns =['IP', 'counts'])

print(max(IP_df.counts))

IP_df_1 = IP_df[IP_df['counts']==1]
between = (IP_df['counts'] > 1) & (IP_df['counts'] < 11)
IP_df_2_10 = IP_df[between]
between2 = (IP_df['counts'] > 10) & (IP_df['counts'] < 101)
IP_df_11_100 = IP_df[between2]
IP_df_1arge = IP_df[IP_df['counts'] > 100]


#Get the location data of the IP adresses, the IP-API allow 150 requests/min, so
# I give some sleep-time, so ensure this requesting rate.
 
IP = list(IP_df['IP'])

res = pd.DataFrame()

for ip in IP:
    
    url = 'http://ip-api.com/json/'+ip 
    #print(url)
    response = requests.get(url)
    dict_jsondata = response.json()
    #print(response)

    response_df = pd.DataFrame.from_dict(dict_jsondata, orient = 'index')
    df_T = response_df.transpose()
    res = res.append(df_T)
    time.sleep(0.5)
    

res = res.reset_index()
res.to_csv('ip_location.csv')