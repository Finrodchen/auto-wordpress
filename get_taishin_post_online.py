import urllib.request as req
import bs4
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials

url = "https://tsscosecurities.blogspot.com/2020/07/Global-Stock-20200731.html"


for round in range(100):

    request = req.Request(url, headers = {
        "User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-CN; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15"
    })

    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")

    scopes = ["https://spreadsheets.google.com/feeds"]

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
            "credentials.json", scopes)

    client = gspread.authorize(credentials)

    sheet = client.open_by_key(
            "1vqxfYK_UMnvVzeY1wX5rjQnNUWUylGejEVlpgnFY-jI").sheet1

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

    sheet.insert_row(c, 1)
     
    url = newurl

