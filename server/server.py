# The flask server to serve the cotnent
import datetime
from flask import Flask
from flask import render_template
from flask import make_response

# import the daily mirror scrapper
import dmScrapper

# create a flask server
app = Flask(__name__)
# index route
@app.route("/")
def index():
    # TODO: create a better landing page
    return "<p>Hello, World!</p>"


# daily mirror atom feed route
@app.route("/dailymirror/atom")
def dailymirror():
    # get current datetime
    now = datetime.datetime.now()
    # get the articles
    articles = dmScrapper.scrape()
    # set default variables
    website_name = "DailyMirror"
    domain_name = "dailymirror.lk"
    icon = "https://i.imgur.com/KUxd2xS.png"
    logo = "https://i.imgur.com/XxDtRdT.jpg"
    # render the jinja template
    resp = make_response(
        render_template(
            "atom.xml",
            author="DailyMirror Editor",
            updated_time=now,
            website_name=website_name,
            domain_name=domain_name,
            articles=articles,
            icon=icon,
            logo=logo,
        )
    )
    #  set the header to xml
    resp.headers["Content-type"] = ": text/atom+xml;charset=UTF-8"
    #  return response
    return resp


# DailyMirror RSS feed
@app.route("/dailymirror/rss")
def dailymirrorRss():
    # get the current datetime
    now = datetime.datetime.now()
    # get the articles
    articles = dmScrapper.scrape()
    # set the default variables
    website_name = "DailyMirror"
    domain_name = "dailymirror.lk"
    icon = "https://i.imgur.com/KUxd2xS.png"
    logo = "https://i.imgur.com/XxDtRdT.jpg"
    # render the jinja template
    resp = make_response(
        render_template(
            "rss.xml",
            author="DailyMirror Editor",
            updated_time=now,
            website_name=website_name,
            domain_name=domain_name,
            articles=articles,
            icon=icon,
        )
    )
    # set the header to xml
    resp.headers["Content-type"] = ": text/rss+xml;charset=UTF-8"
    # return the response
    return resp
