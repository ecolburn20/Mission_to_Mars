from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time
import numpy as np

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)


    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    li = soup.find('li', class_='slide')
    div = li.find('div',class_='content_title')
    title = div.find('a').text
    body = li.find('div', class_='article_teaser_body').text


    url1 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url1)

    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(5)
    browser.click_link_by_partial_text('more info')
    time.sleep(5)
    browser.click_link_by_partial_href('/spaceimages/images/largesize/')

    html = browser.html
    soup1 = BeautifulSoup(html, 'html.parser')
    featured_image_url = soup1.find('img')['src']


    url2 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url2)

    html = browser.html
    soup2 = BeautifulSoup(html, 'html.parser')
    test = soup2.find('li', class_='js-stream-item')

    text =test.find('p').text
    mars_weather = text.replace('\n',' ')
    


    url3 = 'http://space-facts.com/mars/'
    tables = pd.read_html(url3)
    table = tables[0]
    table.columns = ['Description','Value']
    table = table.set_index('Description')
    mars_table = table.to_html()



    url4 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url4)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    dv = soup.find_all('div', class_='item')
    hemispheres = []
    for i in dv:
        hem = i.h3.text
        hemispheres.append(hem)


    images = []
    for h in hemispheres:
        url4 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url4)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        browser.click_link_by_partial_text(h)
        img_url = browser.find_by_tag('img')[3]['src']
        images.append(img_url)



    hemisphere_image_urls = [
        {"title": hemispheres[0], "img_url": images[0]},
        {"title": hemispheres[1], "img_url": images[1]},
        {"title": hemispheres[2], "img_url": images[2]},
        {"title": hemispheres[3], "img_url": images[3]},
    ]
    
    browser.quit()
    mars_data = {
        "title": title,
        "body": body,
        "image_url": featured_image_url,
        "weather": mars_weather,
        "hemisphere_image_urls": hemisphere_image_urls,
        "table": mars_table
    }
    return mars_data
    return tables