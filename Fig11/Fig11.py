from matplotlib import cm
import sys
import os
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import imp
import scipy.stats
import pickle
import math

from wind_tools import geometry as geo
from wind_tools import plotting as wp


from FieldCampaign import read_data_files as rd
from FieldCampaign import controlRef as cref
from FieldCampaign import hector_ref as hr
from FieldCampaign import database as fdb
from FieldCampaign import models as mod

df = pd.read_pickle('Fig11.pickle')

def bin_by_metric(metric,which_windspeed,dataframe = df,bounds_1 = 0,bounds_2 = 0,maximum_ws_bin=False):
    def pat_confidence_interval(sample_mean,sample_std,number_samples,confidence,twotailed):
            confidence_percent = confidence/100.
            alpha = 1.-confidence_percent
            if twotailed == True:
                alpha = alpha/2.
            tc = scipy.stats.t.ppf(1-alpha, number_samples)
            low_bound = sample_mean-(tc*(sample_std/np.sqrt(number_samples-1)))
            up_bound = sample_mean+(tc*(sample_std/np.sqrt(number_samples-1)))
            error = up_bound-low_bound
            return low_bound,up_bound,error 

    total_binned_mean = []

    bin_1_mean = []
    bin_1_std = []
    error_1 = []

    bin_2_mean = []
    bin_2_std = []
    error_2 = []

    if maximum_ws_bin == False:
        ws_bins = np.arange(np.nanmin(dataframe[which_windspeed]),np.nanmax(dataframe[which_windspeed]),.5)
    else:
        ws_bins = np.arange(np.nanmin(dataframe[which_windspeed]),maximum_ws_bin+.5,.5)
    count = 0
    countmean = 0
    for ws in ws_bins:
        #total
        n_mean = len(dataframe['active_power_1'][(dataframe[which_windspeed] >= ws) & (dataframe[which_windspeed] < ws+.5)])
        ttl_mean = np.nanmean(dataframe['active_power_1'][(dataframe[which_windspeed] >= ws) & (dataframe[which_windspeed] < ws+.5)])
        total_binned_mean.append(ttl_mean)

        #one
        power_mean_1 = np.nanmean(dataframe['active_power_1'][(dataframe[which_windspeed] >= ws) & (dataframe[which_windspeed] < ws+.5) & (dataframe[metric] >= bounds_1)])
        bin_1_mean.append(power_mean_1)
        power_std_1 = np.nanstd(dataframe['active_power_1'][(dataframe[which_windspeed] >= ws) & (dataframe[which_windspeed] < ws+.5) & (dataframe[metric] >= bounds_1)])
        bin_1_std.append(power_std_1/2)
        n_1 = len(dataframe['active_power_1'][(dataframe[which_windspeed] >= ws) & (dataframe[which_windspeed] < ws+.5) & (dataframe[metric] >= bounds_1)])

        # to get nstar
        timeseries = dataframe['active_power_1'][(dataframe[which_windspeed] >= ws) & (dataframe[which_windspeed] < ws+.5) & (dataframe[metric] >= bounds_1)]
        lag = 1
        t1_m = timeseries[0:-1*lag] - power_mean_1
        t2_m = timeseries[lag:] - power_mean_1
        alpha = np.correlate(t1_m, t2_m)/(n_1-lag)/(power_std_1**2)
        Nstar = (1-alpha[0])/(1+alpha[0])*n_1
        if Nstar <0:
            Nstar = n_1

        u_1,l_1,error_1_temp = pat_confidence_interval(power_mean_1,power_std_1,Nstar,99,twotailed= True)
        error_1.append(error_1_temp)

        # two
        power_mean_2 = np.nanmean(dataframe['active_power_1'][(dataframe[which_windspeed] >= ws) & (dataframe[which_windspeed] < ws+.5) & (dataframe[metric] < bounds_2)])
        bin_2_mean.append(power_mean_2)
        power_std_2 = np.nanstd(dataframe['active_power_1'][(dataframe[which_windspeed] >= ws) & (dataframe[which_windspeed] < ws+.5) & (dataframe[metric] < bounds_2)])
        bin_2_std.append(power_std_2/2)
        n_2 = len(dataframe['active_power_1'][(dataframe[which_windspeed] >= ws) & (dataframe[which_windspeed] < ws+.5) & (dataframe[metric] < bounds_2)])

        # to get nstar
        timeseries = dataframe['active_power_1'][(dataframe[which_windspeed] >= ws) & (dataframe[which_windspeed] < ws+.5) & (dataframe[metric] < bounds_2)]
        lag = 1
        t1_m = timeseries[0:-1*lag] - power_mean_2
        t2_m = timeseries[lag:] - power_mean_2
        alpha = np.correlate(t1_m, t2_m)/(n_2-lag)/(power_std_2**2)
        Nstar = (1-alpha[0])/(1+alpha[0])*n_2
        if Nstar <0:
            Nstar = n_2

        u_2,l_2,error_2_temp = pat_confidence_interval(power_mean_2,power_std_2,n_2,99,twotailed= True)
        error_2.append(error_2_temp)

        count = count + n_1 + n_2
        countmean = countmean + n_mean
    
    return countmean, total_binned_mean, ws_bins, bin_1_mean, bin_1_std, error_1, bin_2_mean, bin_2_std, error_2



bounds_1 = .2
bounds_2 = 0.07
metric = 'd_alpha_lidar'
countmean, total_binned_mean, ws_bins, bin_1_mean, bin_1_std, error_1, bin_2_mean, bin_2_std, error_2 = bin_by_metric(metric,'wind_speed_1_1',df,bounds_1,bounds_2)

fig, (ax1, ax2) = plt.subplots(2 , 1, sharex=True, figsize = (17,10))

n1 = len(df['active_power_1'][df['d_alpha_lidar']>bounds_1])
n2 = len(df['active_power_1'][df['d_alpha_lidar']<bounds_2])

ax1.fill_between(ws_bins, bin_1_mean-1*np.array(error_1), bin_1_mean+1*np.array(error_1),alpha = .25, color = 'C0')
ax1.plot(ws_bins,bin_1_mean,label = r'high $\alpha$ ' + '\n' + 'data available: ' + str(np.round(100*n1/(useable_data),1)) + '%', color = 'C0')

ax1.fill_between(ws_bins, bin_2_mean-1*np.array(error_2), bin_2_mean+1*np.array(error_2),alpha = .25, color = 'C1')
ax1.plot(ws_bins,bin_2_mean,label = r'low $\alpha$ ' + '\n' + 'data available: ' + str(np.round(100*n2/(useable_data),1)) + '%', color = 'C1')

ax1.plot(ws_bins,total_binned_mean,linewidth = .75, linestyle = '--', color = 'green', label = 'mean')
ax1.axvline(14,color = 'red',linestyle = '--',linewidth = 2)

ax1.set_ylim(-50,1650)
ax1.grid()
ax1.set_ylabel('Power (kW)', fontsize = 20, labelpad = 15)
ax1.set_title('99% confidence intervals on two regimes of REWS on 1 Hz turbine power data', fontsize = 20, y = 1.03)
ax1.legend(fontsize = 20)
ax1.tick_params(axis='both', which='both', labelsize=20)


bin_1_mean = np.array(bin_1_mean)
bin_2_mean = np.array(bin_2_mean)
total_binned_mean = np.array(total_binned_mean)

ax2.axhline(0,color = 'black',linewidth = 2)

ax2.fill_between(ws_bins, bin_1_mean-1*np.array(error_1)-total_binned_mean, bin_1_mean+1*np.array(error_1)-total_binned_mean,alpha = .25, color = 'C0')
ax2.plot(ws_bins,bin_1_mean-total_binned_mean,color = 'C0')

ax2.fill_between(ws_bins, bin_2_mean-1*np.array(error_2)-total_binned_mean, bin_2_mean+1*np.array(error_2)-total_binned_mean,alpha = .25, color = 'C1')
ax2.plot(ws_bins,bin_2_mean-total_binned_mean,color = 'C1')

#plt.plot(ws_bins,total_binned_mean,linewidth = .75, linestyle = '--', color = 'green', label = 'total binned mean'+ '\n' + 'data available: ' + str(np.round(100*countmean/(useable_data),1)) + '%')

ax2.axvline(14,color = 'red',linestyle = '--',linewidth = 2)

# plt.ylim(-50,1650)
ax2.grid()
ax2.set_xlabel('Nacelle anemometer wind speed (m s$^{-1}$)', fontsize = 20, labelpad = 15)
ax2.set_ylabel('Difference from mean (kW)', fontsize = 20, labelpad = 15)
ax2.legend(fontsize = 20,loc = 'upper left')
ax2.set_ylim(-60,60)
ax2.tick_params(axis='both', which='both', labelsize=20)
