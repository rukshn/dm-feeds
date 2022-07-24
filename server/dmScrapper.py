# This is the scrapper written to scrape DailyMirror.lk website
# And generate an RSS feed since DailyMirror does not generate an RSS feed
# for their news website
# Written by Rukshan Ranatunge <rukshan@ruky.me>

# Import beautifulsoup requests and datetime
from bs4 import BeautifulSoup
import requests
import datetime

# Function to make request
# Takes URL as a parameter
# Returns the response code and content
def makeRequest(url):
    # There has to be a user agent for DailyMirror
    # DailyMirror blocks all requests without a user agent
    headers = {
        "User-Agent": "FeedBurner By Rukshan",
        "Accept": "*.*",
    }
    # Make the request
    getRequest = requests.get(url, headers=headers)

    # Return the status code and content
    return [getRequest.status_code, getRequest.text]


# Main Scrape fucntion
def scrape():
    # set base url to daily mirror
    baseUrl = "https://www.dailymirror.lk"
    # make a get request to daily mirror
    req = makeRequest(baseUrl)

    # if ther status code is 200 (successful request)
    if req[0] == 200:
        # parse the response text
        soup = BeautifulSoup(req[1], "html.parser")
        # the latest news is contained within a div with an ID called breakingnewsads
        latestNews = soup.find("div", {"id": "breakingnewsads"})

        # all all links (a tags) inside the breakingnewsads div
        links = latestNews.findAll("a", href=True)

        # linklist is the object that will be returned by the function
        # containing link, article title, article content and published time
        linkList = []

        # enumerate all the links
        for index, link in enumerate(links):
            # the titles of articles are inside of an H3 tag within a link (a tag)
            # there are also links (a tags) but with image tags within the a tags not h3
            # the if will exluce those and only iterate though h3 tags
            if link.find("h3") != None:
                # navigate to each link (article) and get it's content
                # make a get request
                getArticle = makeRequest(link["href"])
                # if the article responds with a status code of 200
                if getArticle[0] == 200:
                    # parse the article content HTML using BS
                    soup = BeautifulSoup(getArticle[1], "html.parser")
                    # get the content
                    content = soup.find("div", {"class": "inleft"})
                    # extract the main article content
                    article_content = content.find(
                        "header", {"class": "inner-content"}
                    )
                    # extract the published time
                    gtime = content.find("span", {"class": "gtime"}).text
                    # convert the published time to a UTF time
                    article_updated = (
                        str(datetime.datetime.strptime(gtime, "%d %B %Y %I:%M %p"))
                        + "+0530"
                    )
                # extract the article title
                title = link.find("h3").text
                # extract the href of the link
                url = link["href"]
                # create an object with title, url, updated time and content
                temp = {
                    "title": title,
                    "url": url,
                    "updated": article_updated,
                    "content": article_content,
                }
                # add it to linkList
                linkList.append(temp)
        return linkList
    else:
        # if the status code to initial request is not 200 return the status code
        print("error - error code: " + str(req[0]))
        print(req[1])
        return req[0]
