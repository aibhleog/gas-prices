import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable
from mpl_toolkits.axes_grid1.colorbar import colorbar
import matplotlib.patheffects as PathEffects

df = pd.read_csv('gasforcar')

plt.figure(figsize=(9,7))
dates = [pd.to_datetime(d) for d in df.date]

#im = plt.scatter(dates,df.ppgal,edgecolor='k',s=100,alpha=0.8)
im = plt.scatter(dates,df.ppgal,c=df.gallons,cmap=plt.cm.viridis,\
	edgecolor='k',s=100,alpha=0.8)
plt.gcf().autofmt_xdate()

txt = plt.text(0.04,0.07,'Gas Prices in Texas',transform=plt.gca().transAxes,fontsize=17)
txt.set_path_effects([PathEffects.withStroke(linewidth=0.4, foreground='k')])

plt.xlabel('date of purchase',fontsize=15,labelpad=12)
plt.ylabel('price per gallon',fontsize=15,labelpad=10)
plt.gca().tick_params(labelsize=14)

ax = plt.gca()
ax_divider = make_axes_locatable(ax)
cax2 = ax_divider.append_axes('top',pad='2.5%',size='5%')
cbar = colorbar(im,cax=cax2,orientation="horizontal")
cbar.ax.set_xlabel('gallons',labelpad=-54,fontsize=15)
cax2.xaxis.set_ticks_position('top')    
cbar.ax.tick_params(labelsize=14)

#plt.tight_layout()
plt.savefig('ppgal-time.png',dpi=200)
#plt.show()
plt.close('all')

print(f"Total gas purchased since {df.loc[0,'date']}: ${round(sum(df.price.values),2)}")
