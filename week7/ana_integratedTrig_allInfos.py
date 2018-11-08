#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  4 13:55:21 2018

@author: vladgriguta
"""

import numpy as np;
import pandas as pd;
import matplotlib.pyplot as plt
import allFunctions
import readFiles

timeSN, timeAr = readFiles.readWeek7()

SNevents = pd.read_csv('events_SN.txt')


# Try a K-means clustering
import week7Functions
columns = ['vuv','x','pmt']
#labels, centres = week7Functions.KMeansClustering3(timeAr,columns,n_clusters=2)












"""
# Code from Oana to draw scatter plot with colorbar + text

X = np.array(timeAr[columns])
numPhotons = timeSN.groupby('event').count()
SNevents['numPhotons'] = numPhotons['time']


plt.figure()
plt.scatter(SNevents['energy'].values, SNevents['numPhotons'].values/SNevents['energy'].values, c = SNevents['x'], s = 100, cmap = 'Blues')
cbar = plt.colorbar()
cbar.set_label('coordinate [cm]', rotation = 270, labelpad=30, y=0.5, fontsize = 18)
plt.xlabel('E_event [MeV]', fontsize = 20)
plt.ylabel('Photons detected/event/energy', fontsize = 20 )
plt.show()
#plt.savefig('Entriesperenergy_vs_energy_SN_{:s}.jpg'.format(coord), format = 'jpg')
"""


"""
# Some tests from last week

# Global variables
resolution  = 0.05 # 50 nanoseconds in microseconds
SN_event_time = 10 # Over 80% of SN signal is recorded within 0.1 microseconds
# Usual number of bins in which a SN is recorded
SN_event_nr_bins = int(SN_event_time/resolution)
trigDuration = 10. #microseconds
simulationTime = 2.5 * 1000000 #2.5 seconds in microseconds

# Grid search to find optimum threshold and SN_event_time
thresholdVals = [5,7,10,13,15]
SN_event_timeVals = [0.5,2,5,10,15,20,25,35]

"""




