import pandas as pd 
import time
import matplotlib.pyplot as plt
import plotly
import plotly.graph_objects as go
import plotly.express as px
import subprocess
import sys

brands = ['Heineken','Grolsch','Brand','Hertog Jan']
colors_supermarket={'Dirk':	'#dd0000','Jumbo':'#ffcc00','Albert Heijn':'#00a1e5'}
colors_beer = {'Heineken':'#26814c','Grolsch':'#38901f','Brand':'#1b3c33','Hertog Jan':'#debc50'}

def get_dataframe_supermarket(supermarket):
    result = pd.DataFrame()
    for brand in ['Heineken','Grolsch','Brand','Hertog Jan']:
        result[brand]=pd.read_csv('logs/'+brand+'.txt',sep=';',index_col='Date')[supermarket]
    return result

def get_dataframe_brand():
    supermarkets = ['Dirk','Jumbo','Albert Heijn']
    result = []
    for supermarket in supermarkets:
        result.append(pd.concat([get_dataframe_supermarket(supermarket)], keys=[supermarket], names=['Supermarket']))
    result=pd.concat(result)
    return result

def get_supermarket_graph(df):
    fig = go.Figure()
    for supermarket in list(df.index.get_level_values(0).unique()):
        df_sup = df.xs(supermarket)
        for column in df_sup.columns.to_list():
            fig.add_trace(
                go.Scatter(
                    x = df_sup.index,
                    y = df_sup[column],
                    name = column,
                    line=dict(color=colors_beer[column]),
                    visible=False
                )
            )
    fig.update_layout(template="simple_white")
    fig.update_layout(
        updatemenus=[go.layout.Updatemenu(
            active=0,
            direction='down',
            buttons=list(
                [dict(label = 'Select Supermarket',
                      method = 'update',
                      args = [{'visible': [False]*12}, # the index of True aligns with the indices of plot traces
                              {'title': 'Please Select a Supermarket',
                               'showlegend':False}])
                 ,dict(label = 'Dirk',
                      method = 'update',
                      args = [{'visible': [True]*4+[False]*8}, # the index of True aligns with the indices of plot traces
                              {'title': 'Dirk Beer Prices',
                               'showlegend':True}]),
                 dict(label = 'Jumbo',
                      method = 'update',
                      args = [{'visible': [False]*4+[True]*4+[False]*4},
                              {'title': 'Jumbo Beer Prices',
                               'showlegend':True}]),
                 dict(label = 'Albert Heijn',
                      method = 'update',
                      args = [{'visible': [False]*8+[True]*4},
                              {'title': 'Albert Heijn Beer Prices',
                               'showlegend':True}]),
                ])
            )
        ])

    string = plotly.io.to_html(fig,full_html=False,include_plotlyjs=False)
    string=string.replace("\n", "")
    return string

def get_beer_graphs(df):
    fig = go.Figure()
    for supermarket in list(df.index.get_level_values(0).unique()):
        df_sup = df.xs(supermarket)
        for column in df_sup.columns.to_list():
            fig.add_trace(
                go.Scatter(
                    x = df_sup.index,
                    y = df_sup[column],
                    name = supermarket,
                    line=dict(color=colors_supermarket[supermarket]),
                    visible=False
                )
            )

    fig.update_layout(template="simple_white")
    fig.update_layout(
        updatemenus=[go.layout.Updatemenu(
            active=0,
            direction='down',
            buttons=list(
                [dict(label = 'Select Label',
                      method = 'update',
                      args = [{'visible': [False]*12}, # the index of True aligns with the indices of plot traces
                              {'title': 'Please Select a Beer Brand',
                               'showlegend':False}])
                 ,dict(label = 'Heineken',
                      method = 'update',
                      args = [{'visible': [True,False,False,False]*3}, # the index of True aligns with the indices of plot traces
                              {'title': 'Heineken',
                               'showlegend':True}]),
                 dict(label = 'Grolsch',
                      method = 'update',
                      args = [{'visible': [False,True,False,False]*3},
                              {'title': 'Grolsch',
                               'showlegend':True}]),
                 dict(label = 'Brand',
                      method = 'update',
                      args = [{'visible': [False,False,True,False]*3},
                              {'title': 'Brand',
                               'showlegend':True}]),
                 dict(label = 'Hertog Jan',
                      method = 'update',
                      args = [{'visible': [False,False,False,True]*3},
                              {'title': 'Hertog Jan',
                               'showlegend':True}]),
                ])
            )
        ])        

    string = plotly.io.to_html(fig,full_html=False,include_plotlyjs=False)
    string=string.replace("\n", "")
    return string

def write_markup():
    ############################ CHANGE PATHS #######################
    path = '/home/pi/dijkstrar.github.io/_portfolio/beerprices.md'
    title_md = "--- \ntitle: \'Beerprice Tracker\' \ndate: 2020-08-25 \npermalink: /portfolio/2020/08/beerprices/ \n---\n\n"
    update_date_md = "History of beer prices and an overview on where to get the cheapest beer. Updated at: "+str(pd.to_datetime("today").strftime("%Y/%m/%d %H:%M")+"\n\n")
    body_md = '''This is a dynamically updating web page.\n
# Beer Tracker
This is a brief overview on the tool that scrapes beer crate prices daily.
Beer prices are collected from Albert Heijn, Dirk and Jumbo

## Methodology
For the scraping Selenium, together with Beautifulsoup is used. A choice was made for Selenium as the Jumbo website blocks access via the request package.
In order to overcome non-overlapping discounting periods, daily beer prices are scraped. Furthermore, due to different lay-outs and html contents, custom made functions had to be designed to overcome these issues. 
An example of such an problematic aspect, is the fact that Albert Heijn lists its future promotions. Moreover Dirk uses separate boxes to highlight promotions, which had to be detected beforehand.
A choice was made to only highlight the four major beer brands (Heineken, Grolsch, Brand and Hertog Jan), as those brands are always available at every supermarket.

## Aim of The Tool
The aim of the tool is to gather insight in the history of beer prices, discounts and to provide an overview of the cheapest crates of beer at any moment.
The history of beer prices is displayed at the bottom of the page. For this history two options exist. You may either choose to display history of beer prices for a specific brand at the three major supermarkets.
Moreover, you can also select to see the history of beer prices at each separate supermarket.

## Example
A relatively relatively straightforward image will highlight which brands can be obtained for the lowest price at which supermarket.
<img src="/images/beer_output.png" >

## History of Beer Prices 
### Per Supermarket

\n'''
    javascript_md = '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script> \n'

    with open(path,'w') as f:
        f.write(title_md)
        f.write(update_date_md)
        f.write(body_md)
        f.write(javascript_md)
        df=get_dataframe_brand()
        f.write(get_supermarket_graph(df))
        f.write('\n### Per Beer Brand \n')
        f.write(get_beer_graphs(df))
        f.close()

#        print('Error occurred in Generating plotly files')
#        with open(path,'w') as f:
#            f.write(title_md)
#            f.write(update_date_md)
#            f.write(body_md)
#            f.write(javascript_md)
#            f.write('*An error occurred in generating plots*')
#        f.close()

if __name__ == '__main__':
    write_markup()
    subprocess.call(['/home/pi/beer_tracker/pusher_of_page.sh'],shell=True)