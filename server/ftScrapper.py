# This is the scrapper written to scrape FT.lk website
# And generate an RSS feed since FT does not generate an RSS feed
# for their news website
# Written by Rukshan Ranatunge <rukshan@ruky.me>

# import beautifulsoup, requests and datetime
from bs4 import BeautifulSoup
import requests
import datetime

# import the makeRequest function from the dmScrapper
from dmScrapper import makeRequest

def scrape():
  # set baseUrl
  baseUrl = "https://ft.lk"
  # make get request to ft.lk home page
  req = makeRequest(baseUrl)

  # if status code is 200 (successful) continue parsing the page
  if req[0] == 200:
    # parse the home page
    soup = BeautifulSoup(req[1], 'html.parser')
    # the latest news are in a div with the id breakingnewsads
    # get contents of the div
    newsContainer = soup.find("div", {"id": "breakingnewsads"})

    # collect all the news elemens from the div
    latestNews = newsContainer.findAll("div", {"class": "cardbs"})
    
    # linklist is the object that will be returned by the function
    # containing link, article title, article content and published time
    linkList = []

    # enumarate all the links
    for index, news in enumerate(latestNews):
      link = news.find("a", href=True)  
      href = link["href"]
      title = link.find("h3").text

      # get individual article
      getArticle = makeRequest(href)
      if getArticle[0] == 200:
        # parse article text
        soup = BeautifulSoup(getArticle[1], "html.parser")
        # get article content
        article_content = soup.find("header", {"class": "inner-content"})
        # get article published time
        gtime = soup.find("span", {"class": "gtime"}).text
        # contvert the time to UTF fime
        article_updated = (str(datetime.datetime.strptime(gtime, "%A, %d %B %Y %H:%M"))) + "+0530"
      
      # create a temporary element to hold data
      temp = {
        "title": title,
        "url": href,
        "updated": article_updated,
        "content": article_content
      }

      # add the element to linkList
      linkList.append(temp)

    return linkList

  else:
    # if the status code is not 200 then return the error code
    print("error - error code: " + str(req[0])) 
    print(req[1])
    return req[0]