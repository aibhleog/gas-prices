'''
This is code used to look at how the gas prices in Texas are changing
as a function of time. Underlaid, I have a moving average plotted, in
order to help guide the eye when comparing to the gasbuddy.com charts.

It's important to note that while these gas values are mostly coming
from the Bryan/College Station area, there are times when I purchased
gas on my drive to Austin or Dallas.
---> these locations are logged in "gasforcar" table

The original code for the moving average can be found here:
https://stackoverflow.com/questions/14313510/how-to-calculate-moving-average-using-numpy/54628145
'''

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable
#import matplotlib.colorbar as colorbar
import matplotlib.patheffects as PathEffects

__author__ = 'Taylor Hutchison'
__email__ = 'aibhleog@tamu.edu'

# reading in data
df = pd.read_csv('gasforcar')

# making figure
plt.figure(figsize=(13,6))
dates = [pd.to_datetime(d) for d in df.date] # converting to datetime object

# - moving average - #
def moving_average(a, n=3) :
    ret = np.nancumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

# using np.isfinite because of the one NaN ppgal value
running_med = moving_average(df['ppgal'][np.isfinite(df.ppgal.values)].values)
# ------------------ #

#im = plt.scatter(dates,df.ppgal,edgecolor='k',s=100,alpha=0.8)
im = plt.scatter(dates,df.ppgal,c=df.gallons,cmap=plt.cm.viridis,\
	edgecolor='k',s=100,alpha=0.8)
plt.gcf().autofmt_xdate()
plt.plot(dates[1:-2],running_med,ls=':',lw=2.5,label='moving average',zorder=0)

txt = plt.text(0.03,0.07,'Gas Prices in Texas',transform=plt.gca().transAxes,fontsize=17)
txt.set_path_effects([PathEffects.withStroke(linewidth=0.4, foreground='k')])

plt.xlabel('date of purchase',fontsize=15,labelpad=12)
plt.ylabel('price per gallon',fontsize=15,labelpad=10)
plt.gca().tick_params(labelsize=14)

ax = plt.gca()
ax_divider = make_axes_locatable(ax)
cax2 = ax_divider.append_axes('top',pad='2.5%',size='5%')
cbar = plt.colorbar(im,cax=cax2,orientation="horizontal")
cbar.ax.set_xlabel('gallons',labelpad=-54,fontsize=15)
cax2.xaxis.set_ticks_position('top')    
cbar.ax.tick_params(labelsize=14)

#plt.tight_layout()
plt.savefig('ppgal-time.png')
#plt.show()
plt.close('all')

print(f"Total gas purchased since {df.loc[0,'date']}: ${round(sum(df.price.values),2)}")




