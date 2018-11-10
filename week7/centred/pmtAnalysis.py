#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 14:18:02 2018

@author: vladgriguta
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import functionsWeek7

timeSN,nr_events_SN = functionsWeek7.Read_SN_W7()
timeAr,nr_events_Ar = functionsWeek7.Read_Ar39_W7()

# Read the light bars data
bars = pd.read_csv('bars_positions_dune1x2x6.txt',delim_whitespace=True,
                   names=['index','x','y','z'])
bars = bars.drop(columns=['index'])


functionsWeek7.PlotBarsDistribution(event='SN',bars=bars,time=timeSN,
                                    nr_events=nr_events_SN)
functionsWeek7.PlotBarsDistribution(event='Ar',bars=bars,time=timeAr,
                                    nr_events=nr_events_Ar)

# Now try the Ar39 events




#numPhotons = timeSN['event'=0].groupby('')
#SNevents['numPhotons'] = numPhotons['time']


# want to find out which PMTs are excited in each SN event

