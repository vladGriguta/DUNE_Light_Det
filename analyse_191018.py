# read.py
# program for getting used to environment

# import the module
import matplotlib.pyplot as plt;
import numpy as np;






# open the file
readFile = open('time2.txt','r')

# create empty arrays
timeSN = [];
timeAr = [];
time = [];

# read in the file line by line
flag = 0
for line in readFile:
    # split the input line based on a comma
    splitUp = line.split(",");
    # The lines of interest have plenty of data
    if(len(splitUp)>10):
        if(flag == 1):
            for i in range(0,len(splitUp)):
                try:
                    timeAr.append(float(splitUp[i].replace(' ','')))
                    time.append(timeAr[i]);
                except:
                    print(splitUp[i])
        if(flag == 0):
            for i in range(0,len(splitUp)):
                try:
                    timeSN.append(float(splitUp[i].replace(' ','')))
                    time.append(timeSN[i])
                except:
                    print(splitUp[i])
            flag = 1
    else:
        print(splitUp)

sizeAr = len(timeAr)
sizeSN = len(timeSN)

print(str(sizeSN) + " " + str(sizeAr))



# Add Ar39 decays to designated array
eventAr = []
eventSN = []
events = []
for i in range(400):
    eventAr.append([])
    eventSN.append([])
    events.append([])

for i in range(0,sizeAr):
    if(timeAr[i] < 1000000):
        eventAr[int(timeAr[i]/2500)].append(timeAr[i])
        events[int(timeAr[i]/2500)].append(timeAr[i])
        
    else:
        eventAr[399].append(timeAr[i])
        events[399].append(timeAr[i])

# Add SN events to designated array
    

for i in range(0,sizeSN):
    if(timeSN[i] < 1000000):
        eventSN[int(timeSN[i]/2500)].append(timeSN[i])
        events[int(timeSN[i]/2500)].append(timeSN[i])
    else:
        eventSN[399].append(timeSN[i])
        events[399].append(timeSN[i])

plt.hist(events[0], bins = 5000)
plt.xlim(1240,1260)
plt.savefig("SNexample.png")

totalSize = sizeSN + sizeAr

for i in range(0,400):
    events[i].sort()
    

# Plan:
# Save data as histograms with varying binning
# Compute the ratio of the difference between each bin and the mean number of
# entries per bin and std of all bins. Compare this with a threshold. Save if above
# Define a cost function for events outside the middle region
def Candidates(events, nbins = 10000, threshold = 2.):
    candidates = []
    SNdet = np.zeros(400)
    fakeSig = 0
    frameEvents = np.zeros(400)
    for i in range(0,400):
        hist, bin_edges = np.histogram(events[i],nbins)
        
        # Initially the trigger is not active
        flagTrigger = 0
        
        binSize = np.mean(np.diff(bin_edges))
        mean = np.mean(hist)
        variance = np.std(hist)
        mean_edges = np.mean(bin_edges)
        for j in range(0,len(hist)):
            # Start every "step" by decreasing the time trigger is still active
            if(flagTrigger >0):
                    flagTrigger = flagTrigger - 1
            if( (hist[j]-mean)/variance > threshold ):
                frameEvents[i] = frameEvents[i] + 1
                # if event comes from SN and has not been flagged before as SN
                # no problem if event was flagged as noise
                if(abs(bin_edges[j]-mean_edges)<10. and SNdet[i] == 0):
                    candidates.append((hist[j],bin_edges[j],bin_edges[j+1],1))
                    SNdet[i] = 1
                # if event is not SN and no trigger was activated within 30 mus
                elif(flagTrigger == 0):
                    candidates.append((hist[j],bin_edges[j],bin_edges[j+1],0))
                    fakeSig = fakeSig + 1
                    # Flag all future events within the 30 mus trigger
                    # equivalent to 30/binSize number of bins
                    flagTrigger = int(30/binSize)
                    
    SNeff = float(np.count_nonzero(SNdet))/400.
    return candidates, SNeff, SNdet, fakeSig, frameEvents


[candidates, SNeff, SNdet, fakeSig, frameEvents] =  Candidates(events, nbins = 1000, threshold = 4.)
print("The efficiencies are " + str(SNeff) + "    " + str(fakeSig))

ROC = []
threshold = 2.0
while( threshold < 15.0):
    [_,SNeff,_, fakeSig, frameEvents] =  Candidates(events, nbins = 10000, threshold = threshold)
    # fake signals are divided by the largest number observed (threshold = 2.)
    ROC.append((SNeff, fakeSig/float(26142)))
    threshold += 0.1
    break

plt.plot(ROC)
plt.xlim(0,1)
plt.xlabel("Fake triggers")
plt.ylim(0,1)
plt.ylabel("True SN signal")
plt.title("ROC Curve for nbins = 10000")



"""
for i in range(0,len(candidates)):
    if(candidates[i][3]):
        # Print the position of the missidentified peak
        print(candidates[i][0])
        
"""



fig = plt.plot(frameEvents)
plt.title( 'Fake events vs frame' )
plt.xlabel("Time frame")
plt.ylabel("Number of events")
plt.savefig('FakeSig.png')

