#source activate pythontest
from osgeo import gdal
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import cmocean

#data from USGS NED 1/3 arc-second n41w104 1 x 1 degree ArcGrid 2015 from https://apps.nationalmap.gov/download/#productSearch

geo = gdal.Open('USGS_NED_13_n41w104_IMG.img')
#upper left corner is N 41 W 104
arr = geo.ReadAsArray()

#for some reason the array is upside down
arr = arr[::-1,::]
print(type(arr))
print np.shape(arr)
print(arr[:,0])
print np.shape(arr[:,0])

x = []
how_far_over = 0
for i in range(len(arr[:,0])):
    i = float(i)
    x.append(-104+ float(i/float(len(arr[:,0]))))

y = []
how_far_over = 0
for i in range(len(arr[0,:])):
    i = float(i)
    y.append(40 + float(i/float(len(arr[0,:]))))


fig,ax = plt.subplots(figsize = (14,14))

xindlow = 5000
xindhigh = 5300
yindlow = 10550
yindhigh = 10812
minelev = np.nanmin(arr[yindlow:yindhigh,xindlow:xindhigh])
maxelev = np.nanmax(arr[yindlow:yindhigh,xindlow:xindhigh])
print(minelev)
print(maxelev)
maxelev=maxelev+3
heights = np.arange(minelev,maxelev,3)

maxelev = np.nanmax(heights)
print(maxelev)
print(heights)
print(len(heights))
heights = heights-maxelev
print(heights)
print(len(heights))
arr[yindlow:yindhigh,xindlow:xindhigh] = arr[yindlow:yindhigh,xindlow:xindhigh]-maxelev
contour = plt.contourf(x[xindlow:xindhigh],y[yindlow:yindhigh],arr[yindlow:yindhigh,xindlow:xindhigh],cmap = cmocean.cm.speed_r,levels = heights)

#plt.scatter(-103.52527778,40.99429167, color = 'black', zorder = 10, marker = 's', s = 300,label = 'met tower')
plt.scatter(-103.525206,40.994292, color = 'black', zorder = 10, marker = '^', s = 300,label = 'lidar')
plt.scatter(-103.529197,40.993425, color = 'red', zorder = 10, marker = 'o', s = 300,label = 'turbine 1')
plt.scatter(-103.523658,40.993358, color = 'black', zorder = 10, marker = 'o', s = 300,label = 'turbine 2')
plt.scatter(-103.520986,40.990506, color = 'black', zorder = 10, marker = 'o', s = 300,label = 'turbine 3')
plt.scatter(-103.519111,40.989092, color = 'black', zorder = 10, marker = 'o', s = 300,label = 'turbine 4')
plt.scatter(-103.517686,40.992289, color = 'black', zorder = 10, marker = 'o', s = 300,label = 'turbine 5')


plt.plot([-103.529398,-103.517661],[40.998054,40.998054],color = 'black', linewidth = 5, zorder = 10, label = '1 km')
plt.annotate('1 kilometer',(-103.5265,40.99838),fontsize = 30)
plt.arrow(-103.515061,40.998054-.0005,0,.0005,head_length = .0005,width =.0001,head_width = .0005,color = 'black')
plt.annotate('N',(-103.514561,40.998054-.0004),fontsize = 30)

cbar = plt.colorbar(contour,fraction=0.04, pad=0.04)


labels = []
for i in cbar.ax.get_yticklabels():
    a = i.get_text()
    labels.append(a)
for i in range(len(labels)):
    if labels[i][0]== u'\u2212':
        labels[i] = -int(labels[i][1:])
        labels[i] = ' ' + str(int(labels[i])) + ' m'
    else:
        labels[i] = '  ' + str(int(labels[i])) + ' m'
    
    
cbar.ax.set_yticklabels(labels)
cbar.ax.tick_params(labelsize=30)





plt.gca().set_aspect('equal', adjustable='box')
ax.tick_params(axis = 'both', which = 'major', labelsize = 10)
from matplotlib.ticker import FormatStrFormatter
ax.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
ax.xaxis.set_ticks([])
ax.yaxis.set_ticks([])
plt.show()
