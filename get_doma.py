import urllib.request as req
from urllib.request import build_opener, HTTPCookieProcessor
import bs4
import re
import time
import pandas as pd

case_number = 1

case = []

for round in range(150):
    
    url = "http://spmcell.cde.org.tw/Public/readdocument.aspx?documentId=" + str(case_number)
    
    opener = build_opener(HTTPCookieProcessor())
    response = opener.open(url)

    case_number= case_number+1

    data = response.read().decode("utf-8")

    root = bs4.BeautifulSoup(data, "lxml")    

    contents = root.find("div", class_="panel")

    if contents == None:
       continue
    else:
        post_title = contents.find("h3")
        post_body = contents.find("table", class_= "grid2")

        rows = [th.text.replace('\n', '') for th in post_body.find_all('td')]
        columns = [th.text.replace('\n', '') for th in post_body.find_all('th')]

        del rows[-1]
        del rows[-1]
        del rows[-1]
        
        columns.append("")

        case.append(rows)

df = pd.DataFrame(case, columns=columns)

df.to_csv(f"./data/doma_list.csv", encoding = "utf_8_sig")