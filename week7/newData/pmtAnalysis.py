#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 14:18:02 2018

@author: vladgriguta
"""
import pandas as pd

# Read SN events decay time
time_SN_vis = pd.read_csv('time_SN_vis.txt')
time_SN_vuv = pd.read_csv('time_SN_vuv.txt')

# Concatenate all into a new DataFrame object
time_SN_vuv['vuv'] = 1
time_SN_vis['vuv'] = 0
frames = [time_SN_vuv,time_SN_vis]
timeSN = pd.concat(frames)
timeSN = timeSN.sort_values('time')
timeSN = timeSN.reset_index(drop=True)

# Read the events as well
SNevents = pd.read_csv('events_SN.txt')


#numPhotons = timeSN['event'=0].groupby('')
#SNevents['numPhotons'] = numPhotons['time']


# want to find out which PMTs are excited in each SN event

