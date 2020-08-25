import pandas as pd 
import time
import matplotlib.pyplot as plt
import plotly
import plotly.graph_objects as go
import plotly.express as px
import subprocess
import sys

brands = ['Heineken','Grolsch','Brand','Hertog Jan']
#https://stackoverflow.com/questions/46410738/plotly-how-to-select-graph-source-using-dropdown
#https://plotly.com/python/dropdowns/
def get_html(brand,df):
    fig = px.line(df, x=df.index, y=column, title=None)#get_title(column)
    fig.update_yaxes(rangemode="tozero")
    fig.update_traces(line_color='#000')
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=24, label="24h", step="hour", stepmode="todate"),
                dict(count=7, label="1w", step="day", stepmode="todate"),
                dict(count=14, label="2w", step="day", stepmode="todate"),
                dict(count=1, label="1m", step="month", stepmode="todate"),
                dict(count=6, label="6m", step="month", stepmode="todate"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(step="all",label="All")
            ])
        )
    )
    fig.update_layout(template="simple_white")

    string = plotly.io.to_html(fig,full_html=False,include_plotlyjs=False)
    string=string.replace("\n", "")
    return(string)

def write_markup():
    ############################ CHANGE PATHS #######################
    path = 'output.md' #'/home/pi/dijkstrar.github.io/_portfolio/beerprices.md'
    title_md = "--- \ntitle: \'Beerprice Tracker\' \ndate: 2020-08-25 \npermalink: /portfolio/2020/08/beerprices/ \n---\n\n"
    update_date_md = "History of beer prices and an overview on where to get the cheapest beer. Updated at: "+str(pd.to_datetime("today").strftime("%Y/%m/%d %H:%M")+"\n\n")
    body_md = '''This is a dynamically updating web page.\n
# beer_tracker
This is a brief overview on the tool that scrapes beer crate prices daily.
Beer prices are collected from Albert Heijn, Dirk and Jumbo

## Methodology
For the scraping Selenium, together with Beautifulsoup is used. A choice was made for Selenium as the Jumbo website blocks access via the request package.
In order to overcome non-overlapping discounting periods, daily beer prices are scraped. Furthermore, due to different lay-outs and html contents, custom made functions had to be designed to overcome these issues. 
An example of such an problematic aspect, is the fact that Albert Heijn lists its future promotions. Moreover Dirk uses separate boxes to highlight promotions, which had to be detected beforehand.
A choice was made to only highlight the four major beer brands (Heineken, Grolsch, Brand and Hertog Jan), as those brands are always available at every supermarket.

## Aim of The Tool
The aim of the tool is to gather insight in the history of beer prices, discounts and to provide an overview of the cheapest crates of beer at any moment.
The history of beer prices is displayed at the bottom of the page. 

## Example
A relatively relatively straightforward image will highlight which brands can be obtained for the lowest price at which supermarket.
![alt text](<output.png>) \n'''
    javascript_md = '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script> \n'
    try:
        with open(path,'w') as f:
            f.write(title_md)
            f.write(update_date_md)
            f.write(body_md)
            f.write(javascript_md)
            for brand in brands:
                df=pd.read_csv('logs/'+brand+'.txt',sep=';',index_col='Date')
                df.index=pd.to_datetime(df.index)

        f.close()
    except:
        print('Error occurred in Generating plotly files')
        with open(path,'w') as f:
            f.write(title_md)
            f.write(update_date_md)
            f.write(body_md)
            f.write(javascript_md)
            f.write('*An error occurred in generating plots*')
        f.close()

if __name__ == '__main__':
    write_markup()
    # subprocess.call(['/home/pi/net_speed/pusher_of_page.sh'],shell=True)