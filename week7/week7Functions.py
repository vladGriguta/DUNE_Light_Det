#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  4 16:30:27 2018

@author: vladgriguta
"""
import numpy as np







def KMeansClustering3( timeSN, columns, n_clusters = 5):
    from sklearn.cluster import KMeans
    import matplotlib.pyplot as plt
    
    X = np.array(timeSN[columns])
    kmeans = KMeans(n_clusters,random_state=0).fit(X)
    
    from mpl_toolkits.mplot3d import Axes3D
    fig = plt.figure()
    ax = Axes3D(fig)
    labels = kmeans.labels_
    ax.scatter(X[:,0],X[:,1],X[:,2],alpha=0.1,depthshade=False,
               c=labels.astype(np.float),edgecolor = 'k')
    
    ax.w_xaxis.set_ticklabels([])
    ax.w_yaxis.set_ticklabels([])
    ax.w_zaxis.set_ticklabels([])
    ax.set_xlabel(columns[0])
    ax.set_ylabel(columns[1])
    ax.set_zlabel(columns[2])
    ax.set_title('K-Means Clusters')
    #fig.show()
    
    print("Number of iternations: "+str(kmeans.n_iter_))
    
    return kmeans.labels_,kmeans.cluster_centers_
    
def InCaseIComeBackToDensity():
    # Try to plot the 3D density
    from scipy.stats import gaussian_kde
    
    X = np.array(timeSN[columns])
    
    xyz = np.stack([timeSN[columns]]).transpose()
    density = gaussian_kde(xyz)
    
    
    x = np.linspace(np.min(X[:,0]),np.max(X[:,0]),20)
    y = np.linspace(np.min(X[:,1]),np.max(X[:,2]),20)
    z = np.linspace(np.min(X[:,2]),np.max(X[:,2]),20)
    
    Z = density(xyz)
    
    fig = plt.figure()
    ax = plt.subplot(projection='3d')
    p = ax.scatter(x,y,z,c=Z,alpha=0.5)
    fig.colorbar(p)
    fig.show()
    
    
    fig = plt.figure()
    ax = plt.subplot(projection='3d')
    p = ax.scatter(X[:,0],X[:,1],X[:,2],c=Z,alpha=0.5)
    fig.colorbar(p)
    fig.show()