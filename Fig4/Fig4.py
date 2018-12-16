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

%matplotlib inline  

from FieldCampaign import read_data_files as rd
from FieldCampaign import controlRef as cref
from FieldCampaign import hector_ref as hr
from FieldCampaign import database as fdb
from FieldCampaign import models as mod

df = pd.read_pickle('Fig4.pickle')
i = 856637
f, (ax1, ax2) = plt.subplots(1, 2, sharey=True, figsize = (15,15))
ax1.plot(np.array([df['lidar_ws_40'][i],df['lidar_ws_60'][i],df['lidar_ws_80'][i],df['lidar_ws_100'][i],df['lidar_ws_120'][i]]),np.array([40,60,80,100,120]),c = 'black')
ax1.axhline(120,color = 'red',linestyle = '--',linewidth = 2)
ax1.axhline(40,color = 'red',linestyle = '--',linewidth = 2)
ax1.set_ylabel('meters AGL',fontsize = 30)
ax1.set_xlabel('lidar wind speed (m s$^{-1}$)',fontsize = 30)

ax2.plot(np.array([df['lidar_wd_40'][i],df['lidar_wd_60'][i],df['lidar_wd_80'][i],df['lidar_wd_100'][i],df['lidar_wd_120'][i]]),np.array([40,60,80,100,120]),c = 'black')
ax2.axhline(120,color = 'red',linestyle = '--',linewidth = 2)
ax2.axhline(40,color = 'red',linestyle = '--',linewidth = 2)
ax2.set_xlabel('lidar wind direction (degrees)',fontsize = 30)


ax1.grid()
ax2.grid()
ax1.tick_params(axis='both', which='both', labelsize=30)
ax2.tick_params(axis='both', which='both', labelsize=30)

plt.show()
