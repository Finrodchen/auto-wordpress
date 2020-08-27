import urllib.request as req
from urllib.request import build_opener, HTTPCookieProcessor
import bs4
import re
import time
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

case_number = 1

rows = []
columns = []

scopes = ["https://spreadsheets.google.com/feeds"]

credentials = ServiceAccountCredentials.from_json_keyfile_name(
        "credentials.json", scopes)

client = gspread.authorize(credentials)

sheet = client.open_by_key(
        "1AvkvzvahCl5ybBkWIJwGQvOhwQ84gHyZT743ZeXclwQ").sheet1

for round in range(150):

    scopes = ["https://spreadsheets.google.com/feeds"]

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
            "credentials.json", scopes)

    client = gspread.authorize(credentials)

    sheet = client.open_by_key(
            "1AvkvzvahCl5ybBkWIJwGQvOhwQ84gHyZT743ZeXclwQ").sheet1
   
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
        rows.insert(1, post_title.getText())
        columns = [th.text.replace('\n', '') for th in post_body.find_all('th')]
        columns.insert(1,"執行醫院")

        del rows[-1]
        del rows[-1]
        del rows[-1]
        
        columns.append("")

        sheet.insert_row(rows, 1)

sheet.insert_row(columns, 1)

