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

df = pd.read_pickle('Fig9.pickle')
f, (ax1, ax2, ax3) = plt.subplots(1, 3, sharey=True, figsize = (17,8))
ax1.scatter(df['rews_subtract_nacelle_speed_nodir'][(df['d_sonic_ol_10m']<1000) & (df['d_sonic_ol_10m']>-1000)],df['d_sonic_ol_10m'][(df['d_sonic_ol_10m']<1000) & (df['d_sonic_ol_10m']>-1000)],alpha = .003)
ax1.set_ylabel(r'$\zeta$',fontsize = 30)
ax1.set_xlabel('REWS$_{NS}$',fontsize = 30)
ax1.set_xlim(-5,5)
ax1.locator_params(axis='x', nbins=3)
ax1.set_xticks([-5,0,5])
ax1.set_xticklabels([-5,0,5])

ax2.scatter(df['d_alpha_lidar'][(df['d_sonic_ol_10m']<1000) & (df['d_sonic_ol_10m']>-1000)],df['d_sonic_ol_10m'][(df['d_sonic_ol_10m']<1000) & (df['d_sonic_ol_10m']>-1000)],alpha = .003)
ax2.set_xlabel(r'$\alpha$',fontsize = 30)
ax2.set_xlim(-.75,1)
#ax2.locator_params(axis='x', nbins=3)
ax2.set_xticks([-.75,0,1])
ax2.set_xticklabels([-.75,0,1])
# ax2.set_yticklabels(['6%','4%','2%'])

# ax3.scatter(df['d_veer_lidar_40_120'][(df['d_sonic_ol_10m']<1000) & (df['d_sonic_ol_10m']>-1000)],df['d_sonic_ol_10m'][(df['d_sonic_ol_10m']<1000) & (df['d_sonic_ol_10m']>-1000)],alpha = .003)
# ax3.set_xlabel(r'$\beta_{bulk}$',fontsize = 30)
# ax3.set_xlim(-.75,1)
# ax3.locator_params(axis='x', nbins=3)

ax3.scatter(np.abs(df['d_veer_lidar_40_120'])[(df['d_sonic_ol_10m']<1000) & (df['d_sonic_ol_10m']>-1000)],df['d_sonic_ol_10m'][(df['d_sonic_ol_10m']<1000) & (df['d_sonic_ol_10m']>-1000)],alpha = .003)
ax3.set_xlabel(r'|$\beta_{bulk}$|',fontsize = 30)
ax3.set_xlim(-.1,1)
ax3.locator_params(axis='x', nbins=4)
ax3.set_xticks([0,.5,1])
ax3.set_xticklabels([0,.5,1])


ax1.grid()
ax2.grid()
ax3.grid()
# ax4.grid()
ax1.tick_params(axis='both', which='both', labelsize=30)
ax2.tick_params(axis='both', which='both', labelsize=30)
ax3.tick_params(axis='both', which='both', labelsize=30)
# ax4.tick_params(axis='both', which='both', labelsize=30)

plt.subplots_adjust(wspace = .3)
plt.ylim(-200,200)
plt.show()

