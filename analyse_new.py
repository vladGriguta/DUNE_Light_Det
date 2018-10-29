# analyse_new.py
# This code checks the efficiency of a trigger on SN events 


# import the module
import matplotlib.pyplot as plt;
import numpy as np;
import pandas as pd;


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
def DivideDataByRes(resolution,time,simulationTime):
    events = np.zeros(int(simulationTime/resolution))
    for i in range(0,len(time)):
        events[int(time[i]/resolution)] += 1
    return events

events = DivideDataByRes(resolution,time,simulationTime)
SN_event_time = 15 # Over 80% of SN signal is recorded within 0.1 microseconds
# Usual number of bins in which a SN is recorded
SN_event_nr_bins = int(SN_event_time/resolution)
mean_events = np.mean(events)
# Threshold imposed on the variation from the mean within the interval an
# usual SN event is recorded
threshold = 7 * (SN_event_nr_bins*mean_events)

def Candidates(events, SN_event_nr_bins, threshold, SN_event_time, eventsSN, trigDuration):
    SNCandidates = np.zeros(len(eventsSN))
    SNTrig = []
    fakeTrig = []
    # Go through the array and get those points where the total number of events
    # counted is above the threshold.
    events_in_region = np.sum(events[0:SN_event_nr_bins])
    progress = 0;
    for i in range(SN_event_nr_bins+1,len(events)):
        # Start by printing progress
        if(i % int(len(events)/10) == 0):
            progress += 10
            print(str(progress) + ' % Completed\n')
        
        # update number of events by substracting the element furthest away from
        # current position and adding the element in current position
        events_in_region = events_in_region - events[i-1-SN_event_nr_bins] + events[i]
        if(events_in_region>threshold):
            time_of_event = (i-float(SN_event_nr_bins/2))*resolution
            # Check if trigger has not activated recently
            no_SN_Trig = 1
            no_fake_Trig = 1
            # Use try-except to avoid error when arrays are empty
            try:
                if(time_of_event-SNTrig[len(SNTrig)-1]<trigDuration):
                    no_SN_Trig = 0
                    #print(time_of_event-SNTrig[len(SNTrig)-1])
            except:
                pass
            try:
                if(time_of_event-fakeTrig[len(fakeTrig)-1]<trigDuration):
                    no_fake_Trig = 0
                    #print(time_of_event-fakeTrig[len(fakeTrig)-1])
            except:
                pass
            if(no_SN_Trig and no_fake_Trig):            
                # Check if flag is within vicinity of an actual SN event
                if(np.min(abs(time_of_event-eventsSN['eventTime'])) < SN_event_time):
                    SNCandidates[np.argmin(abs(time_of_event-eventsSN['eventTime']))] +=1
                    SNTrig.append(time_of_event)
                else:
                    fakeTrig.append(time_of_event)
    

    return SNCandidates, fakeTrig, SNTrig
                

trigDuration = 10. #microseconds
[SNCandidates, fakeTrig, SNTrig] = Candidates(events, SN_event_nr_bins, threshold, SN_event_time, eventsSN,trigDuration = trigDuration)

trigEf = 100 * np.sum(SNCandidates>0)/len(SNCandidates)
fakeRate = len(fakeTrig) / (simulationTime/1000000)
print(trigEf)
print(fakeRate)

# Add SNTrig to eventsSN
eventsSN['TriggerResponse'] = SNCandidates.tolist()


        







"""
from sklearn import svm
from mlxtend.plotting import plot_decision_regions

X = eventsSN[['energy', 'distanceToAnode']]
Y = eventsSN['TriggerResponse']

clf = svm.SVC(decision_function_shape='ovo')
clf.fit(X.values, Y.values)

# Plot Decision Region using mlxtend's awesome plotting function
plot_decision_regions(X=X.values, 
                      y=Y.values.astype(np.integer),
                      clf=clf, 
                      legend=2)

# Update plot object with X/Y axis labels and Figure Title
plt.xlabel(X.columns[0], size=14)
plt.ylabel(X.columns[1], size=14)
plt.title('SVM Decision Region Boundary', size=16)
"""



# Visualizing the results
def Plot_Trigger_Distrib(eventsSN,trigEf,fakeRate,threshold,SN_event_nr_bins,mean_events,SN_event_time):
    # Plot the SN events that did not pass trigger
    X1 = []
    Y1 = []
    c1 = []
    X2 = []
    Y2 = []
    c2 = []
    
    for i in range(0,len(eventsSN)):
        if(eventsSN['TriggerResponse'][i]):
            X1.append(eventsSN['energy'][i])
            Y1.append(eventsSN['distanceToAnode'][i])
            c1.append('blue')
        else:
            X2.append(eventsSN['energy'][i])
            Y2.append(eventsSN['distanceToAnode'][i])
            c2.append('red')
    plt.scatter(X1,Y1,c = c1,label = 'Detected',alpha=0.7)
    plt.scatter(X2,Y2,c = c2,label = 'Undetected',alpha=0.7)
    plt.legend()
    plt.title('Scatter plot of SN events')
    plt.xlabel('Energy / MeV')
    plt.ylabel('Distance to anode / cm')
    textstr = '\n'.join((
        r'$\mathrm{SNEfficiency}=%.2f $' % (trigEf, )+'%',
        r'$\mathrm{FakeEventsRate}=%d s^{-1} $' % (fakeRate, )))
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
    plt.text(25, 375, textstr, fontsize=12,
            verticalalignment='top', bbox=props)
    thr = int(threshold / (SN_event_nr_bins*mean_events))
    plt.savefig('week5/SNtime'+str(SN_event_time)+'.thr'+str(thr) +'.pdf', format='pdf')


Plot_Trigger_Distrib(eventsSN,trigEf,fakeRate,threshold,SN_event_nr_bins,mean_events,SN_event_time)



