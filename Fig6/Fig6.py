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

df = pd.read_pickle('Fig6.pickle')
f, (ax1, ax2) = plt.subplots(1, 2, figsize = (17,8))
ax1.scatter(df['rews_subtract_nacelle_speed_nodir'],df['rews_subtract_nacelle_speed'],alpha = .003)
ax1.set_xlabel(r'REWS$_{NS}$',fontsize = 30)
ax1.set_ylabel(r'REWS$_{\theta,NS}$',fontsize = 30)
# ax1.set_xlim(-5,5)
ax1.locator_params(axis='x', nbins=3)
ax1.grid()
ax1.tick_params(axis='both', which='both', labelsize=30)

ax2.scatter(np.abs(df['d_veer_lidar_40_120']),df['d_total_DSPM_1'],alpha = .003)
ax2.set_xlabel(r'|$\beta_{bulk}$|',fontsize = 30)
ax2.set_ylabel(r'$\beta_{total}$',fontsize = 30)
ax2.set_xlim(-.1,1)
ax2.set_ylim(-.1,1)
ax2.locator_params(axis='x', nbins=3)

ax2.grid()
ax2.tick_params(axis='both', which='both', labelsize=30)

plt.subplots_adjust(wspace = .3)
plt.show()


