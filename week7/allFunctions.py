# Here are the functions to be used in our analysis
import matplotlib.pyplot as plt
import numpy as np;
import pandas as pd;

def DivideDataByRes(resolution,time,simulationTime):
    events = np.zeros(int(simulationTime/resolution))
    for i in range(0,len(time)):
        events[int(time[i]/resolution)] += 1
    return events

def Candidates(events, SN_event_nr_bins, threshold, SN_event_time, eventsSN, trigDuration,resolution):
    # Plan:
    # For a given resolution, go through each time frame
    # In each resolving step compute the total number of entries in the last dt ns
    # compare this to some threshold, chosen by hand, in terms of the std of time
    # flag if above threshold
    # if within a reasonable time from the actual SN event successful
    # otherwise insuccessful
    # analyse the cases when insuccessful
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

def GridSearch(events, thresholdVals, SN_event_timeVals, eventsSN, trigDuration,resolution):
    # Function that searches through a grid of threshold and SN_event_time vals
    # and returs a Dataframe object with the appropriate values of SN detection
    # efficiency and fake trigger rate
    
    index = list(map(str, thresholdVals))
    columns = list(map(str, SN_event_timeVals))
    df_eff = pd.DataFrame(index = index,columns = columns)
    df_fake = pd.DataFrame(index = index,columns = columns)
    
    # Needed to compute the trigger
    mean_events = np.mean(events)

    progress = 0    
    for i in range(0,len(thresholdVals)):
        for j in range(0,len(SN_event_timeVals)):
            if(((i+1)*(j+1)) % int((len(thresholdVals)+1)*(len(SN_event_timeVals)+1)/10) == 0):
                progress += 10
                print(str(progress) + ' % Completed!!!!!!!!!!!!!!!!!!!!!!!!!!\n')
            SN_event_time = SN_event_timeVals[j]
            
            # Trigger depends on the accepted duration of the SN event
            SN_event_nr_bins = int(SN_event_time/resolution)
            threshold = thresholdVals[i] * float(mean_events*SN_event_nr_bins)
            
            [SNCandidates, fakeTrig, _] = Candidates(events, SN_event_nr_bins, threshold, SN_event_time, eventsSN,trigDuration,resolution)
            df_eff[str(SN_event_timeVals[j])][str(thresholdVals[i])] = (100 * np.sum(SNCandidates>0)/len(SNCandidates))
            df_fake[str(SN_event_timeVals[j])][str(thresholdVals[i])] = (len(fakeTrig) / 2.5)

    return df_eff, df_fake
    

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
    
    
def PlotGridSearch(df_eff, efficiency = True):
    X, Y = np.meshgrid(list(map(float, df_eff.index)),list(map(float, df_eff.columns)))
    plt.scatter(X, Y, c = np.transpose(df_eff.values), cmap='viridis', linewidth=0.5);
    plt.colorbar()
    plt.xlabel('Threshold / per mean # events in interval')
    plt.ylabel('Interval of integration / microseconds')
    if(efficiency):
        plt.title('SN Detection Efficiency')
        plt.savefig('week5/GridSearchEffPreliminary2.pdf', format='pdf')
    else:
        plt.title('Fake Events Rate')
        plt.savefig('week5/GridSearchFakePreliminary2.pdf', format='pdf')
    plt.show()

    
def SVMClass(eventsSN):
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