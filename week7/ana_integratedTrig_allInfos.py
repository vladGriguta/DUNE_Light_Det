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


# Try a K-means clustering
import week7Functions
columns = ['pmt','y','z']
week7Functions.KMeansClustering3(timeSN,columns,n_clusters=2)

# Try to plot the 3D density
from scipy.stats import gaussian_kde

X = np.array(timeSN[columns])

xyz = np.array(timeSN[columns]).transpose()
density = gaussian_kde(xyz)


x = np.linspace(np.min(X[:,0]),np.max(X[:,0]),20)
y = np.linspace(np.min(X[:,1]),np.max(X[:,2]),20)
z = np.linspace(np.min(X[:,2]),np.max(X[:,2]),20)



xyz = np.meshgrid(x,y,z)
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
