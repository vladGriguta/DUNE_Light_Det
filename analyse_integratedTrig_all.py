# analyse_new.py
# This code checks the efficiency of a trigger on SN events 


# import the module

import matplotlib.pyplot as plt
import numpy as np;
import pandas as pd;
import allFunctions

# Global variables
resolution  = 0.05 # 50 nanoseconds in microseconds
SN_event_time = 10 # Over 80% of SN signal is recorded within 0.1 microseconds
# Usual number of bins in which a SN is recorded
SN_event_nr_bins = int(SN_event_time/resolution)
trigDuration = 10. #microseconds


# open the files
readFileSN = open('time_SN.txt','r')
readFileAr39 = open('time_Ar39.txt','r')
readFileEvents = open('events_SN.txt','r')
simulationTime = 2.5 * 1000000 #2.5 seconds in microseconds


# create empty arrays
timeSN = [];
timeAr = [];
time = [];
eventsSN = [];

# read the SN file
for line in readFileSN:
    # split the input line based on a comma
    splitUp = line.split(",");
    # The lines of interest have plenty of data
    for i in range(0,len(splitUp)):
        try:
            timeSN.append(float(splitUp[i].replace(' ','')))
            time.append(timeSN[i]);
        except:
            print(splitUp[i])

# read the Ar39 file
for line in readFileAr39:
    # split the input line based on a comma
    splitUp = line.split(",");
    # The lines of interest have plenty of data
    for i in range(0,len(splitUp)):
        try:
            timeAr.append(float(splitUp[i].replace(' ','')))
            time.append(timeAr[i])
        except:
            print(splitUp[i])
                      
            

# read the SN events file
lineNr = 0
for line in readFileEvents:
    # split the input line based on a comma
    splitUp = line.split(",");
    # Create list of arrays
    eventsSN.append([])
    for i in range(0,len(splitUp)):
        try:
            eventsSN[lineNr].append(float(splitUp[i].replace(' ','')))
        except Exception as ex:
            print(ex)
            print(splitUp[i])
    lineNr = lineNr + 1

eventsSN = pd.DataFrame(eventsSN, columns = ['energy','distanceToAnode','eventTime'])
# eventTime wrongly saved in seconds. Convert to micro seconds (x1e6)
eventsSN.loc[:,'eventTime'] *= 1000000

# Sort all arrays of time
time = np.sort(time)
timeSN = np.sort(timeSN)
timeAr = np.sort(timeAr) 
eventsSN = eventsSN.sort_values('eventTime')

# Divide data into "steps" given by the resolution
events = allFunctions.DivideDataByRes(resolution,time,simulationTime)

"""
for i in range(0,len(eventsSN)):
    eventsSN['arrivalTime'][i] = np.array

for i in range(0,len(eventsSN)-1):
    j = 0
    while(timeSN[j]<eventsSN['eventTime'][i+1]):
        eventsSN['arrivalTime'][i].append(timeSN[j])
        j += 1
        print(j)
    i +=1
    print(i)
"""




"""
mean_events = np.mean(events)
# Threshold imposed on the variation from the mean within the interval an
# usual SN event is recorded
threshold = 7 * (SN_event_nr_bins*mean_events)
[SNCandidates, fakeTrig, SNTrig] = allFunctions.Candidates(events, SN_event_nr_bins, threshold, SN_event_time, eventsSN,trigDuration,resolution)

trigEf = 100 * np.sum(SNCandidates>0)/len(SNCandidates)
fakeRate = len(fakeTrig) / (simulationTime/1000000)
print(trigEf)
print(fakeRate)
# Add SNTrig to eventsSN
eventsSN['TriggerResponse'] = SNCandidates.tolist()
"""



# Grid search to find optimum threshold and SN_event_time
thresholdVals = [5,7,10,13,15]
SN_event_timeVals = np.linspace(3,7,num=10)

[df_eff, df_fake] = allFunctions.GridSearch(events, thresholdVals, SN_event_timeVals, eventsSN, trigDuration,resolution)

X, Y = np.meshgrid(list(map(float, df_eff.index)),list(map(float, df_eff.columns)))

allFunctions.PlotGridSearch(df_eff,efficiency=True)
allFunctions.PlotGridSearch(df_fake,efficiency=False)

df_eff.to_csv('efficienciesNov.csv', sep=',')
df_fake.to_csv('fakeEventsNov.csv', sep=',')

#allFunctions.Plot_Trigger_Distrib(eventsSN,trigEf,fakeRate,threshold,SN_event_nr_bins,mean_events,SN_event_time)

# allFunctions.SVMClass(eventsSN)


