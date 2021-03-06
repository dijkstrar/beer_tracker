# beer_tracker
Daily scrape beer crate prices of major brands in the Netherlands. 
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
A relatively straightforward image will highlight which brands can be obtained for the lowest price at which supermarket right now.
![alt text](<output.png>) 
