
#DOWNLOAD IPYNB AS SCRAPE_MARS AND MAKE SCRAPE FUNCTION
#EDIT UNNECESSARY DATA
# coding: utf-8

# Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. <br>
# Assign the text to variables that you can reference later.



import os
from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
import pymongo
import pandas as pd 
import time
import datetime
from pprint import pprint
import time


#define  function for exec path for chromedriver.exe. 

def init_browser():
  executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
  return Browser('chrome', **executable_path)





def mars_scrape():
  #to scrape all necessary info from mars related websites

  #empty dictionary
  mars_info_dict = dict()




# NASA MARS NEWS

  url = "https://mars.nasa.gov/news/"
  browser = init_browser()
  browser.visit(url)
  #browser.is_element_present_by_css("ul.item_list li.slide", wait_time =2)
  html = browser.html

  #create soup object
  #parse html with bs
  news_soup = bs(html, 'html.parser')
  #print(news_soup.prettify())
  slide_elem = news_soup.select_one('ul.item_list li.slide')
  # print(slide_elem.prettify())

  #slide_elem.find("div", class_='content_title')
  # Use the parent element to find the first a tag and save it as `news_title`
  news_title = slide_elem.find("div", class_='content_title').get_text()
  # news_title
  # Use the parent element to find the paragraph text
  news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
  # news_p
  mars_info_dict["Mars_news_title"] = news_title
  mars_info_dict["Mars_news_body"] = news_p







  #IMAGES

  url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
  browser.visit(url2)
  time.sleep(3)

  full_img_elem = browser.find_by_id('full_image')
  full_img_elem.click()
  time.sleep(3)

  # try except stuff
  more_info_elem = browser.find_link_by_partial_text('more info')
  more_info_elem.click()
  time.sleep(3)


  # ### Soup Object
  html_image = browser.html
  image_soup = bs(html_image, 'html.parser')

  image_path = image_soup.select_one('figure.lede a img')

  partial_img = image_path.get("src")
  #partial_img

  full_img = 'https://www.jpl.nasa.gov' + partial_img
  #full_img

  mars_info_dict["Mars_featured_image_url"]= full_img







  # ### Mars Weather
  url3 = "https://twitter.com/marswxreport?lang=en"
  browser.visit(url3)
  html3 = browser.html
  weather_soup = bs(html3, 'html.parser')
  #print(weather_soup.prettify())

  # First, find a tweet with the data-name `Mars Weather`
  mars_weather_tweet = weather_soup.find('div', attrs={"class": "tweet", "data-name": "Mars Weather"})
  mars_weather_tweet


  mars_weather = mars_weather_tweet.find('p', 'tweet-text').get_text()
  mars_weather

  mars_info_dict["Mars_tweet_weather"] = mars_weather
  pprint(mars_info_dict)







  # ## Mars Facts
  url4 = "https://space-facts.com/mars/"

  df = pd.read_html(url4)[0]

  time.sleep(1)

  df.columns=['description', 'value']
  df.set_index('description', inplace=True)

  df.to_html("mars_facts.html", index = False)

  mars_html = df.to_html(classes="mars_facts table table-striped")
  mars_info_dict["Mars_facts_table"] = mars_html
  pprint(mars_info_dict)






# ## Mars Hemisphere
  url5 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
  browser.visit(url5)
  time.sleep(3)

  hemisphere_image_urls = []

  # First, get a list of all of the hemispheres
  links = browser.find_by_css("a.product-item h3")
  print("Printing links")
  print(links)

  # Next, loop through those links, click the link, find the sample anchor, return the href
  for i in range(len(links)):
      hemisphere = {}
      print("i =" + str(i))

     # We have to find the elements on each loop to avoid a stale element exception
      browser.find_by_css("a.product-item h3")[i].click()
      time.sleep(3)

     # Next, we find the Sample image anchor tag and extract the href
      sample_elem = browser.find_link_by_text('Sample').first
      hemisphere['img_url'] = sample_elem['href']
      print(sample_elem)
      print(hemisphere)
      
     # Get Hemisphere title
      hemisphere['title'] = browser.find_by_css("h2.title").text

     # Append hemisphere object to list
      hemisphere_image_urls.append(hemisphere)
      
      browser.back()




#Return final dictionary with all the mars information that was scraped in the 5 steps above. 
  print("just before final return of mars_info_dict")
  mars_return_dict =  {
      "News_Title": mars_info_dict["Mars_news_title"],
      "News_Summary" :mars_info_dict["Mars_news_body"],
      "Featured_Image" : mars_info_dict["Mars_featured_image_url"],
      "Weather_Tweet" : mars_info_dict["Mars_tweet_weather"],
      "Facts" : mars_info_dict["Mars_facts_table"],
      "Hemisphere_Image_urls": hemisphere_image_urls,
      #"Date" : mars_info_dict["Date_time"],
    }
  print(mars_return_dict)
  return mars_return_dict


# output_dict = mars_scrape()
# print("Printing output..")
# print(output_dict)

