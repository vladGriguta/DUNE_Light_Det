#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  4 13:53:15 2018

@author: vladgriguta
"""

import pandas as pd;

def readWeek7():
    # Read Ar39 decay time
    time_Ar_vis = pd.DataFrame()
    time_Ar_vis = pd.read_csv('time_Ar_vis.txt')
    time_Ar_vuv = pd.DataFrame()
    time_Ar_vuv = pd.read_csv('time_Ar_vuv.txt')
    
    # Concatenate all into a new DataFrame object
    time_Ar_vuv['vuv'] = 1
    time_Ar_vis['vuv'] = 0
    frames = [time_Ar_vuv,time_Ar_vis]
    timeAr = pd.concat(frames)
    timeAr = timeAr.sort_values('time')
    # 'event' column not properly saved
    timeAr = timeAr.drop(columns=['event'])
    
    
    # Read SN events decay time
    time_SN_vis = pd.DataFrame()
    time_SN_vis = pd.read_csv('time_SN_vis.txt')
    time_SN_vuv = pd.DataFrame()
    time_SN_vuv = pd.read_csv('time_SN_vuv.txt')
    
    # Concatenate all into a new DataFrame object
    time_SN_vuv['vuv'] = 1
    time_SN_vis['vuv'] = 0
    frames = [time_SN_vuv,time_SN_vis]
    timeSN = pd.concat(frames)
    timeSN = timeSN.sort_values('time')
    
    return timeSN, timeAr
