# -*- coding: utf-8 -*-
#IMPORTS
print('STARTING')
import matplotlib
matplotlib.use('Agg')
from matplotlib.offsetbox import (TextArea, DrawingArea, OffsetImage, AnnotationBbox)
from matplotlib.cbook import get_sample_data
import matplotlib.image as mpimg 
import matplotlib.pyplot as plt 
from matplotlib.pyplot import cm
from matplotlib.pylab import rcParams
rcParams['figure.figsize'] = 48, 24
from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox
import pandas as pd
import numpy as np

# VARIABLES
brands = ['Heineken','Grolsch','Brand','Hertog Jan']
urls = {'Dirk':'/home/pi/beer_tracker/supermarkt logos/dirk.png', 'Albert Heijn':'/home/pi/beer_tracker/supermarkt logos/ah.png',
        'Jumbo':'/home/pi/beer_tracker/supermarkt logos/jumbo.png'}
zooms = {'Dirk':1,'Albert Heijn':0.4,'Jumbo':0.4}
box_positions = {'Heineken':(1000., -260.),'Grolsch':(1000,-530),'Brand':(1000., -800.),'Hertog Jan':(1000., -1070)}
text_positions = {'Heineken':(0.8, 0.79),'Grolsch':(0.8, 0.58),'Brand':(0.8, 0.38),'Hertog Jan':(0.8, 0.17)}


def prepare_df(brand):
    df=pd.read_csv('/home/pi/beer_tracker/logs/'+brand+'.txt',sep=';',index_col='Date')
    df.index=pd.to_datetime(df.index)
    for column in df.columns:
        df[column]=pd.to_numeric(df[column])
    return df

def determine_minima(brands):
    minima = {}
    for brand in brands:
        brand_df = prepare_df(brand)
        minima[brand] = (brand_df.iloc[-1].idxmin(),np.nanmin(brand_df.iloc[-1]))
    return minima

def plot_supermarket(ax,brand,supermarket):
    arr_img = plt.imread(urls[supermarket])
    imagebox = OffsetImage(arr_img, zoom=zooms[supermarket])
    imagebox.image.axes = ax
    ab = AnnotationBbox(imagebox,[0.3, 0.55],
                    xybox=box_positions[brand], 
                    xycoords='data',
                    boxcoords="offset points",frameon=False
                    )
    return ab

def create_plot():
    fig, ax = plt.subplots()
    print('DETERMINING MINIMA')
    minima = determine_minima(brands)
    print('PLOTTING IMAGE')
    for key in minima.keys():
        ab=plot_supermarket(ax,key,minima[key][0])
        ax.add_artist(ab)
        ax.text(text_positions[key][0], text_positions[key][1], '€'+str(minima[key][1]), horizontalalignment='center',verticalalignment='center', transform=ax.transAxes,fontsize=80)
    ax.text(0,0,'Date: '+pd.to_datetime("today").strftime("%Y/%m/%d"),horizontalalignment='center',verticalalignment='center',transform=ax.transAxes,fontsize=40)
    img = mpimg.imread('/home/pi/beer_tracker/background.jpg')
    plt.tick_params(axis='both', labelsize=0, length = 0)
    plt.box(False)
    plt.imshow(img)
    print('SAVING IMAGE')
    plt.savefig('/home/pi/beer_tracker/output.png', bbox_inches='tight')
    plt.savefig('/home/pi/dijkstrar.github.io/images/beer_output.png', bbox_inches='tight')

if __name__ == '__main__':
    create_plot()
    print('Done')
