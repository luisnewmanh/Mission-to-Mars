
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt

def scrape_all():
    # Path to chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph=mars_news(browser)
    
    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": mars_hemispheres(browser),
        "last_modified": dt.datetime.now()
    }

    #quit browser
    browser.quit()
    return data

###First Scrap - Mars News
def mars_news(browser):
    # Visit the Quotes to Scrape site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    #Parse HTML
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    #Error hadling
    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        #slide_elem.find("div", class_='content_title')
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None
    
    # return scrapped info
    return news_title, news_p

# ### Second scrap - JPL Featured Images
def featured_image(browser):
    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    # Find the more info button using text and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
        
        # Use the base URL to create an absolute URL
        img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    
    except AttributeError:
        return None
        
    return img_url

# ### Third scrap - Mars Facts
def mars_facts():
    try:
        #read first table [0] from html and save it as data frame
        df = pd.read_html('http://space-facts.com/mars/')[0]
    except BaseException:
        return None
        
    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)
    #transform data set to html and add bootrstrap
    summary=df.to_html(classes="table table-striped")
    
    return summary

def mars_hemispheres(browser):
    # Visit the hemisphere website
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    #Parse HTML
    html = browser.html
    hem_soup = soup(html, 'html.parser')

    try:
        #Title list
        hems_titles = hem_soup.select('div.description a h3')
        for title in range (4):
            hems_titles[title]=hems_titles[title].text

        #Image List
        images=hem_soup.select('div.item a')
        for im in range (8):    
            test=images[im].get('href')
            url_image=f'https://astrogeology.usgs.gov{test}'
            browser.visit(url_image)
            #Parse the resulting html with soup
            html2 = browser.html
            img_soup2 = soup(html2, 'html.parser')
            #get url
            img_url_hem = img_soup2.select_one('div.downloads ul li a').get("href")
            images[im]=img_url_hem
        im_list=set(images)
        im_list=list(im_list)
        im_list.sort()

        #Create list with directories
        mars_list=[]
        for element in range (4):
            mars_dic = {"img_url": im_list[element],
                        "title": hems_titles[element]}
            mars_list.append(mars_dic)
        mars_list
    except AttributeError:
        return None
    return mars_list

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())







