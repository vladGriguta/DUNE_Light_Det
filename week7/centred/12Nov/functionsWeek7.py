#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 10:59:10 2018

@author: vladgriguta
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def PlotBarsDistribution(event,bars,time,nr_events):
    
    z = np.sort(list(set(bars['z'])))
    y = np.sort(list(set(bars['y'])))
    
    # Create arrays corresponding to the edges of each light bar
    z_diff = np.mean(np.diff(z))/2.
    z_edges = z - z_diff
    z_edges = np.append(z_edges,[np.max(z)+z_diff])
    
    y_diff = np.mean(np.diff(y))/2.
    y_edges = y - y_diff
    y_edges = np.append(y_edges,[np.max(y)+y_diff])
    
    # Create an array storing each 
    pmtCounts = np.zeros((len(y),len(z)))
    # Convert from pmt number to 
    for i in range(len(time)):
        pmtCounts[int(time['pmt'][i]%len(y))][int(time['pmt'][i] / len(y))] += 1
    
        
    # Normalise the number of counts (i.e. divide by number of events for SN,
    # or by another appropriate number for Ar39 events
    if(event == 'SN'):
        pmtCounts = pmtCounts/float(nr_events)
        # Extension: do the plot the Standard deviation
        # Plan: Easy, save photons as per SN event
        std_pmtCounts_SN = np.zeros((len(set(time['event'])),len(y),len(z)))
        for i in range(len(time)):
            std_pmtCounts_SN[int(time['event'][i])][int(time['pmt'][i]%len(y))][int(time['pmt'][i] / len(y))] += 1
        std_pmtCounts_SN = np.std(std_pmtCounts_SN,axis=0)
        
        
    elif(event == 'Ar'):
        # Plan: Save data as per interval of delta_t us (for Ar39)
        delta_t = 2.5
        
        simulationTime = np.max(time['time']) # in microseconds
        pmtCounts = pmtCounts * delta_t / float(simulationTime)  # normalise as per microsecond
                                                                 # for now
        # measure of the total number of photons from Ar in delta_t
        print('Mean number of Ar photons in '+str(delta_t)+' is '+str(np.sum(pmtCounts))) 
        
        # Extension: do the plot the Standard deviation
        simulationTime = np.max(time['time']) # in microseconds
        std_pmtCounts_Ar = np.zeros((int(simulationTime/delta_t)+1,len(y),len(z)))
        for i in range(len(time)):
            std_pmtCounts_Ar[int(time['time'][i]/delta_t)][int(time['pmt'][i]%len(y))][int(time['pmt'][i] / len(y))] += 1
        std_pmtCounts_Ar = np.std(std_pmtCounts_Ar,axis=0)
    
    X,Y = np.meshgrid(z_edges,y_edges)
    if(event == 'SN'):
        plt.pcolormesh(X,Y,pmtCounts,vmin=0,vmax=5.5)
        cbar = plt.colorbar()
        plt.xlabel('Z / cm')
        plt.ylabel('Y / cm')
        cbar.set_label('Mean photons per SN event', rotation = 270, labelpad=30, y=0.5, fontsize = 18)
        plt.title('SN events')
        plt.savefig('SN_PMTDistrib.png')
        plt.close()
        # Extension
        plt.pcolormesh(X,Y,3*std_pmtCounts_SN,vmin=0,vmax=5.5)
        cbar = plt.colorbar()
        plt.xlabel('Z / cm')
        plt.ylabel('Y / cm')
        cbar.set_label('3*STD(photons) per SN event', rotation = 270, labelpad=30, y=0.5, fontsize = 18)
        plt.title('SN events')
        plt.savefig('SN_PMTDistrib_std.png')
        plt.close()
    elif(event == 'Ar'):
        plt.pcolormesh(X,Y,pmtCounts,vmin=0)
        cbar = plt.colorbar()
        plt.xlabel('Z / cm')
        plt.ylabel('Y / cm')
        cbar.set_label('Mean photons per '+str(delta_t)+' us', rotation = 270, labelpad=30, y=0.5, fontsize = 18)
        plt.title('Ar39 events')
        plt.savefig('Ar39_PMTDistrib_1us.png')
        plt.close()
        # Extension
        plt.pcolormesh(X,Y,3*std_pmtCounts_Ar,vmin=0)
        cbar = plt.colorbar()
        plt.xlabel('Z / cm')
        plt.ylabel('Y / cm')
        cbar.set_label('3*STD(photons) per '+str(delta_t)+' us', rotation = 270, labelpad=30, y=0.5, fontsize = 18)
        plt.title('Ar39 events')
        plt.savefig('Ar39_PMTDistrib_5us_std.png')
        plt.close()
        
    
def Read_SN_W7():
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
    del time_SN_vis, time_SN_vuv
    
    nr_events_SN = int(np.max(timeSN['event']))+1
    
    return timeSN,nr_events_SN

def Read_Ar39_W7():
    # Read SN events decay time
    time_Ar_vis = pd.read_csv('time_Ar_vis.txt')
    time_Ar_vuv = pd.read_csv('time_Ar_vuv.txt')
    
    # Concatenate all into a new DataFrame object
    time_Ar_vuv['vuv'] = 1
    time_Ar_vis['vuv'] = 0
    frames = [time_Ar_vuv,time_Ar_vis]
    timeAr = pd.concat(frames)
    timeAr = timeAr.sort_values('time')
    timeAr = timeAr.reset_index(drop=True)
    del time_Ar_vis, time_Ar_vuv
    
    nr_events_Ar = int(np.max(timeAr['event']))+1
        
    return timeAr,nr_events_Ar


