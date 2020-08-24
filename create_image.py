#IMPORTS
from matplotlib.offsetbox import (TextArea, DrawingArea, OffsetImage, AnnotationBbox)
from matplotlib.cbook import get_sample_data
import matplotlib.image as mpimg 
import matplotlib.pyplot as plt 
from matplotlib.pyplot import cm
from matplotlib.pylab import rcParams
rcParams['figure.figsize'] = 48, 24
from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox
import pandas as pd

# VARIABLES
brands = ['Heineken','Grolsch','Brand','Hertog Jan']
urls = {'Dirk':'supermarkt logos/dirk.png', 'Albert Heijn':'supermarkt logos/ah.png','Jumbo':'supermarkt logos/jumbo.png'}
zooms = {'Dirk':1,'Albert Heijn':0.4,'Jumbo':0.4}
box_positions = {'Heineken':(1000., -260.),'Grolsch':(1000,-530),'Brand':(1000., -800.),'Hertog Jan':(1000., -1070)}
text_positions = {'Heineken':(0.8, 0.79),'Grolsch':(0.8, 0.58),'Brand':(0.8, 0.38),'Hertog Jan':(0.8, 0.17)}


def determine_minima(brands):
    minima = {}
    for brand in brands:
        df=pd.read_csv('logs/'+brand+'.txt',sep=';',index_col='Date')
        df.index=pd.to_datetime(df.index)
        minima[brand] = (df.iloc[-1].idxmin(),min(df.iloc[-1]))
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
    minima = determine_minima(brands)
    for key in minima.keys():
        ab=plot_supermarket(ax,key,minima[key][0])
        ax.add_artist(ab)
        ax.text(text_positions[key][0], text_positions[key][1], '€'+str(minima[key][1]), horizontalalignment='center',verticalalignment='center', transform=ax.transAxes,fontsize=80)

    img = mpimg.imread('background.jpg')
    plt.tick_params(axis='both', labelsize=0, length = 0)
    plt.box(False)
    plt.imshow(img)
    plt.savefig('output.png', bbox_inches='tight')

if __name__ == '__main__':
    create_plot()