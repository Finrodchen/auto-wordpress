import urllib.request as req
import bs4
import re
import time
import pandas as pd

url = "https://ibmi.taiwan-healthcare.org/news_detail.php?REFDOCTYPID=0o4dd9ctwhtyumw0&REFDOCID=0qf8jpira4iij9ir"
news = []

for round in range(100):

    request = req.Request(url, headers = {
        "User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-CN; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15"
    })

    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")

    root = bs4.BeautifulSoup(data, "lxml")
    post_title = root.find("div", class_="center-left-title col-xs-12")
    post_date = root.find("div", class_="center-left-date")
    post_body = root.find("div", class_= "center-left-value")

    content_title = post_title.getText()
    content_date = post_date.getText()
    content_body = post_body.getText()

    old_post = root.find("div", class_= "left-top-1")
    old_post_link = old_post.find("a")


    if old_post_link == None:
         break
    else:
        oldurl = old_post_link.get("href")

    c = [url, content_title, content_date, content_body]

    news.append(c)
    
    url = "https://ibmi.taiwan-healthcare.org/" + oldurl.replace("./", "")

    time.sleep(1)

df = pd.DataFrame(news)

df.to_csv(f"./data/ibmi_news.csv", encoding = "utf_8_sig")