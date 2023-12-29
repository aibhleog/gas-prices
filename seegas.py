'''
This is code was originally used to look at how the gas prices in Texas 
were changing over time.  Now, I've updated it to show either Maryland
or Texas.  I'll continue adding states to this code as I progress in my 
career.  Underlaid, I have a moving average plotted, in order to help 
guide the eye when comparing to the gasbuddy.com charts.

It's important to note that while these gas values are mostly coming
from the areas I live in, there are times when I purchased
gas on my drive to Austin or Dallas (in TX) or to other big cities.
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
import matplotlib.dates as md

__author__ = 'Taylor Hutchison'
__email__ = 'aibhleog@tamu.edu'


# places this car has lived
maryland = { 'y1': 0.14, 'y2': 0.07, 'interval': 30, 'interval_format':'%Y-%m' }
texas = { 'y1': 0.885, 'y2': 0.8, 'interval': 120, 'interval_format':'%Y-%m' }
places = { 'TX': texas, 'MD': maryland }

# reading in data
state = 'MD'
st = places[state]
df = pd.read_csv(f'gasforcar-{state}.txt')


# calculating total gas
state_total = round(sum(df.price.values),2)


# making figure
plt.figure(figsize=(13,6))
ax = plt.gca()

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
# this try except only really matters when you have a small sample (aka just moved)
try: ax.plot(dates[1:-2],running_med,ls=':',lw=2.5,label='moving average',zorder=0)
except ValueError: ax.plot(dates[1:-1],running_med,ls=':',lw=2.5,label='moving average',zorder=0)

txt = ax.text(0.025,st['y1'],f'Gas Prices in {state}',transform=ax.transAxes,fontsize=17)
txt.set_path_effects([PathEffects.withStroke(linewidth=0.4, foreground='k')])
ax.text(0.026,st['y2'],f'Total: ${state_total}',transform=ax.transAxes,fontsize=13)

ax.set_xlabel('date of purchase',fontsize=15,labelpad=12)
ax.set_ylabel('price per gallon',fontsize=15,labelpad=10)
ax.tick_params(labelsize=14)

# setting up xaxis
interval = st['interval'] # days
ax.xaxis.set_major_formatter(md.DateFormatter(st['interval_format']))
ax.xaxis.set_major_locator(md.DayLocator(interval=interval)) # interval is in days
ax.minorticks_on()

# color bar!
ax_divider = make_axes_locatable(ax)
cax2 = ax_divider.append_axes('top',pad='2.5%',size='5%')
cbar = plt.colorbar(im,cax=cax2,orientation="horizontal")
cbar.ax.set_xlabel('gallons',labelpad=-54,fontsize=15)
cax2.xaxis.set_ticks_position('top')    
cbar.ax.tick_params(labelsize=14)

#plt.tight_layout()
plt.savefig(f'ppgal-time-{state}.png')
# plt.show()
plt.close('all')


# calculating all gas ever
keys = list(places.keys())
total = 0
for key in keys:
	filler_df = pd.read_csv(f'gasforcar-{key}.txt')
	total += sum(filler_df.price.values)
	if key == 'TX': first_date = filler_df.loc[0,'date']

print(f"Total gas purchased since {first_date}: ${round(total,2)}")
print(f"Total gas purchased in {state}: ${state_total}")











