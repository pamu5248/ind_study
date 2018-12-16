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

df = pd.read_pickle('Fig5.pickle')
fig = plt.figure( figsize = (17,10))
ax1 = fig.add_subplot(321)
n, bins, patches = plt.hist(df['rews_subtract_nacelle_speed_nodir'].dropna(),bins = 400)
ax1.bar(-100,0, color = 'C1',label = 'high')
ax1.bar(-100,0, color = 'C0',label = 'low')
lim = 0
ax1.axvline(lim,color = 'black',linewidth = 5)
for i,patch in enumerate(patches):
    if bins[i] <lim:
        plt.setp(patch, 'facecolor', 'C0')
    elif bins[i] > lim:
        plt.setp(patch, 'facecolor', 'C1')
ax1.legend(fontsize = 20,loc = 'upper right')
ax1.set_xlabel(r'REWS - nacelle speed (REWS$_{NS}$) (m s$^{-1}$)',fontsize = 20)
ax1.set_ylabel('Count',fontsize = 20)
ax1.tick_params(axis='both', which='both', labelsize=20)

ax1.set_xlim(-5,5)
ax1.tick_params(axis='both', which='both', labelsize=20)
ax1.locator_params(axis='y', nbins=4)
ax1.locator_params(axis='x', nbins=6)

###########################################################################

ax2 = fig.add_subplot(322)
n, bins, patches = plt.hist(df['rews_subtract_nacelle_speed'].dropna(),bins = 400)
ax2.bar(-100,0, color = 'C1',label = 'high')
ax2.bar(-100,0, color = 'C0',label = 'low')
lim = 0
ax2.axvline(lim,color = 'black',linewidth = 5)
for i,patch in enumerate(patches):
    if bins[i] <lim:
        plt.setp(patch, 'facecolor', 'C0')
    elif bins[i] > lim:
        plt.setp(patch, 'facecolor', 'C1')
ax2.legend(fontsize = 20,loc = 'upper right')
ax2.set_xlabel(r'REWS$_{\theta}$ - nacelle speed (REWS$_{\theta,NS}$) (m s$^{-1}$)',fontsize = 20)
#ax2.set_ylabel('Count',fontsize = 20)
ax2.tick_params(axis='both', which='both', labelsize=20)

ax2.set_xlim(-5,5)
ax2.tick_params(axis='both', which='both', labelsize=20)
ax2.locator_params(axis='y', nbins=4)
ax2.locator_params(axis='x', nbins=6)

###########################################################################
ax3 = fig.add_subplot(323)
n, bins, patches, = plt.hist(df['d_alpha_lidar'].dropna(),bins = 1000,color = 'lightgrey')
ax3.bar(-100,0, color = 'C0',label = 'high')
ax3.bar(-100,0, color = 'C1',label = 'low')
for i,patch in enumerate(patches):
    if bins[i] <.07:
        plt.setp(patch, 'facecolor', 'C1')
    elif bins[i] > .2:
        plt.setp(patch, 'facecolor', 'C0')

ax3.axvline(.07,color = 'black',linewidth = 2)
# plt.axvline(.09,color = 'black')
ax3.axvline(1/7,color = 'red',linewidth = 2,linestyle = '--',label = 'neutral')
ax3.axvline(.2,color = 'black',linewidth = 2)
ax3.legend(fontsize = 20,loc = 'upper right')
ax3.set_xlabel(r'$\alpha$',fontsize = 20)
ax3.set_ylabel('Count',fontsize = 20)
ax3.set_xlim(-.75,1)
ax3.tick_params(axis='both', which='both', labelsize=20)
ax3.locator_params(axis='y', nbins=4)
ax3.locator_params(axis='x', nbins=6)

###########################################################################
ax4 = fig.add_subplot(324)
n, bins, patches = plt.hist(df['d_veer_lidar_40_120'].dropna(),bins = 200)
ax4.bar(-100,0, color = 'C1',label = 'high')
ax4.bar(-100,0, color = 'C0',label = 'low')
ax4.axvline(lim,color = 'black',linewidth = 5)
lim = 0
for i,patch in enumerate(patches):
    if bins[i] <lim:
        plt.setp(patch, 'facecolor', 'C0')
    elif bins[i] > lim:
        plt.setp(patch, 'facecolor', 'C1')
ax4.legend(fontsize = 20,loc = 'upper right')
ax4.set_xlabel(r'$\beta_{bulk}$ (degrees m$^{-1}$)',fontsize = 20)
#ax4.set_ylabel('Count',fontsize = 20)
ax4.tick_params(axis='both', which='both', labelsize=20)

ax4.set_xlim(-.75,1)
ax4.tick_params(axis='both', which='both', labelsize=20)
ax4.locator_params(axis='y', nbins=4)
ax4.locator_params(axis='x', nbins=6)

###########################################################################
ax5 = fig.add_subplot(325)
n, bins, patches = plt.hist(np.abs(df['d_veer_lidar_40_120']).dropna(),bins = 200)
ax5.bar(-100,0, color = 'C1',label = 'high')
ax5.bar(-100,0, color = 'C0',label = 'low')
ax5.axvline(.1,color = 'black',linewidth = 5)
for i,patch in enumerate(patches):
    if bins[i] <.1:
        plt.setp(patch, 'facecolor', 'C0')
    elif bins[i] > .1:
        plt.setp(patch, 'facecolor', 'C1')
ax5.legend(fontsize = 20,loc = 'upper right')
ax5.set_xlabel(r'|$\beta_{bulk}$| (degrees m$^{-1}$)',fontsize = 20)
ax5.set_ylabel('Count',fontsize = 20)
ax5.tick_params(axis='both', which='both', labelsize=20)

ax5.set_xlim(-.1,1)
ax5.tick_params(axis='both', which='both', labelsize=20)
ax5.locator_params(axis='y', nbins=4)
ax5.locator_params(axis='x', nbins=6)

###########################################################################
ax6 = fig.add_subplot(326)
n, bins, patches = plt.hist(np.abs(df['d_total_DSPM_1']).dropna(),bins = 300)
ax6.bar(-100,0, color = 'C1',label = 'high')
ax6.bar(-100,0, color = 'C0',label = 'low')
ax6.axvline(.15,color = 'black',linewidth = 5)
for i,patch in enumerate(patches):
    if bins[i] <.15:
        plt.setp(patch, 'facecolor', 'C0')
    elif bins[i] > .15:
        plt.setp(patch, 'facecolor', 'C1')
ax6.legend(fontsize = 20,loc = 'upper right')
ax6.set_xlabel(r'$\beta_{total}$ (degrees m$^{-1}$)',fontsize = 20)
#ax6.set_ylabel('Count',fontsize = 20)
ax6.tick_params(axis='both', which='both', labelsize=20)

ax6.set_xlim(-.1,1)
ax6.tick_params(axis='both', which='both', labelsize=20)
ax6.locator_params(axis='y', nbins=4)
ax6.locator_params(axis='x', nbins=6)

plt.subplots_adjust(hspace = .6, wspace = .25)
