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
df = pd.read_pickle('Fig2.pickle')

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

plt.polar()
fig = plt.figure(figsize = (25,7.5))
#########################################################################################
ax1 = fig.add_subplot(131, projection='polar')
wind_direction = df['lidar_wd_80']
wind_speed = df['lidar_ws_80']
direction_binwidth = 5
speed_binwidth = 5
which_map = 'viridis'
edgecolor = True
hide_ticklabels = False
textsize = 45


wd_bins, list_of_binned_lists = bin_windrose(wind_direction,wind_speed,direction_binwidth)
hist_list = []
bin_list = []

# numpy is not good at histograms for some reason from my end
# so instead I plot each wind direction bin
fig2 = plt.figure(figsize = (20,10))
ax12 = fig2.add_subplot(131, projection='polar')
for i,wd in enumerate(wd_bins):
    n, bins, patches = ax12.hist(list_of_binned_lists[i],bins=np.arange(0,np.nanmax(wind_speed),speed_binwidth))
    hist_list.append(n)
    bin_list.append(bins)
plt.close()

total = 0
for i in hist_list:
    for y in i:
        total = total+y
total = total/100

wd_bins_deg = wd_bins

#switch partly to met coordinates
wd_bins = -1*np.array(wd_bins)
wd_bins = wd_bins*(np.pi/180.)


# plot as bar plots where each bar is sum of occurrences that happened
count = 0
max_val = 0
testtotal = 0
for i,wd in enumerate(wd_bins):
    sum_of_occurrences_list = []
    for y,val in enumerate(hist_list[i]):
        y=y+1
        sum_of_occurrences = np.sum(hist_list[i][:y])
        sum_of_occurrences_list.append(sum_of_occurrences)
    colorlist = []
    for z,summation in enumerate(sum_of_occurrences_list[::-1]): 
        cmap = cm.get_cmap(which_map,len(np.linspace(.1,1,len(sum_of_occurrences_list))))
        which_color_index = np.arange(len(sum_of_occurrences_list))
        which_color_index = which_color_index[::-1]
        colorlist.append(cmap(z))

        bar = ax1.bar(wd,summation/total,width = .0175*direction_binwidth,alpha = 1,color = cmap(which_color_index[z]),align = 'edge',zorder = count)
        count = count + 1
        if summation/total > max_val:
            max_val = summation/total
        if edgecolor == True:
            for test in bar:
                test.set_edgecolor("black")
                test.set_linewidth(.5)
        if z <=0:
            testtotal = testtotal + float(summation/total)
ax1.fill_between(np.linspace(-80*np.pi/180.,-145*np.pi/180.,100),0,6.5,color = 'gray',alpha = .5,zorder=3000)
ax1.fill_between(np.linspace(-245*np.pi/180.,-270*np.pi/180.,100),0,6.5,color = 'gray',alpha = .5,zorder=3000)

#finish switching to met coordinates
ax1.set_theta_zero_location("N")
ax1.set_xticklabels(['N', 'NW', 'W', 'SW', 'S', 'SE', 'E', 'NE'])
ax1.tick_params(axis='x', which='major', pad=10)
ax1.set_ylim(0,max_val)

if hide_ticklabels == True:
    ax.set_yticklabels([])


#make a legend that's basically discrete colorbar
from matplotlib.patches import Patch
custom_patches = []
custom_labels = []
for i in colorlist:
    print(i)
    custom_patches.append(Patch(facecolor = i))
for i in range(len(bins)-1):
    custom_labels.append(str(bins[i]) + ' - ' + str(bins[i+1]))
leg = ax1.legend(custom_patches, custom_labels,title = 'wind speed m s$^{-1}$',fontsize = 15)
leg.set_title('wind speed m s$^{-1}$', prop = {'size':15})
leg.get_frame().set_alpha(1)



ax1.tick_params(axis='x', which='both', labelsize = 10+20)
ax1.tick_params(axis='y', which='both', labelsize = 20)


ax1.set_rgrids([6,4,2], angle=90)
ax1.set_yticklabels(['6%','4%','2%'])



#########################################################################################
ax2 = fig.add_subplot(133, projection='polar')
wind_direction = df['lidar_wd_80'][df['d_sonic_ol_10m']<0]
wind_speed = df['lidar_ws_80'][df['d_sonic_ol_10m']<0]
direction_binwidth = 5
speed_binwidth = 5
which_map = 'viridis'
edgecolor = True
hide_ticklabels = False
textsize = 45


wd_bins, list_of_binned_lists = bin_windrose(wind_direction,wind_speed,direction_binwidth)
hist_list = []
bin_list = []

# numpy is not good at histograms for some reason from my end
# so instead I plot each wind direction bin
fig2 = plt.figure(figsize = (20,10))
ax12 = fig2.add_subplot(131, projection='polar')
for i,wd in enumerate(wd_bins):
    n, bins, patches = ax12.hist(list_of_binned_lists[i],bins=np.arange(0,np.nanmax(wind_speed),speed_binwidth))
    hist_list.append(n)
    bin_list.append(bins)
plt.close()

total = 0
for i in hist_list:
    for y in i:
        total = total+y
total = total/100

wd_bins_deg = wd_bins

#switch partly to met coordinates
wd_bins = -1*np.array(wd_bins)
wd_bins = wd_bins*(np.pi/180.)


# plot as bar plots where each bar is sum of occurrences that happened
count = 0
#max_val = 0
testtotal = 0
for i,wd in enumerate(wd_bins):
    sum_of_occurrences_list = []
    for y,val in enumerate(hist_list[i]):
        y=y+1
        sum_of_occurrences = np.sum(hist_list[i][:y])
        sum_of_occurrences_list.append(sum_of_occurrences)
    colorlist = []
    for z,summation in enumerate(sum_of_occurrences_list[::-1]): 
        cmap = cm.get_cmap(which_map,len(np.linspace(.1,1,len(sum_of_occurrences_list))))
        which_color_index = np.arange(len(sum_of_occurrences_list))
        which_color_index = which_color_index[::-1]
        colorlist.append(cmap(z))

        bar = ax2.bar(wd,summation/total,width = .0175*direction_binwidth,alpha = 1,color = cmap(which_color_index[z]),align = 'edge',zorder = count)
        count = count + 1
#         if summation/total > max_val:
#             max_val = summation/total
        if edgecolor == True:
            for test in bar:
                test.set_edgecolor("black")
                test.set_linewidth(.5)
        if z <=0:
            testtotal = testtotal + float(summation/total)
ax2.fill_between(np.linspace(-80*np.pi/180.,-145*np.pi/180.,100),0,6.5,color = 'gray',alpha = .5,zorder=3000)
ax2.fill_between(np.linspace(-245*np.pi/180.,-270*np.pi/180.,100),0,6.5,color = 'gray',alpha = .5,zorder=3000)

#finish switching to met coordinates
ax2.set_theta_zero_location("N")
ax2.set_xticklabels(['N', 'NW', 'W', 'SW', 'S', 'SE', 'E', 'NE'])
ax2.tick_params(axis='x', which='major', pad=10)
ax2.set_ylim(0,max_val)

if hide_ticklabels == True:
    ax3.set_yticklabels([])



ax2.tick_params(axis='x', which='both', labelsize = 10+20)
ax2.tick_params(axis='y', which='both', labelsize = 20)


ax2.set_rgrids([6,4,2], angle=90)
ax2.set_yticklabels(['6%','4%','2%'])

#########################################################################################
ax3 = fig.add_subplot(132, projection='polar')
wind_direction = df['lidar_wd_80'][df['d_sonic_ol_10m']>0]
wind_speed = df['lidar_ws_80'][df['d_sonic_ol_10m']>0]
direction_binwidth = 5
speed_binwidth = 5
which_map = 'viridis'
edgecolor = True
hide_ticklabels = False
textsize = 45


wd_bins, list_of_binned_lists = bin_windrose(wind_direction,wind_speed,direction_binwidth)
hist_list = []
bin_list = []

# numpy is not good at histograms for some reason from my end
# so instead I plot each wind direction bin
fig2 = plt.figure(figsize = (20,10))
ax12 = fig2.add_subplot(131, projection='polar')
for i,wd in enumerate(wd_bins):
    n, bins, patches = ax12.hist(list_of_binned_lists[i],bins=np.arange(0,np.nanmax(wind_speed),speed_binwidth))
    hist_list.append(n)
    bin_list.append(bins)
plt.close()

total = 0
for i in hist_list:
    for y in i:
        total = total+y
total = total/100

wd_bins_deg = wd_bins

#switch partly to met coordinates
wd_bins = -1*np.array(wd_bins)
wd_bins = wd_bins*(np.pi/180.)


# plot as bar plots where each bar is sum of occurrences that happened
count = 0
#max_val = 0
testtotal = 0
for i,wd in enumerate(wd_bins):
    sum_of_occurrences_list = []
    for y,val in enumerate(hist_list[i]):
        y=y+1
        sum_of_occurrences = np.sum(hist_list[i][:y])
        sum_of_occurrences_list.append(sum_of_occurrences)
    colorlist = []
    for z,summation in enumerate(sum_of_occurrences_list[::-1]): 
        cmap = cm.get_cmap(which_map,len(np.linspace(.1,1,len(sum_of_occurrences_list))))
        which_color_index = np.arange(len(sum_of_occurrences_list))
        which_color_index = which_color_index[::-1]
        colorlist.append(cmap(z))

        bar = ax3.bar(wd,summation/total,width = .0175*direction_binwidth,alpha = 1,color = cmap(which_color_index[z]),align = 'edge',zorder = count)
        count = count + 1
#         if summation/total > max_val:
#             max_val = summation/total
        if edgecolor == True:
            for test in bar:
                test.set_edgecolor("black")
                test.set_linewidth(.5)
        if z <=0:
            testtotal = testtotal + float(summation/total)
ax3.fill_between(np.linspace(-80*np.pi/180.,-145*np.pi/180.,100),0,6.5,color = 'gray',alpha = .5,zorder=3000)
ax3.fill_between(np.linspace(-245*np.pi/180.,-270*np.pi/180.,100),0,6.5,color = 'gray',alpha = .5,zorder=3000)

#finish switching to met coordinates
ax3.set_theta_zero_location("N")
ax3.set_xticklabels(['N', 'NW', 'W', 'SW', 'S', 'SE', 'E', 'NE'])
ax3.tick_params(axis='x', which='major', pad=10)
ax3.set_ylim(0,max_val)

if hide_ticklabels == True:
    ax3.set_yticklabels([])




ax3.tick_params(axis='x', which='both', labelsize = 10+20)
ax3.tick_params(axis='y', which='both', labelsize = 20)



ax3.set_rgrids([6,4,2], angle=90)
ax3.set_yticklabels(['6%','4%','2%'])




plt.subplots_adjust(wspace = .3)




