#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 09:55:12 2018

@author: vladgriguta
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def PlotGridSearch(df_eff, efficiency = True):
    X, Y = np.meshgrid(list(map(float, df_eff.index)),list(map(float, df_eff.columns)))
    if(efficiency):
        plt.scatter(X, Y, c = np.transpose(df_eff.values), cmap='viridis', linewidth=0.5);
        cbar = plt.colorbar()
        cbar.set_label('Efficiency (%)', rotation = 270, labelpad=30, y=0.5, fontsize = 18)
        plt.title('SN Detection Efficiency')
        plt.xlabel('Threshold / per mean # events in interval')
        plt.ylabel('Interval of integration / microseconds')
        plt.savefig('EffFinal.jpg', format='jpg')
    else:
        Z = np.zeros(np.shape(df_eff))
        for i in range(np.shape(df_eff)[0]):
            for j in range(np.shape(df_eff)[1]):
                if(df_eff.values[i][j]):
                    Z[i][j] = np.log10(df_eff.values[i][j])
        Z = np.transpose(Z)
        plt.scatter(X, Y, c = Z, cmap='viridis', linewidth=0.5);
        cbar = plt.colorbar()
        cbar.set_label('Event Rate (log scale)', rotation = 270, labelpad=30, y=0.5, fontsize = 18)
        plt.xlabel('Threshold / per mean # events in interval')
        plt.ylabel('Interval of integration / microseconds')
        plt.title('Fake Events Rate')
        plt.savefig('FakeFinal.jpg', format='jpg')
    plt.show()

df_eff = pd.DataFrame()
df_eff = pd.read_csv('efficienciesNov.csv')

df_fake = pd.DataFrame()
df_fake = pd.read_csv('fakeEventsNov.csv')


#PlotGridSearch(df_eff,efficiency=True)
PlotGridSearch(df_fake,efficiency=False)


