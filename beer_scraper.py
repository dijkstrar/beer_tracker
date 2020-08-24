from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from contextlib import contextmanager
import time
import re
import pandas as pd


@contextmanager
def get_chrome() -> Chrome:
    # https://docs.python.org/3.7/library/contextlib.html#contextlib.contextmanager
    opts = ChromeOptions()
    opts.headless = True
    driver = Chrome(options=opts,executable_path=r'/usr/lib/chromium-browser/chromedriver')
    yield driver
    driver.close()
    driver.quit()
    
    
def albert_heijn(driver) -> dict:
    
    beer_urls = {'Heineken':'https://www.ah.nl/producten/product/wi210145/heineken-premium-pilsener',
           'Grolsch':'https://www.ah.nl/producten/product/wi232949/grolsch-premium-pilsner-krat',
           'Hertog Jan':'https://www.ah.nl/producten/product/wi2708/hertog-jan-traditioneel-natuurzuiver-bier',
           'Brand':'https://www.ah.nl/producten/product/wi227163/brand-pilsener',
           'Warsteiner':'https://www.ah.nl/producten/product/wi126867/warsteiner-pilsener'}
    
    def extract_price(soup: BeautifulSoup):
        full =float(soup.select_one("span[class*='price-amount_integer']").text)
        fract= float(soup.select_one("span[class*='price-amount_fractional']").text)/100
        return full+fract
    
    def future_promotion(driver):
        discount_selector = "div[class*='product-hero_root']"
        results_el = driver.find_element_by_css_selector(discount_selector)
        results_html = results_el.get_attribute('outerHTML')
        soup = BeautifulSoup(results_html, 'html.parser')
        discount_time = soup.select_one("span[class*='smart-label_lineclamp']")
        if discount_time is not None:
            return 'vanaf' in discount_time.text
        return False
            
    
    def visit_page(url,driver):
        driver.get(url)
        if not future_promotion(driver):
            results_selector = "div[class*='product-card-hero-price_now']"
        else:
            results_selector = "div[class*='product-card-hero-price_was']"
        results_el = driver.find_element_by_css_selector(results_selector)
        results_html = results_el.get_attribute('outerHTML')
        return results_html

    result_dict = {}
    for (beer,url) in beer_urls.items():
        results_html=visit_page(url,driver)
        soup = BeautifulSoup(results_html, 'html.parser')
        info = extract_price(soup)
        result_dict[beer] = info
    return result_dict


def dirk(driver):
    beer_urls = {'Heineken':'https://www.dirk.nl/boodschappen/dranken-sap-koffie-thee/bier/heineken-pilsener/6',
           'Grolsch':'https://www.dirk.nl/boodschappen/dranken-sap-koffie-thee/bier/grolsch-premium-pilsener-krat/8993',
           'Hertog Jan':'https://www.dirk.nl/boodschappen/dranken-sap-koffie-thee/bier/hertog-jan-pilsener/9486',
           'Brand':'https://www.dirk.nl/boodschappen/dranken-sap-koffie-thee/bier/brand-pilsener/8359',
                }
    def extract_price(soup: BeautifulSoup, discount):
        if discount:
            #https://stackoverflow.com/questions/1547574/regex-for-prices
            spantext = (soup.select("span")[1])
            match = re.findall(r'\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})',str(spantext))
            price = float(match[0])
        else:
            full =float((soup.select_one("span[class*='product-card__price__euros']").text)[:-1])
            fract= float(soup.select_one("span[class*='product-card__price__cents']").text)/100
            price = full+fract
        return price

    def visit_page(url,driver):
        driver.get(url)
        try: # discounted
            results_selector = "div[class*='product-card__discount']"
            results_el = driver.find_element_by_css_selector(results_selector)
            discount = True
        except NoSuchElementException: #not discounted
            discount = False
            results_selector = "div[class*='product-card__price__new']"
            results_el = driver.find_element_by_css_selector(results_selector)
        results_html = results_el.get_attribute('outerHTML')
        return results_html,discount

    result_dict = {}
    for (beer,url) in beer_urls.items():
        results_html,discount=visit_page(url,driver)
        soup = BeautifulSoup(results_html, 'html.parser')
        info = extract_price(soup,discount)
        result_dict[beer] = info
    return result_dict


def jumbo(driver):
    beer_urls = {'Heineken':'https://www.jumbo.com/heineken-premium-pilsener-krat-24-x-30cl/87441KRT',
           'Grolsch':'https://www.jumbo.com/grolsch-premium-pilsner-fles-24-x-30cl/147464KRT',
           'Hertog Jan':'https://www.jumbo.com/hertog-jan-traditioneel-natuurzuiver-bier-krat-24-x-30cl/865788KRT',
           'Brand':'https://www.jumbo.com/brand-bier-krat-24-x-30cl/140388KRT',
           'Warsteiner':'https://www.jumbo.com/warsteiner-krat-24-x-300ml/449245KRT'
                }
    def extract_price(soup: BeautifulSoup):
        full = float(soup.select_one('span[class*="jum-product-price__current-price--larger"]').text)
        fract = float(soup.select_one('span').text[-2:])/100
        return full+fract

    def visit_page(url,driver):
        driver.get(url)
        results_selector = "span[class*='jum-product-price__current-price']"
        time.sleep(1)
        results_el = driver.find_element_by_css_selector(results_selector)
        results_html = results_el.get_attribute('outerHTML')
        return results_html
    
    
    result_dict = {}
    for (beer,url) in beer_urls.items():
        results_html=visit_page(url,driver)
        soup = BeautifulSoup(results_html, 'html.parser')
        info = extract_price(soup)
        result_dict[beer] = info
    return result_dict

def fetch_minima():
    minima = {}
    brands = ['Heineken','Grolsch','Brand','Hertog Jan']
    with get_firefox() as driver:
        ah_prices = albert_heijn(driver)
        dirk_prices = dirk(driver)
        jumbo_prices = jumbo(driver)
    
    #write files
    for brand in brands:
        file = open('logs/'+brand+'.txt','a')
        date = pd.to_datetime("today").strftime("%Y/%m/%d")
        file.write(date+';'+str(ah_prices[brand])+';'+str(dirk_prices[brand])+';'+str(jumbo_prices[brand])+'\n')
        file.close()
    
    #minimum detection
    for brand in brands:
        minimum_price = min(ah_prices[brand],dirk_prices[brand],jumbo_prices[brand])
        if (brand,minimum_price) in ah_prices.items():
            supermarket = 'Albert Heijn'
        elif (brand,minimum_price) in dirk_prices.items():
            supermarket = 'Dirk'
        else: supermarket = 'Jumbo'
        minima[brand] = (min(ah_prices[brand],dirk_prices[brand],jumbo_prices[brand]),supermarket)
    return minima

if __name__ == '__main__':
    start_time=time.time()
    print('---FETCHING PRICES---')
    print(fetch_minima())
    print("--- %s seconds ---"% (time.time()-start_time))
