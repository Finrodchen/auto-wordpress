import urllib.request as req
import bs4
import re
import time
import pandas as pd

url = "https://tsscosecurities.blogspot.com/2020/07/Global-Stock-20200731.html"
news = []

for round in range(50):

    request = req.Request(url, headers = {
        "User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-CN; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15"
    })

    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")

    root = bs4.BeautifulSoup(data, "lxml") 
    body = root.find("div", class_= "post-body entry-content")

    contents = body.getText()

    old_post = root.find("div", class_= "blog-pager")
    new_post_link = old_post.find("a", class_="blog-pager-newer-link")
    
    if new_post_link == None:
        break
    else:
        newurl = new_post_link.get("href")
        
    c = [url, root.title.string, contents]
    news.append(c)
 
    url = newurl
    
    time.sleep(1)


df = pd.DataFrame(news)

df.to_csv(f"./data/fin_news.csv", encoding = "utf_8_sig")