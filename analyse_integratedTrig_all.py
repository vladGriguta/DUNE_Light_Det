# analyse_new.py
# This code checks the efficiency of a trigger on SN events 


# import the module

import numpy as np;
import pandas as pd;
import allFunctions


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

# Plan:
# For a given resolution, go through each time frame
# In each resolving step compute the total number of entries in the last dt ns
# compare this to some threshold, chosen by hand, in terms of the std of time
# flag if above threshold
# if within a reasonable time from the actual SN event successful
# otherwise insuccessful
# analyse the cases when insuccessful

resolution  = 0.05 # 50 nanoseconds in microseconds


events = allFunctions.DivideDataByRes(resolution,time,simulationTime)
SN_event_time = 15 # Over 80% of SN signal is recorded within 0.1 microseconds
# Usual number of bins in which a SN is recorded
SN_event_nr_bins = int(SN_event_time/resolution)
mean_events = np.mean(events)
# Threshold imposed on the variation from the mean within the interval an
# usual SN event is recorded
threshold = 7 * (SN_event_nr_bins*mean_events)

trigDuration = 10. #microseconds
[SNCandidates, fakeTrig, SNTrig] = allFunctions.Candidates(events, SN_event_nr_bins, threshold, SN_event_time, eventsSN,trigDuration,resolution)

trigEf = 100 * np.sum(SNCandidates>0)/len(SNCandidates)
fakeRate = len(fakeTrig) / (simulationTime/1000000)
print(trigEf)
print(fakeRate)
# Add SNTrig to eventsSN
eventsSN['TriggerResponse'] = SNCandidates.tolist()



# Grid search to find optimum threshold and SN_event_time
thresholdVals = [5,7,10]
SN_event_timeVals = [0.1,0.5,1,5,10]

[df_eff, df_fake] = allFunctions.GridSearch(events, SN_event_nr_bins, thresholdVals, SN_event_timeVals, eventsSN, trigDuration,resolution)


#allFunctions.Plot_Trigger_Distrib(eventsSN,trigEf,fakeRate,threshold,SN_event_nr_bins,mean_events,SN_event_time)

# allFunctions.SVMClass(eventsSN)

