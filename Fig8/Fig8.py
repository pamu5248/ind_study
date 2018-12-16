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

df = pd.read_pickle('Fig8.pickle')
def bin_windrose(wind_direction,wind_speed,direction_binwidth):
    wd_array = []
    list_of_binned_lists = []
    for wd in np.arange(0,np.nanmax(wind_direction),direction_binwidth):
        wd_array.append(wd)
        if wd == 355:
            wind_speed_by_direction = wind_speed[(wind_direction>=wd) & (wind_direction<=(wd+direction_binwidth))]
        else:
            wind_speed_by_direction = wind_speed[(wind_direction>=wd) & (wind_direction<(wd+direction_binwidth))]
        wind_speed_by_direction = np.array(wind_speed_by_direction)
        wind_speed_by_direction = wind_speed_by_direction[~np.isnan(wind_speed_by_direction)]
        wind_speed_by_direction = sorted(wind_speed_by_direction)
        list_of_binned_lists.append(wind_speed_by_direction)

    list_of_binned_lists = np.array(list_of_binned_lists)
    return wd_array, list_of_binned_lists

wd_bins, list_of_binned_lists = bin_windrose(df['lidar_wd_80'],df['d_sonic_ol_10m'],5)

mean_list = []
for lis in list_of_binned_lists:
    mean = np.nanmean(lis)
    mean_list.append(mean)
mean_list = np.array(mean_list)


plt.polar()
fig = plt.figure(figsize = (20,10))
ax1 = fig.add_subplot(131, projection='polar')
wd_bins_deg = wd_bins

#switch partly to met coordinates
neutral = 0.
neutral_list = []
for i in np.arange(0,2*np.pi,.01):
    neutral_list.append(neutral)
wd = -1*np.array(wd_bins)
wd = wd*(np.pi/180.)

ax1.scatter(wd[mean_list <0],np.abs(mean_list[mean_list <0]),alpha = 1,c = 'C1',s=30, label = 'convective')
ax1.scatter(wd[mean_list >0],np.abs(mean_list[mean_list >0]),alpha = 1,c = 'C0',s=30, label = 'stable')


ax1.fill_between(np.linspace(-80*np.pi/180.,-145*np.pi/180.,100),0,max_val,color = 'gray',alpha = .5,zorder=3)
ax1.fill_between(np.linspace(-245*np.pi/180.,-270*np.pi/180.,100),0,max_val,color = 'gray',alpha = .5,zorder=3)



ax1.grid(zorder = 10)
#finish switching to met coordinates
ax1.set_theta_zero_location("N")
ax1.set_xticklabels(['N', 'NW', 'W', 'SW', 'S', 'SE', 'E', 'NE'])
ax1.tick_params(axis='x', which='major', pad=35)
ax1.set_ylim(0,max_val)

leg = plt.legend(title = r'$\zeta$', prop={'size': 15},loc = 'lower right')
leg.set_title(r'$\zeta$', prop = {'size':20})
leg.get_frame().set_alpha(1)

ax1.tick_params(axis='x', which='both', labelsize = 10+20)
ax1.tick_params(axis='y', which='both', labelsize = 20)
ax1.tick_params(axis='x', which='major', pad=10)

ax1.set_rmax(.6)

####################################################################################
wd_bins, list_of_binned_lists = bin_windrose(df['lidar_wd_80'][df['d_sonic_ol_10m']<0],df['d_sonic_ol_10m'][df['d_sonic_ol_10m']<0],5)

mean_list = []
for lis in list_of_binned_lists:
    mean = np.nanmean(lis)
    mean_list.append(mean)
mean_list = np.array(mean_list)
    


ax2 = fig.add_subplot(132, projection='polar')
wd_bins_deg = wd_bins

#switch partly to met coordinates
neutral = 0.
neutral_list = []
for i in np.arange(0,2*np.pi,.01):
    neutral_list.append(neutral)
wd = -1*np.array(wd_bins)
wd = wd*(np.pi/180.)

ax2.scatter(wd,np.abs(mean_list),alpha = 1,c = 'C1',s=30, label = 'convective')


ax2.fill_between(np.linspace(-80*np.pi/180.,-145*np.pi/180.,100),0,max_val,color = 'gray',alpha = .5,zorder=3000)
ax2.fill_between(np.linspace(-245*np.pi/180.,-270*np.pi/180.,100),0,max_val,color = 'gray',alpha = .5,zorder=3000)

ax2.tick_params(axis='x', which='both', labelsize = 10+20)
ax2.tick_params(axis='y', which='both', labelsize = 20)

ax2.grid(zorder = 10)
#finish switching to met coordinates
ax2.set_theta_zero_location("N")
ax2.set_xticklabels(['N', 'NW', 'W', 'SW', 'S', 'SE', 'E', 'NE'])
ax2.tick_params(axis='x', which='major', pad=10)
ax2.set_ylim(0,max_val)

####################################################################################
wd_bins, list_of_binned_lists = bin_windrose(df['lidar_wd_80'][df['d_sonic_ol_10m']>0],df['d_sonic_ol_10m'][df['d_sonic_ol_10m']>0],5)

mean_list = []
for lis in list_of_binned_lists:
    mean = np.nanmean(lis)
    mean_list.append(mean)
mean_list = np.array(mean_list)
    


ax3 = fig.add_subplot(133, projection='polar')
wd_bins_deg = wd_bins

#switch partly to met coordinates
neutral = 0.
neutral_list = []
for i in np.arange(0,2*np.pi,.01):
    neutral_list.append(neutral)
wd = -1*np.array(wd_bins)
wd = wd*(np.pi/180.)

ax3.scatter(wd,mean_list,alpha = 1,c = 'C0',s=30, label = 'stable')


ax3.fill_between(np.linspace(-80*np.pi/180.,-145*np.pi/180.,100),0,max_val,color = 'gray',alpha = .5,zorder=3000)
ax3.fill_between(np.linspace(-245*np.pi/180.,-270*np.pi/180.,100),0,max_val,color = 'gray',alpha = .5,zorder=3000)

ax3.tick_params(axis='x', which='both', labelsize = 10+20)
ax3.tick_params(axis='y', which='both', labelsize = 20)

ax2.grid(zorder = 10)
#finish switching to met coordinates
ax3.set_theta_zero_location("N")
ax3.set_xticklabels(['N', 'NW', 'W', 'SW', 'S', 'SE', 'E', 'NE'])
ax3.tick_params(axis='x', which='major', pad=10)
ax3.set_ylim(0,max_val)


plt.subplots_adjust(wspace = .3)
