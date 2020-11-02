#!/usr/bin/env python
# coding: utf-8

# In[2]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd


# In[3]:


# Path to chromedriver
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# In[4]:


# Visit the Quotes to Scrape site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# In[5]:


#Parse HTML
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')


# In[6]:


slide_elem.find("div", class_='content_title')


# In[12]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# In[13]:


news_title = slide_elem.find("div", class_='content_title')
news_title.text


# In[14]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p


# ### Featured Images

# In[15]:


# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)


# In[16]:


# Find and click the full image button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()


# In[17]:


# Find the more info button using text and click that
browser.is_element_present_by_text('more info', wait_time=1)
more_info_elem = browser.links.find_by_partial_text('more info')
more_info_elem.click()


# In[18]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[19]:


# Find the relative image url
img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel


# In[20]:


# Use the base URL to create an absolute URL
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url


# In[26]:


#read first table [0] from html and save it as data frame
df = pd.read_html('http://space-facts.com/mars/')[0]
df.columns=['description', 'value']
df.set_index('description', inplace=True)
df


# In[28]:


#transform data set to html
summary=df.to_html()


# Deliverable 1: Scrape Full-Resolution Mars Hemisphere Images and Titles

# In[134]:


# Visit the hemisphere website
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# In[135]:


#Parse HTML
html = browser.html
hem_soup = soup(html, 'html.parser')


# In[136]:


#Title list
hems_titles = hem_soup.select('div.description a h3')
for title in range (4):
    hems_titles[title]=hems_titles[title].text
hems_titles


# In[137]:


#Image List
images=hem_soup.select('div.item a')
images


# In[138]:


#extract URL
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
im_list


# In[142]:


#Create list with directories
mars_list=[]
for element in range (4):
    mars_dic = {"img_url": im_list[element],
                "title": hems_titles[element]}
    mars_list.append(mars_dic)
mars_list


# In[143]:


#quit browser
browser.quit()


# In[ ]:




