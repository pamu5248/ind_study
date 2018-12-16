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

df = pd.read_pickle('Fig7.pickle')
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

wd_bins, list_of_binned_lists = bin_windrose(df['lidar_wd_80'],df['d_alpha_lidar'],5)

mean_list = []
max_val = 0
for lis in list_of_binned_lists:
    mean = np.nanmean(lis)
    if mean > max_val:
        max_val = mean
    mean_list.append(mean)
mean_list = np.array(mean_list)
    

plt.polar()
fig = plt.figure(figsize = (20,20))
ax = fig.add_subplot(111, projection='polar')
wd_bins_deg = wd_bins

#switch partly to met coordinates
neutral = 1/7.
neutral_list = []
for i in np.arange(0,2*np.pi,.01):
    neutral_list.append(neutral)
wd = -1*np.array(wd_bins)
wd = wd*(np.pi/180.)


plt.plot(np.arange(0,2*np.pi,.01),neutral_list, color = 'black',zorder = 9,label = 'neutral')
plt.scatter(wd[mean_list < neutral],mean_list[mean_list < neutral],alpha = 1,c = 'C1',s=200, label = 'convective')
plt.scatter(wd[mean_list >= neutral],mean_list[mean_list >= neutral],alpha = 1,c = 'C0',s=200, label = 'stable')


plt.fill_between(np.linspace(-80*np.pi/180.,-145*np.pi/180.,100),0,max_val,color = 'gray',alpha = .5,zorder=3000)
plt.fill_between(np.linspace(-245*np.pi/180.,-270*np.pi/180.,100),0,max_val,color = 'gray',alpha = .5,zorder=3000)


plt.grid(zorder = 10)
#finish switching to met coordinates
ax.set_theta_zero_location("N")
ax.set_xticklabels(['N', 'NW', 'W', 'SW', 'S', 'SE', 'E', 'NE'])
ax.tick_params(axis='x', which='major', pad=35)
ax.set_ylim(0,max_val)

leg = plt.legend(title = r'$\alpha$',fontsize = 45)
leg.get_frame().set_alpha(1)
plt.setp(leg.get_title(),fontsize = 45)

plt.tick_params(axis='x', which='both', labelsize = 45+20)
plt.tick_params(axis='y', which='both', labelsize = 45)

print(plt.xticks())
hello = np.arange(0,2*np.pi,np.pi/4)
print(hello)
plt.tight_layout()

plt.show()
