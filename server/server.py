# The flask server to serve the cotnent
import datetime
from flask import Flask
from flask import render_template
from flask import make_response

# import the daily mirror scrapper
import dmScrapper
import ftScrapper

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
    resp.headers["Content-type"] = ": application/atom+xml;charset=UTF-8"
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
            logo=logo,
        )
    )
    # set the header to xml
    resp.headers["Content-type"] = "application/rss+xml;charset=UTF-8"
    # return the response
    return resp

# FT.lk ATOM Feed
@app.route("/ft/atom")
def ftAtom():
    # get current time 
    now = datetime.datetime.now()

    # get ft articles 
    articles = ftScrapper.scrape()

    # set default variables
    website_name = "FT"
    domain_name = "ft.lk"
    icon = "https://i.imgur.com/hvG1LjW.png"
    logo = "https://i.imgur.com/CYgv8JS.png"

    # render RSS jinja template
    resp = make_response(
        render_template(
            "rss.xml",
            author="FT Editor",
            updated_time=now,
            website_name=website_name,
            domain_name=domain_name,
            articles=articles,
            icon=icon,
            logo=logo,
        )
    )

    # set header
    resp.headers['content-type'] = "application/atom+xml;charset=UTF-8"
    return resp

# FT.LK RSS Feed
@app.route("/ft/rss")
def ftRss():
    # get current time
    now = datetime.datetime.now()

    # get FT articles
    articles = ftScrapper.scrape()

    # set default variables
    website_name = "FT"
    domain_name = "ft.lk"
    icon = "https://i.imgur.com/hvG1LjW.png"
    logo = "https://i.imgur.com/CYgv8JS.png"

    # render RSS jinja template
    resp = make_response(
        render_template(
            "rss.xml",
            author="FT Editor",
            updated_time=now,
            website_name=website_name,
            domain_name=domain_name,
            articles=articles,
            icon=icon,
            logo=logo,
        )
    )

    # set header
    resp.headers['content-type'] = "application/rss+xml;charset=UTF-8"
    return resp